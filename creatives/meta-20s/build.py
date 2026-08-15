#!/usr/bin/env python3
"""Créa Meta 20 s : remontage des rushes + voix off recoupée au mot près.

La voix est découpée dans la bande existante en s'appuyant sur words.json
(144 mots horodatés), donc les sous-titres se recalculent sans repasser par
une transcription.
"""
import json, subprocess, unicodedata, re
from PIL import Image, ImageDraw, ImageFont

W, H = 720, 1280
SRC = "/root/.claude/uploads/b6b4b174-cc8a-5915-a346-1947ec943bb5/5749cb0a-adsansson.mp4"
WORK = "/tmp/claude-0/-home-user-talyss/b6b4b174-cc8a-5915-a346-1947ec943bb5/scratchpad/work"

# Pastille noire arrondie, pas une barre pleine largeur : elle doit couvrir
# l'ancien texte incrusté (x 142-581, y 960-1090) et rien de plus. Détachée des
# bords et à coins arrondis, elle se lit comme un cartouche de sous-titre plutôt
# que comme un bandeau posé sur l'image.
PLATE_X, PLATE_Y = 45, 936           # 45-675 x 936-1104
PLATE_W, PLATE_H = 630, 168
PLATE_R = 32                         # rayon des coins
CAP_Y = 998                          # bloc de texte ~963-1033, centré dans la pastille
FONT_PX = 54
MAX_TEXT_W = 560                     # tient dans la pastille (630 px) avec marge
GOLD, WHITE = "&H1BA9DE&", "&H00FFFFFF&"
KEYWORDS = ["Talyss", "sans douleur", "doux et lisses", "peau morte", "râpe électrique"]

# --- voix : (début, fin) dans vo_final2.wav + le texte réellement prononcé -------
# L'ASR écrit "rap"/"Thalys"/"sa hérite" ; on réaffiche l'orthographe correcte.
VO = [
    (2.90,  7.95, "Avant, c'était pédicure toutes les 3 semaines, parce que mes "
                  "talons étaient une catastrophe."),
    (18.26, 21.60, "râpes manuelles, soit ça irrite, soit ça ne fait rien."),
    (24.40, 27.90, "Et puis, une amie m'a fait découvrir la râpe électrique Talyss."),
    (31.62, 34.40, "elle enlève toute la peau morte, sans douleur."),
    # « _ » colle deux mots en un seul jeton : la ponctuation française détachée
    # (« Résultat : ») compte pour un mot côté audio.
    (37.84, 41.05, "Résultat_: des pieds incroyablement doux et lisses."),
    (43.96, 46.80, "Les stocks partent vite, alors commandez maintenant sur Talyss_!"),
]

# --- image : (début, fin) dans le rush, dans le nouvel ordre ---------------------
# Chaque plan tient dans une seule scène du rush (coupes connues), pour ne jamais
# démarrer ou finir sur une transition d'origine.
SHOTS = [
    (0.35, 2.75),    # mains gantées qui liment — lecture « institut »
    (4.40, 5.75),    # talon sec en tong
    (5.95, 7.25),    # plante craquelée
    (15.50, 16.35),  # N&B : crème / râpe
    (17.20, 18.50),  # N&B : lame sur le talon
    (18.70, 19.35),  # N&B : râpe électrique concurrente
    (19.50, 20.00),  # N&B : outils dans la boîte
    (20.15, 21.50),  # UGC : elle présente l'appareil
    (8.60, 10.75),   # appareil en action, poussière
    (29.60, 31.30),  # appareil rose, poussière qui vole
    (25.50, 26.58),  # appareil sur pied humide
    (31.50, 33.00),  # talon lisse
    (33.15, 34.86),  # deux pieds lisses sur serviette
    (40.60, 41.92),  # sandales portées — résultat lifestyle
]
CARD_HOLD = 2.7      # durée de la carte de fin après les plans


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


