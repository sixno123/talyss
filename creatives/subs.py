#!/usr/bin/env python3
"""Align the script to the measured word timings and emit karaoke-style ASS
subtitles that replace the burned-in ones."""
import json, re, subprocess, unicodedata, difflib
from PIL import ImageFont

# ---------------------------------------------------------------- config
W, H = 720, 1280
PLATE_TOP, PLATE_BOT = 930, 1120          # frosted band that hides the old text
CAP_Y = (PLATE_TOP + PLATE_BOT) // 2      # captions sit centred in the band
FONT_PX = 54
MAX_TEXT_W = 610                          # keep ~55px breathing room each side
ENDCARD_T = 43.75                         # subtitles stop where the new card starts
GOLD = "&H1BA9DE&"                        # &HBBGGRR& = #DEA91B, warm brand accent

# Display text == spoken text, except digits the TTS read out in full.
LINES = [
    "Voici comment j'ai arrêté de jeter mon argent",
    "dans les soins des pieds",
    "Avant, c'était pédicure toutes les 3 semaines",
    "parce que mes talons étaient une catastrophe",
    "Dès qu'ils séchaient, ça craquelait et ça ressemblait à ça",
    "Impossible de mettre des sandales ou des talons sans complexer",
    "J'ai testé toutes les alternatives : pierre ponce, râpes manuelles",
    "soit ça irrite, soit ça ne fait rien",
    "Certaines, on dirait carrément des râpes à fromage",
    "Et puis une amie m'a fait découvrir la râpe électrique Talyss",
    "Elle utilise des petits disques abrasifs à usage unique",
    "et elle enlève toute la peau morte, sans douleur",
    "Vitesse réglable, et ça marche sur peau sèche ou humide",
    "Résultat : des pieds incroyablement doux et lisses",
    "Le kit arrive avec 60 disques, de quoi tenir des mois",
    "Les stocks partent vite, alors commandez maintenant sur Talyss",
]
SPOKEN = {"3": "trois", "60": "soixante"}


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]", "", s)


# ------------------------------------------------- whisper tokens -> times
raw = json.load(open("words.json", encoding="utf-8"))
asr = []
for it in raw:                       # re-join "j" + "'ai" that whisper splits
    if it["w"].startswith("'") and asr:
        asr[-1] = {"w": asr[-1]["w"] + it["w"], "s": asr[-1]["s"], "e": it["e"]}
    else:
        asr.append(dict(it))

# ------------------------------------------------- script tokens
script = []                          # (line_index, display_word, norm_spoken)
for li, line in enumerate(LINES):
    for word in line.split():
        script.append((li, word, norm(SPOKEN.get(word.strip(",.:"), word))))

# ------------------------------------------------- align the two streams
sm = difflib.SequenceMatcher(None, [t[2] for t in script],
                             [norm(a["w"]) for a in asr], autojunk=False)
times = [None] * len(script)
for i, j, n in sm.get_matching_blocks():
    for k in range(n):
        times[i + k] = (asr[j + k]["s"], asr[j + k]["e"])

matched = sum(t is not None for t in times)
print(f"aligned {matched}/{len(script)} script words to the audio")

# Words the ASR misheard have no time. Spread each unmatched RUN evenly across the
# hole between its aligned neighbours — filling them individually would give every
# word in the run the same start and put cards out of order.
i = 0
while i < len(times):
    if times[i] is not None:
        i += 1
        continue
    j = i
    while j < len(times) and times[j] is None:
        j += 1
    n = j - i
    prev = times[i - 1][1] if i > 0 else 0.0
    nxt = times[j][0] if j < len(times) else prev + 0.30 * n
    step = max(nxt - prev, 0.12 * n) / n
    for k in range(i, j):
        times[k] = (prev + step * (k - i), prev + step * (k - i + 1))
    i = j

