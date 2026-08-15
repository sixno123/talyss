#!/usr/bin/env python3
"""Créa « Mielle Glow » -> Talyss, deux versions.

A : montage d'origine, habillé Talyss.
B : remonté, ~20 s.

Dans les deux cas la voix d'origine est conservée mais rendue MUETTE sur le nom
du concurrent (17,62-18,18 s). Couper la piste décalerait l'image ; la taire ne
décale rien, et le sous-titre affiche « Talyss » pendant ce silence.
La revendication « -50 % » (à partir de 35,58 s) est absorbée par la carte de fin.
"""
import json, subprocess, unicodedata, re, sys
from PIL import Image, ImageDraw, ImageFont

W, H = 720, 1280
SRC = "/root/.claude/uploads/b6b4b174-cc8a-5915-a346-1947ec943bb5/4a78dbe0-ad2237375970125334hd.mp4"
CARD = "/home/user/talyss/creatives/endcard.png"

# Sous-titres incrustés mesurés : x 99-639, y 970-1053. Le cartouche doit les
# couvrir ET garder le texte au-dessus de l'interface Reels (~y 1024), d'où un
# cartouche plus haut que large-nécessaire, texte calé dans sa moitié haute.
PLATE_X, PLATE_Y, PLATE_W, PLATE_H, PLATE_R = 60, 920, 620, 160, 32
CAP_Y = 985                       # bloc de texte ~950-1020 : zone sûre
FONT_PX, MAX_TEXT_W = 52, 545
PLATE_RGBA = (255, 255, 255, 255)
ACCENT, INK = "&H00264E7E&", "&H001B1B1B&"      # #7E4E26 brun, #1B1B1B encre
KEYWORDS = ["Talyss", "60 disques", "ultra lisse", "corne disparaît", "zéro galère"]

MUTE = (17.58, 18.24)             # « honey glow »
WORD = "w_talyss.wav"             # « Talyss » recalé en hauteur (voir pitch_fit.py)
WORD_AT = 17.60                   # démarre dans la fenêtre muette, 0,04 s de marge
CARD_HOLD = 3.0

# Texte réellement affiché, jeton par jeton (l'ASR se trompe : « crouchés »,
# « racleés », « musiquet », « rappe », « faisse », « rédits »…).
# « _ » colle deux mots en un seul jeton audio.
DISPLAY = """Toi tu as les pieds croûtés là, toi tu as les pieds
ravagés par la misère là, les pieds qui déchirent le moustiquaire. Les
filles, si vous voulez pas finir comme ça, écoutez bien, crème, râpe,
pierre, ponce, j'ai tout testé, résultat, rien. Et la corne ça garde
la transpi, donc oui, odeur, bactéries, pas glam. Puis j'ai testé Talyss,
franchement, deux minutes, zéro galère, tu passes, la corne disparaît, résultat.
T'as le_talon ultra lisse et effet spa pédicure, alors que je suis
posée sur mon canapé et avec les 60 disques inclus, je suis
large tout l'été. Si tu veux des pieds sexy et ready pour
sortir en sandale n'importe quand, clique, essaye et reviens me dire merci.""".split()


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]", "", s)


def ts(t):
    cs = int(round(t * 100))
    h, cs = divmod(cs, 360000)
    m, cs = divmod(cs, 6000)
    s, cs = divmod(cs, 100)
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


# ------------------------------------------------------------------ jetons
raw = json.load(open("words.json", encoding="utf-8"))[:126]     # jusqu'à « merci. »
toks = []
for it in raw:                                   # recoller « j » + « 'ai »
    if it["w"].startswith("'") and toks:
        toks[-1] = {"w": toks[-1]["w"] + it["w"], "s": toks[-1]["s"], "e": it["e"]}
    else:
        toks.append(dict(it))
# « honey » + « glow » deviennent un seul jeton, affiché « Talyss »
i = next(k for k, t in enumerate(toks) if norm(t["w"]) == "honey")
toks[i] = {"w": "Talyss,", "s": toks[i]["s"], "e": toks[i + 1]["e"]}
del toks[i + 1]

assert len(toks) == len(DISPLAY), f"{len(toks)} jetons audio vs {len(DISPLAY)} affichés"
SRC_WORDS = [(d.replace("_", " "), t["s"], t["e"]) for d, t in zip(DISPLAY, toks)]
print(f"{len(SRC_WORDS)} jetons alignés, dernier mot à {SRC_WORDS[-1][2]:.2f}s")

font = ImageFont.truetype(
    subprocess.run(["fc-match", "-f", "%{file}", "Montserrat:weight=extrabold"],
                   capture_output=True, text=True).stdout.strip(), FONT_PX)


def text_w(t):
    b = font.getbbox(t)
    return b[2] - b[0]


