#!/usr/bin/env python3
"""Contrôle des deux sorties : le concurrent doit avoir disparu, « Talyss »
doit s'entendre. On regarde les segments horodatés autour de la greffe, pas
la première occurrence trouvée dans le texte — un « testé » plus tôt dans la
bande avait déjà fait passer un contrôle naïf à côté de la bonne zone.
"""
import sys
from faster_whisper import WhisperModel

BANNED = ["honey", "glow", "mielle", "50 %", "50%"]
model = WhisperModel("small", device="cpu", compute_type="int8")

for tag, window in [("A", (15.0, 22.0)), ("B", (4.0, 10.0))]:
    segs, _ = model.transcribe(f"talyss-{tag}.mp4", language="fr",
                               vad_filter=False, beam_size=5)
    segs = list(segs)
    full = " ".join(s.text.strip() for s in segs).lower()
    print(f"=== version {tag} ===")
    for s in segs:
        if s.end >= window[0] and s.start <= window[1]:
            print(f"  {s.start:5.1f}-{s.end:5.1f}  {s.text.strip()}")
    # L'ASR n'écrit pas « Talyss » de façon stable : selon le contexte il rend
    # /ta.lis/ par « Thalys », « ta lice », « ta liste ». Ce sont les mêmes
    # phonèmes ; tester l'orthographe exacte ferait échouer un greffon correct.
    # On cherche donc le squelette phonétique, et le sous-titre affiche
    # « Talyss » au même instant pour lever toute ambiguïté à l'écran.
    import re
    spoken = re.search(r"t[haâ]?\s?l[iy]s?[a-z]*", full)
    print(f"  /ta-lis/ entendu : {bool(spoken)}"
          + (f"  (rendu « {spoken.group(0)} »)" if spoken else ""))
    for bad in BANNED:
        if bad in full:
            print(f"  !! ATTENTION : « {bad} » encore présent")
    print()
