#!/usr/bin/env python3
"""Choisit le ratio de transposition du mot greffé sur l'INTELLIGIBILITÉ, pas
sur la hauteur.

Caler la hauteur au plus près (1,44x) rendait le mot bouillie : l'ASR entendait
« Pétalice ». Ce qui compte pour une marque, c'est qu'on la comprenne. On
greffe donc chaque candidat dans la vraie phrase et on regarde ce que l'ASR
en fait.
"""
import subprocess
from faster_whisper import WhisperModel

SRC = "/root/.claude/uploads/b6b4b174-cc8a-5915-a346-1947ec943bb5/4a78dbe0-ad2237375970125334hd.mp4"
MUTE = (17.58, 18.24)
WORD_AT = 17.60
RATIOS = [1.00, 1.15, 1.30]

model = WhisperModel("small", device="cpu", compute_type="int8")

for r in RATIOS:
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", "w_raw.wav", "-af",
         f"rubberband=pitch={r}:formant=preserved,volume=1.58,"
         f"afade=t=in:d=0.02,afade=t=out:st=0.55:d=0.05",
         "-ar", "48000", "-ac", "1", f"_w{r}.wav"], check=True)
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", SRC, "-i", f"_w{r}.wav",
         "-filter_complex",
         f"[0:a]volume=enable='between(t,{MUTE[0]},{MUTE[1]})':volume=0[m];"
         f"[1:a]aformat=channel_layouts=stereo,"
         f"adelay={int(WORD_AT*1000)}|{int(WORD_AT*1000)}[w];"
         f"[m][w]amix=inputs=2:normalize=0,atrim=start=16.6:end=19.4,"
         f"asetpts=N/SR/TB[out]",
         "-map", "[out]", "-ar", "48000", "-ac", "2", f"_ctx{r}.wav"], check=True)
    segs, _ = model.transcribe(f"_ctx{r}.wav", language="fr",
                               vad_filter=False, beam_size=5)
    txt = " ".join(s.text.strip() for s in segs)
    print(f"  ratio {r:.2f} -> « {txt} »")
