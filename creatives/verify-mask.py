#!/usr/bin/env python3
"""Gate for the frosted band: prove the burned-in captions are gone.

Profiles the mask WITHOUT the new subtitles — they are white and sit in the same
place, so rendering them would count them as leftovers.
"""
import subprocess, numpy as np

SRC = "/root/.claude/uploads/b6b4b174-cc8a-5915-a346-1947ec943bb5/5749cb0a-adsansson.mp4"
FPS, END = 4, 43.6
OLD_TOP, OLD_BOT = 960, 1090          # what bbox.py measured on the source

BAND = ("crop=720:240:0:905,gblur=sigma=34,eq=brightness=-0.20:saturation=0.62,"
        "format=rgb24")


def frames(args, graph):
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-t", str(END), "-i", SRC] + args +
        ["-filter_complex", graph, "-map", "[v]",
         "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
        capture_output=True, check=True).stdout
    n = 720 * (OLD_BOT - OLD_TOP) * 3
    return np.frombuffer(raw, np.uint8).reshape(-1, OLD_BOT - OLD_TOP, 720, 3)


crop_old = f"crop=720:{OLD_BOT - OLD_TOP}:0:{OLD_TOP},fps={FPS}"

before = frames([], f"[0:v]{crop_old}[v]")
after = frames(
    ["-loop", "1", "-framerate", "30", "-t", str(END), "-i", "feather.png"],
    f"[0:v]split[b][p];[p]{BAND}[bandrgb];[1:v]format=gray[m];"
    f"[bandrgb][m]alphamerge[band];[b][band]overlay=0:905,{crop_old}[v]")

b = (before >= 246).all(axis=3)
a = (after >= 246).all(axis=3)
b_cnt, a_cnt = int(b.sum()), int(a.sum())

print(f"{len(before)} frames, old caption box y {OLD_TOP}-{OLD_BOT}")
print(f"  source : {b_cnt:,} near-white px")
print(f"  masked : {a_cnt:,}  ({100 * a_cnt / max(b_cnt, 1):.3f}% left)")
rows = a.sum(axis=(0, 2))
print(f"  worst row: y={OLD_TOP + int(rows.argmax())} -> {int(rows.max())} px "
      f"across {len(after)} frames")