# ------------------------------------------------- chunk into caption cards
font = ImageFont.truetype(
    subprocess.run(["fc-match", "-f", "%{file}", "Montserrat:weight=extrabold"],
                   capture_output=True, text=True).stdout.strip(), FONT_PX)

def width(text):
    return font.getbbox(text)[2] - font.getbbox(text)[0]

chunks, cur = [], []
for idx, (li, word, _) in enumerate(script):
    same_line = cur and script[cur[0]][0] == li
    trial = " ".join(script[k][1] for k in cur + [idx])
    if same_line and width(trial) <= MAX_TEXT_W:
        cur.append(idx)
    else:
        if cur:
            chunks.append(cur)
        cur = [idx]
if cur:
    chunks.append(cur)

# A card shouldn't end on a number or a function word ("toutes les 3" / "réglable, et").
# Push such trailing tokens onto the next card, right-to-left so widths stay valid.
TRAIL_BAD = {"le", "la", "les", "de", "des", "du", "d", "a", "et", "ou", "sur", "un",
             "une", "mon", "ma", "mes", "son", "sa", "ses", "ce", "cette", "au", "aux",
             "en", "dans", "pour", "avec", "que", "qui", "ne", "se", "je", "tu", "il",
             "elle", "on", "tout", "toute", "toutes"}

for i in range(len(chunks) - 2, -1, -1):
    if script[chunks[i][0]][0] != script[chunks[i + 1][0]][0]:
        continue                                    # different script line, leave it
    for _ in range(2):                              # at most two tokens per card
        if len(chunks[i]) < 2:
            break
        word = script[chunks[i][-1]][1]
        if word[-1] in ",.:;!?":                    # punctuation is a natural break
            break
        key = norm(word)
        if not (key in TRAIL_BAD or key.isdigit()):
            break
        moved = [chunks[i][-1]] + chunks[i + 1]
        if width(" ".join(script[k][1] for k in moved)) > MAX_TEXT_W:
            break
        chunks[i] = chunks[i][:-1]
        chunks[i + 1] = moved

cards = []
for n, ids in enumerate(chunks):
    text = " ".join(script[k][1] for k in ids)
    start = times[ids[0]][0]
    own_end = times[ids[-1]][1]
    nxt = times[chunks[n + 1][0]][0] if n + 1 < len(chunks) else own_end + 0.4
    end = max(min(nxt, own_end + 0.75), start + 0.25)   # never zero/negative length
    cards.append({"text": text, "start": start, "end": end, "line": script[ids[0]][0]})

cards = [c for c in cards if c["start"] < ENDCARD_T]     # card takes over after
for c in cards:
    c["end"] = min(c["end"], ENDCARD_T)

# ------------------------------------------------- write ASS
def ts(t):
    cs = int(round(t * 100))
    h, cs = divmod(cs, 360000)
    m, cs = divmod(cs, 6000)
    s, cs = divmod(cs, 100)
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Montserrat ExtraBold,{FONT_PX},&H00FFFFFF,&H00101010,&H80000000,0,0,0,0,100,100,0.4,0,1,3.4,2.2,5,40,40,40,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

with open("subs.ass", "w", encoding="utf-8") as f:
    f.write(head)
    for c in cards:
        body = re.sub(r"(Talyss)", r"{\\c" + GOLD + r"}\1{\\c&H00FFFFFF&}", c["text"])
        f.write(f"Dialogue: 0,{ts(c['start'])},{ts(c['end'])},Cap,,0,0,0,,"
                f"{{\\pos({W//2},{CAP_Y})\\fad(70,70)}}{body}\n")

print(f"{len(cards)} caption cards, last ends {cards[-1]['end']:.2f}s")
for c in cards[:6]:
    print(f"  {c['start']:6.2f}-{c['end']:6.2f}  {c['text']}")
print("  ...")
for c in cards[-4:]:
    print(f"  {c['start']:6.2f}-{c['end']:6.2f}  {c['text']}")
