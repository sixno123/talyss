#!/usr/bin/env python3
"""Locate the burned-in caption band by profiling near-white pixels."""
import subprocess, numpy as np

SRC = "/root/.claude/uploads/b6b4b174-cc8a-5915-a346-1947ec943bb5/5749cb0a-adsansson.mp4"
Y0, H, W = 780, 480, 720
FPS = 4
END = 43.6   # stop before the end card, which gets replaced anyway

raw = subprocess.run(
    ["ffmpeg", "-v", "error", "-t", str(END), "-i", SRC,
     "-vf", f"crop={W}:{H}:0:{Y0},fps={FPS}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
    capture_output=True, check=True).stdout

frames = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
print(f"{len(frames)} frames analysed")

# Caption glyphs are pure white; most real content is not.
white = (frames >= 246).all(axis=3)

row_profile = white.sum(axis=(0, 2))
col_profile = white.sum(axis=(0, 1))

# Rows/cols carrying at least 4% of the peak count are part of the text block.
r_thr, c_thr = row_profile.max() * 0.04, col_profile.max() * 0.04
rows = np.where(row_profile > r_thr)[0]
cols = np.where(col_profile > c_thr)[0]

print(f"text rows  : y {Y0 + rows[0]} .. {Y0 + rows[-1]}  (height {rows[-1]-rows[0]+1})")
print(f"text cols  : x {cols[0]} .. {cols[-1]}  (width {cols[-1]-cols[0]+1})")

print("\nrow profile (every 8px, absolute y):")
for i in range(0, H, 8):
    bar = "#" * int(40 * row_profile[i] / max(row_profile.max(), 1))
    print(f"  y={Y0+i:4d} {row_profile[i]:7d} {bar}")

# How many frames actually show a caption at all?
per_frame = white[:, rows[0]:rows[-1]+1, :].sum(axis=(1, 2))
print(f"\nframes with caption pixels: {(per_frame > 200).sum()}/{len(frames)}")
