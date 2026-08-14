#!/usr/bin/env python3
"""Word-level timings for the finished voiceover, so the new subtitles land
exactly on the spoken words."""
import json
from faster_whisper import WhisperModel

model = WhisperModel("small", device="cpu", compute_type="int8")
segments, info = model.transcribe(
    "vo_final2.wav", language="fr", word_timestamps=True,
    vad_filter=False, beam_size=5,
)

words = []
for seg in segments:
    for w in seg.words:
        words.append({"w": w.word.strip(), "s": round(w.start, 3), "e": round(w.end, 3)})

with open("words.json", "w", encoding="utf-8") as f:
    json.dump(words, f, ensure_ascii=False, indent=1)

print(f"{len(words)} words, last ends at {words[-1]['e']:.2f}s")
print(" ".join(w["w"] for w in words))
