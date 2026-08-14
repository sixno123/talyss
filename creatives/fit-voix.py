#!/usr/bin/env python3
"""Fit the generated voiceover to the video length by capping inter-phrase
silences instead of speeding up the whole read."""
import subprocess, sys

SRC = "vo_raw.mp3"
OUT = "vo_tight.wav"
CAP = 0.30          # max length kept for any internal pause
AUDIO_END = 52.3561  # start of the trailing silence -> hard stop

# (start, end) of every detected silence, from ffmpeg silencedetect -35dB/0.20s
SIL = [
    (2.74778, 3.40746), (6.01431, 6.38236), (8.61512, 9.32236),
    (10.2109, 10.5162), (11.1837, 11.5781), (12.5832, 13.0787),
    (16.4617, 16.9077), (18.7404, 19.0552), (20.8442, 21.2466),
    (22.0916, 22.3809), (23.2216, 23.7217), (26.1924, 26.6959),
    (27.1145, 27.5934), (30.316, 30.7486), (33.9632, 34.4435),
    (35.8557, 36.0728), (36.097, 36.4063), (37.0278, 37.8181),
    (38.7508, 39.0608), (40.3707, 40.5837), (40.9473, 41.7847),
    (42.328, 43.0301), (45.3325, 45.8742), (47.3735, 47.8053),
    (48.581, 49.2577), (50.1052, 50.6926),
]

# Build keep-intervals: all speech, plus each pause truncated to CAP.
keeps, cursor = [], 0.0
for s_start, s_end in SIL:
    keeps.append((cursor, min(s_start + CAP, s_end)))
    cursor = s_end
keeps.append((cursor, AUDIO_END))          # tail speech, trailing silence dropped

kept = sum(e - s for s, e in keeps)
print(f"segments={len(keeps)}  kept={kept:.3f}s  (was {AUDIO_END:.3f}s)")

# atrim each keep-interval, then concat
parts, labels = [], []
for i, (s, e) in enumerate(keeps):
    parts.append(f"[0:a]atrim=start={s:.5f}:end={e:.5f},asetpts=N/SR/TB[a{i}]")
    labels.append(f"[a{i}]")
graph = ";".join(parts) + ";" + "".join(labels) + f"concat=n={len(keeps)}:v=0:a=1[out]"

subprocess.run(
    ["ffmpeg", "-y", "-v", "error", "-i", SRC,
     "-filter_complex", graph, "-map", "[out]",
     "-ar", "48000", "-ac", "1", OUT],
    check=True,
)
dur = float(subprocess.run(
    ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", OUT],
    capture_output=True, text=True, check=True).stdout.strip())
print(f"tightened duration = {dur:.3f}s")