# ------------------------------------------------------------------ pastille
S = 4
plate = Image.new("RGBA", (PLATE_W * S, PLATE_H * S), (0, 0, 0, 0))
ImageDraw.Draw(plate).rounded_rectangle(
    [0, 0, PLATE_W * S - 1, PLATE_H * S - 1], radius=PLATE_R * S, fill=PLATE_RGBA)
plate.resize((PLATE_W, PLATE_H), Image.LANCZOS).save("plate.png")
assert PLATE_X <= 99 and PLATE_X + PLATE_W >= 639, "pastille trop étroite"
assert PLATE_Y <= 970 and PLATE_Y + PLATE_H >= 1053, "pastille trop courte"

HEAD = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Montserrat ExtraBold,{FONT_PX},{INK},&H00FFFFFF,&H80FFFFFF,0,0,0,0,100,100,0.4,0,1,0,0,5,40,40,40,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def write_ass(words, path):
    """Cartons karaoké : un événement ASS par mot prononcé."""
    shown = [norm(w[0]) for w in words]
    is_kw = [False] * len(words)
    for phrase in KEYWORDS:
        ph = [norm(x) for x in phrase.split()]
        for i in range(len(shown) - len(ph) + 1):
            if shown[i:i + len(ph)] == ph:
                for k in range(i, i + len(ph)):
                    is_kw[k] = True

    cards, cur = [], []
    for i, (t, s, e) in enumerate(words):
        if cur and text_w(" ".join(words[k][0] for k in cur + [i])) > MAX_TEXT_W:
            cards.append(cur); cur = []
        cur.append(i)
        if t[-1] in ".!?" or (len(cur) >= 3 and t[-1] in ",;:") or len(cur) >= 4:
            cards.append(cur); cur = []
    if cur:
        cards.append(cur)

    n = 0
    with open(path, "w", encoding="utf-8") as f:
        f.write(HEAD)
        for ci, ids in enumerate(cards):
            c_start = words[ids[0]][1]
            c_end = (words[cards[ci + 1][0]][1] if ci + 1 < len(cards)
                     else words[ids[-1]][2] + 0.4)
            bounds = [c_start]
            for j in range(1, len(ids)):
                bounds.append(min(max(words[ids[j]][1], bounds[-1]), c_end))
            bounds.append(c_end)
            live = [j for j in range(len(ids)) if bounds[j + 1] - bounds[j] > 0.001]
            for pos, j in enumerate(live):
                body = " ".join(
                    f"{{\\c{ACCENT}}}{words[k][0]}{{\\c{INK}}}"
                    if (m == j or (is_kw[k] and m < j)) else words[k][0]
                    for m, k in enumerate(ids))
                fin = 60 if pos == 0 else 0
                fout = 60 if pos == len(live) - 1 else 0
                f.write(f"Dialogue: 0,{ts(bounds[j])},{ts(bounds[j + 1])},Cap,,0,0,0,,"
                        f"{{\\pos({W // 2},{CAP_Y})\\fad({fin},{fout})}}{body}\n")
                n += 1
    print(f"  {len(cards)} cartons, {n} événements -> {path}")