# ---------------------------------------------------------------- mots -> nouvelle timeline
raw = json.load(open(f"{WORK}/words.json", encoding="utf-8"))
asr = []
for it in raw:                                   # recoller "c" + "'était"
    if it["w"].startswith("'") and asr:
        asr[-1] = {"w": asr[-1]["w"] + it["w"], "s": asr[-1]["s"], "e": it["e"]}
    else:
        asr.append(dict(it))

words, cursor = [], 0.0                          # (texte affiché, début, fin) recalés
for seg_start, seg_end, text in VO:
    # sélection sur le milieu du mot : un mot qui démarre juste avant la borne
    # de coupe (« Elle » à 27,78) ne doit pas être happé par le segment
    picked = [a for a in asr if seg_start <= (a["s"] + a["e"]) / 2 < seg_end]
    shown = [t.replace("_", " ") for t in text.split()]
    assert len(picked) == len(shown), (
        f"{len(picked)} mots audio vs {len(shown)} affichés dans « {text[:40]}… »")
    for a, disp in zip(picked, shown):
        words.append((disp, cursor + a["s"] - seg_start, cursor + a["e"] - seg_start))
    cursor += seg_end - seg_start

vo_dur = cursor
print(f"voix : {len(words)} mots, {vo_dur:.2f} s")

# mots-clés repérés sur toute la suite, pas carton par carton
shown_norm = [norm(w[0]) for w in words]
is_kw = [False] * len(words)
for phrase in KEYWORDS:
    toks = [norm(x) for x in phrase.split()]
    for i in range(len(shown_norm) - len(toks) + 1):
        if shown_norm[i:i + len(toks)] == toks:
            for k in range(i, i + len(toks)):
                is_kw[k] = True

# ---------------------------------------------------------------- durées
shots_dur = sum(e - s for s, e in SHOTS)
total = shots_dur + CARD_HOLD
print(f"plans : {len(SHOTS)}, {shots_dur:.2f} s -> total {total:.2f} s")

# ---------------------------------------------------------------- audio
parts = "".join(f"[0:a]atrim=start={s}:end={e},asetpts=N/SR/TB[a{i}];"
                for i, (s, e, _) in enumerate(VO))
# apad dans le graphe (-af est exclu ici) et borné, sinon le flux serait infini
graph = parts + "".join(f"[a{i}]" for i in range(len(VO))) + \
    f"concat=n={len(VO)}:v=0:a=1,apad=whole_dur={total:.3f}[out]"
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", f"{WORK}/vo_final2.wav",
                "-filter_complex", graph, "-map", "[out]",
                "-ar", "48000", "-ac", "2", "vo20.wav"], check=True)

# ---------------------------------------------------------------- vidéo
vparts = "".join(f"[0:v]trim=start={s}:end={e},setpts=N/FRAME_RATE/TB[v{i}];"
                 for i, (s, e) in enumerate(SHOTS))
vgraph = vparts + "".join(f"[v{i}]" for i in range(len(SHOTS))) + \
    f"concat=n={len(SHOTS)}:v=1:a=0[cut]"
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", SRC,
                "-filter_complex", vgraph, "-map", "[cut]",
                "-an", "-c:v", "libx264", "-crf", "16", "-preset", "fast",
                "cut.mp4"], check=True)

# ---------------------------------------------------------------- sous-titres
# Cartons de 2 à 4 mots, un événement ASS par mot (karaoké).
font = ImageFont.truetype(
    subprocess.run(["fc-match", "-f", "%{file}", "Montserrat:weight=extrabold"],
                   capture_output=True, text=True).stdout.strip(), FONT_PX)

def text_w(t):
    b = font.getbbox(t)
    return b[2] - b[0]

