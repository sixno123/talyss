#!/usr/bin/env python3
"""Fabrique le mot « Talyss » greffé là où le nom du concurrent a été coupé.

Source : la voix off Talyss de la créa 47 s, qui prononce déjà la marque
(27,34-27,88 s dans vo_final2.wav).

Deux réglages ont été trouvés à l'oreille de l'ASR, pas au calcul :

1. **Début de l'extraction.** Partir 0,04 s plus tôt happait le /k/ final
   d'« électrique » ; l'ASR entendait alors « Octalis », « Kitalis ». Démarrer
   à 27,34 s supprime cette consonne parasite.

2. **Ratio de transposition = 1,15.** Caler la hauteur au plus près de la
   créatrice demandait 1,44x, ce qui rendait le mot inintelligible
   (« Pétalice »). À 1,15 l'ASR relit « Thalys » — l'orthographe exacte qu'elle
   produit sur la vraie voix off Talyss. Pour une marque, être compris prime
   sur être à la bonne hauteur.
"""
import subprocess
import numpy as np

SRC = "/root/.claude/uploads/b6b4b174-cc8a-5915-a346-1947ec943bb5/4a78dbe0-ad2237375970125334hd.mp4"
VO = ("/tmp/claude-0/-home-user-talyss/b6b4b174-cc8a-5915-a346-1947ec943bb5"
      "/scratchpad/work/vo_final2.wav")
CUT = (27.34, 27.88)            # « Talyss » sans le /k/ d'« électrique »
NEIGHBOUR = (16.80, 17.62)      # « Puis j'ai testé », pour le niveau
RATIO = 1.15


def pcm(path, *args):
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", *args, "-i", path,
         "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
        capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768


def rms(x):
    return float(np.sqrt((x ** 2).mean()))


subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(CUT[0]), "-to",
                str(CUT[1]), "-i", VO, "-ac", "1", "-ar", "48000",
                "w_raw.wav"], check=True)
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", "w_raw.wav", "-af",
                f"rubberband=pitch={RATIO}:formant=preserved",
                "-ar", "48000", "-ac", "1", "_lvl.wav"], check=True)

target = rms(pcm(SRC, "-ss", str(NEIGHBOUR[0]), "-to", str(NEIGHBOUR[1])))
gain = target / max(rms(pcm("_lvl.wav")), 1e-6)

subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", "_lvl.wav", "-af",
                f"volume={gain:.3f},afade=t=in:d=0.02,afade=t=out:st=0.515:d=0.025",
                "-ar", "48000", "-ac", "1", "w_talyss.wav"], check=True)

out = pcm("w_talyss.wav")
print(f"w_talyss.wav : {len(out)/16000:.2f}s, RMS {rms(out):.4f} "
      f"(voisin {target:.4f}), gain {gain:.2f}x, ratio {RATIO}")