def build(tag, shots, audio_keep):
    """shots/audio_keep : listes de (début, fin) dans la source."""
    shots_dur = sum(e - s for s, e in shots)
    audio_dur = sum(e - s for s, e in audio_keep)
    # La carte doit tenir jusqu'à la fin de la voix : sinon `-t` tronque la piste
    # et le dernier mot du CTA est coupé net.
    total = max(shots_dur + CARD_HOLD, audio_dur + 0.4)

    # mots recalés sur la nouvelle timeline
    words, cursor = [], 0.0
    for a, b in audio_keep:
        for t, s, e in SRC_WORDS:
            if a <= (s + e) / 2 < b:
                words.append((t, cursor + s - a, cursor + e - a))
        cursor += b - a
    write_ass(words, f"subs_{tag}.ass")

    # audio : on tait le concurrent sur la source, on greffe « Talyss » à sa
    # place, PUIS on découpe. Le mixage doit précéder la découpe pour que les
    # deux versions héritent du mot.
    # asplit est nécessaire : un flux filtré ne se consomme qu'une fois, et il
    # faut le relire autant de fois qu'il y a de segments à extraire.
    n = len(audio_keep)
    mute = f"volume=enable='between(t,{MUTE[0]},{MUTE[1]})':volume=0"
    agraph = (
        f"[0:a]{mute}[muet];"
        f"[1:a]aformat=channel_layouts=stereo,"
        f"adelay={int(WORD_AT * 1000)}|{int(WORD_AT * 1000)}[mot];"
        f"[muet][mot]amix=inputs=2:normalize=0[mix];"          # normalize=0 : sinon amix divise les niveaux par deux
        f"[mix]asplit={n}" + "".join(f"[m{i}]" for i in range(n)) + ";"
        + "".join(f"[m{i}]atrim=start={s}:end={e},asetpts=N/SR/TB[a{i}];"
                  for i, (s, e) in enumerate(audio_keep))
        + "".join(f"[a{i}]" for i in range(n))
        + f"concat=n={n}:v=0:a=1,apad=whole_dur={total:.3f}[out]")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", SRC, "-i", WORD,
                    "-filter_complex", agraph, "-map", "[out]",
                    "-ar", "48000", "-ac", "2", f"a_{tag}.wav"], check=True)

    # image
    vgraph = ("[0:v]split=%d" % len(shots)
              + "".join(f"[p{i}]" for i in range(len(shots))) + ";"
              + "".join(f"[p{i}]trim=start={s}:end={e},setpts=N/FRAME_RATE/TB[v{i}];"
                        for i, (s, e) in enumerate(shots))
              + "".join(f"[v{i}]" for i in range(len(shots)))
              + f"concat=n={len(shots)}:v=1:a=0[cut]")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", SRC,
                    "-filter_complex", vgraph, "-map", "[cut]", "-an",
                    "-c:v", "libx264", "-crf", "16", "-preset", "fast",
                    f"cut_{tag}.mp4"], check=True)

    subprocess.run([
        "ffmpeg", "-y", "-v", "error",
        "-i", f"cut_{tag}.mp4", "-i", f"a_{tag}.wav",
        "-loop", "1", "-framerate", "30", "-t", f"{total:.3f}", "-i", "plate.png",
        "-loop", "1", "-framerate", "30", "-t", f"{total:.3f}", "-i", CARD,
        "-filter_complex",
        f"[0:v][2:v]overlay={PLATE_X}:{PLATE_Y}:enable='lt(t,{shots_dur:.3f})'[pl];"
        f"[pl]ass=subs_{tag}.ass[sub];"
        f"[sub][3:v]overlay=0:0:enable='gte(t,{shots_dur:.3f})',format=yuv420p[v]",
        "-map", "[v]", "-map", "1:a", "-t", f"{total:.3f}",
        "-c:v", "libx264", "-crf", "18", "-preset", "medium",
        "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2",
        "-movflags", "+faststart", f"talyss-{tag}.mp4"], check=True)
    print(f"  -> talyss-{tag}.mp4  ({total:.2f}s, {len(shots)} plan(s))")


# ------------------------------------------------------------------ version A
print("Version A — montage d'origine")
build("A", shots=[(0.0, 35.50)], audio_keep=[(0.0, 35.50)])

# ------------------------------------------------------------------ version B
# Démarre après l'accroche qui s'adresse au corps du spectateur (politique Meta
# « attributs personnels »), sur « crème, râpe, pierre ponce… ».
print("Version B — remontage ~20 s")
# Chaque segment audio est borné sur des mots entiers, pour ne pas traîner un
# fragment de la phrase voisine (« …rien. Et là, » au lieu de « …rien. »).
B_AUDIO = [
    (8.85, 12.62),    # crème, râpe, pierre, ponce, j'ai tout testé, résultat, rien.
    (16.75, 20.35),   # Puis j'ai testé Talyss, franchement, deux minutes, zéro galère,
    (20.38, 22.68),   # tu passes, la corne disparaît, résultat.
    (22.72, 25.00),   # T'as le talon ultra lisse et effet spa pédicure,
    (26.60, 29.48),   # et avec les 60 disques inclus, je suis large tout l'été.
    (33.38, 35.42),   # clique, essaye et reviens me dire merci.
]
# Chaque plan tient dans une seule scène du rush ; la somme colle exactement à
# celle des segments audio (16,87 s), pour que l'image ne devance pas la voix.
B_SHOTS = [
    (9.20, 9.87),     # N&B : lame sur le talon
    (11.30, 12.50),   # N&B : râpe électrique concurrente
    (13.00, 13.75),   # N&B : outils dans la boîte
    (14.60, 15.75),   # N&B : pierre ponce
    (17.15, 18.60),   # UGC : elle présente l'appareil
    (19.45, 20.20),   # appareil sur le talon
    (20.30, 21.70),   # poussière qui vole
    (22.20, 23.55),   # gros plan corne qui part
    (23.70, 24.65),   # talon net
    (29.60, 31.88),   # pied lisse
    (26.65, 28.05),   # bandeau « 60 disques »
    (24.75, 26.23),   # effet spa, posée sur le canapé
    (32.60, 34.64),   # sandales, résultat lifestyle
]
build("B", shots=B_SHOTS, audio_keep=B_AUDIO)