cards, cur = [], []
for i, (w, s, e) in enumerate(words):
    # compter les mots ne suffit pas : un carton de 4 mots longs déborde du cadre
    if cur and text_w(" ".join(words[k][0] for k in cur + [i])) > MAX_TEXT_W:
        cards.append(cur)
        cur = []
    cur.append(i)
    # une fin de phrase ferme toujours le carton : sinon la fin d'une réplique et
    # le début de la suivante se retrouvent sur la même ligne
    if w[-1] in ".!?" or (len(cur) >= 3 and w[-1] in ",;:") or len(cur) >= 4:
        cards.append(cur)
        cur = []
if cur:
    cards[-1].extend(cur) if cards else cards.append(cur)

head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Montserrat ExtraBold,{FONT_PX},&H00FFFFFF,&H00101010,&H80000000,0,0,0,0,100,100,0.4,0,1,2.6,0,5,40,40,40,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

events = 0
with open("subs20.ass", "w", encoding="utf-8") as f:
    f.write(head)
    for ci, ids in enumerate(cards):
        c_start = words[ids[0]][1]
        c_end = (words[cards[ci + 1][0]][1] if ci + 1 < len(cards)
                 else min(words[ids[-1]][2] + 0.45, vo_dur))
        bounds = [c_start]
        for j in range(1, len(ids)):
            bounds.append(min(max(words[ids[j]][1], bounds[-1]), c_end))
        bounds.append(c_end)
        live = [j for j in range(len(ids)) if bounds[j + 1] - bounds[j] > 0.001]
        for pos, j in enumerate(live):
            body = " ".join(
                f"{{\\c{GOLD}}}{words[k][0]}{{\\c{WHITE}}}"
                if (n == j or (is_kw[k] and n < j)) else words[k][0]
                for n, k in enumerate(ids))
            fin = 60 if pos == 0 else 0
            fout = 60 if pos == len(live) - 1 else 0
            f.write(f"Dialogue: 0,{ts(bounds[j])},{ts(bounds[j + 1])},Cap,,0,0,0,,"
                    f"{{\\pos({W // 2},{CAP_Y})\\fad({fin},{fout})}}{body}\n")
            events += 1
print(f"{len(cards)} cartons, {events} événements ASS")

# ---------------------------------------------------------------- pastille
# Dessinée 4× puis réduite : PIL crénelle les coins arrondis, le sur-échantillonnage
# les lisse et évite l'escalier visible sur un aplat noir.
S = 4
plate = Image.new("RGBA", (PLATE_W * S, PLATE_H * S), (0, 0, 0, 0))
ImageDraw.Draw(plate).rounded_rectangle(
    [0, 0, PLATE_W * S - 1, PLATE_H * S - 1], radius=PLATE_R * S, fill=(0, 0, 0, 255))
plate.resize((PLATE_W, PLATE_H), Image.LANCZOS).save("plate.png")
assert PLATE_Y <= 960 and PLATE_Y + PLATE_H >= 1090, "la pastille ne couvre pas l'ancien texte"
assert PLATE_X <= 142 and PLATE_X + PLATE_W >= 581, "pastille trop étroite"

# ---------------------------------------------------------------- rendu final
subprocess.run([
    "ffmpeg", "-y", "-v", "error",
    "-i", "cut.mp4", "-i", "vo20.wav",
    "-loop", "1", "-framerate", "30", "-t", f"{total:.3f}", "-i", "plate.png",
    "-loop", "1", "-framerate", "30", "-t", f"{total:.3f}",
    "-i", f"{WORK}/endcard.png",
    "-filter_complex",
    f"[0:v][2:v]overlay={PLATE_X}:{PLATE_Y}:enable='lt(t,{shots_dur:.3f})'[plated];"
    f"[plated]ass=subs20.ass[sub];"
    f"[sub][3:v]overlay=0:0:enable='gte(t,{shots_dur:.3f})',format=yuv420p[v]",
    "-map", "[v]", "-map", "1:a",
    "-t", f"{total:.3f}",
    "-c:v", "libx264", "-crf", "18", "-preset", "medium",
    "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2",
    "-movflags", "+faststart", "talyss-meta-20s.mp4"], check=True)
print("-> talyss-meta-20s.mp4")
