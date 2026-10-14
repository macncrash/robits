"""Render a screencast of the parts tools as an MP4 (partsel-demo.mp4 next to this file).

Every command shown is run for real when the video is made, so the output on screen is the tools' actual
output at that moment. Needs Pillow and ffmpeg; run from anywhere:

    python3 tools/partsel/demo/make_video.py
"""
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).with_name("partsel-demo.mp4")
W, H, FPS = 1600, 900, 30
FONT = "/System/Library/Fonts/Menlo.ttc"
SIZE, LINE = 18, 25
BG, FG, DIM, ACCENT, CAPTION_BG = "#0f1218", "#d8dee9", "#7a8494", "#7fc8f8", "#1b2030"
VERDICT = {"PASS": "#8fd694", "FAIL": "#f28b82", "CHECK": "#f6d36b", "NO": "#f28b82"}
CAPTION_H = 110
ALIAS = "python3 tools/partsel/partsel.py"

font = ImageFont.truetype(FONT, SIZE)
bold = ImageFont.truetype(FONT, SIZE, index=1)
title_font = ImageFont.truetype(FONT, 40, index=1)
caption_font = ImageFont.truetype(FONT, 24, index=1)
sub_font = ImageFont.truetype(FONT, 18)
CHAR_W = font.getlength("M")
COLS = int((W - 60) / CHAR_W)
ROWS = (H - CAPTION_H - 50) // LINE

# (caption, sub-caption, command shown, seconds to hold the output)
SCENES = [
    ("1. Requirements live with the project",
     "What the actuator needs from a motor: the operating point, then one check per requirement.",
     "head -24 unknown-machine/requirements/motor.toml", 5),
    ("2. One card per orderable part",
     "Numbers copied exactly from the vendor's catalog. Every value names its source and page.",
     "sed -n '1,6p;14,34p' parts/frameless-motors/kollmorgen-kbm-17h01-b.toml | cut -c1-140", 6),
    ("3. Run the selector",
     "PASS = every hard check met. FAIL = one isn't. CHECK = the card is missing a value, so it can't be confirmed.",
     "partsel unknown-machine/requirements/motor.toml --brief", 6),
    ("4. Ask why, with sources",
     "--detail explains each failure and traces every number back to its page in the catalog.",
     "partsel unknown-machine/requirements/motor.toml --detail | sed -n '/^## KBM-17H01-A00/,/mass_kg/p'", 6),
    ("5. What if we used a 48 V drive?",
     "--set overrides the operating point for one run. Nothing in the 85 mm frame works at 48 V and 3000 rpm.",
     "partsel unknown-machine/requirements/motor.toml --brief --set bus_vdc=48", 6),
    ("6. What if the motor spun faster?",
     "At 4500 rpm the B winding still fits the 325 V bus; the A winding needs even more voltage.",
     "partsel unknown-machine/requirements/motor.toml --brief --set speed_rpm=4500", 5),
    ("7. Feed the pick into the hand checks",
     "KBM-17H01-B00 numbers in analysis/hand_calcs.py: copper loss, housing temperature, bond shear.",
     "python3 unknown-machine/analysis/hand_calcs.py | tail -5", 7),
]

TITLE = ("partsel: picking bought parts fast",
         ["Unknown-machine joint actuator: choosing the frameless motor",
          "Plain Python 3.11+, no installs.  Part cards in parts/, requirements next to the project.",
          "In this video, partsel = python3 tools/partsel/partsel.py"])
OUTRO = ("Result: Kollmorgen KBM-17H01-B00 (US), 240 Vac drive",
         ["STEVE studies, housing bolted into the pedestal (clamp band removed):",
          "  40 W, still air, base insulated       69–73 °C on the case (winding rated 155 °C)",
          "  40 W, base on a 35 °C structure       35–44 °C; 28 W leave through the base",
          "  ring + bearing loads, 4 screws        9.8 MPa",
          "  first natural frequency, on pedestal  1.82 kHz (no internal parts)",
          "",
          "Bolted to metal, the motor's full 2.06 N·m continuous rating fits (about 55 °C case).",
          "Next: Kollmorgen's 3D model for the stator bore and end turns, then the shop package."])


def run(cmd):
    real = cmd.replace("partsel ", ALIAS + " ", 1) if cmd.startswith("partsel ") else cmd
    real = real.replace("| partsel ", "| " + ALIAS + " ")
    out = subprocess.run(["bash", "-c", real], cwd=ROOT, capture_output=True, text=True)
    return (out.stdout + out.stderr).rstrip("\n").splitlines()


def clip(line):
    return line if len(line) <= COLS else line[:COLS - 1] + "…"


def colour_of(line):
    for word, colour in VERDICT.items():
        if f" {word} " in f" {line} " or f"**{word}**" in line or line.endswith(f": {word}"):
            return colour
    if line.startswith("#") or line.startswith("##"):
        return ACCENT
    return FG


def frame(caption, sub, lines, cursor=False):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, CAPTION_H], fill=CAPTION_BG)
    d.text((30, 22), caption, font=caption_font, fill=ACCENT)
    d.text((30, 64), sub, font=sub_font, fill=DIM)
    y = CAPTION_H + 25
    for i, line in enumerate(lines[-ROWS:]):
        if line.startswith("$ "):
            d.text((30, y), "$", font=bold, fill="#8fd694")
            d.text((30 + 2 * CHAR_W, y), clip(line[2:]), font=bold, fill=FG)
        else:
            d.text((30, y), clip(line), font=font, fill=colour_of(line))
        y += LINE
    if cursor:
        last = lines[-ROWS:][-1] if lines else "$ "
        x = 30 + len(clip(last)) * CHAR_W
        d.rectangle([x, y - LINE + 3, x + CHAR_W - 2, y - 3], fill=FG)
    return img


def card(title, lines):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.text((80, 200), title, font=title_font, fill=ACCENT)
    for i, line in enumerate(lines):
        d.text((80, 290 + i * 36), line, font=caption_font if i == 0 else sub_font,
               fill=FG if i == 0 else DIM if not line.startswith("  ") else FG)
    return img


class Video:
    def __init__(self, path):
        self.p = subprocess.Popen(
            ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
             "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
             "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(path)], stdin=subprocess.PIPE)

    def hold(self, img, seconds):
        data = img.tobytes()
        for _ in range(max(1, round(seconds * FPS))):
            self.p.stdin.write(data)

    def close(self):
        self.p.stdin.close()
        return self.p.wait()


def main():
    v = Video(OUT)
    v.hold(card(*TITLE), 4)
    screen = []
    for caption, sub, cmd, hold in SCENES:
        screen = []                                       # each scene starts on a clear screen
        typed = "$ "
        for ch in cmd:                                   # type the command, two characters per frame
            typed += ch
            if len(typed) % 2 == 0:
                v.hold(frame(caption, sub, screen + [typed], cursor=True), 1 / FPS)
        screen.append(typed)
        v.hold(frame(caption, sub, screen, cursor=False), 0.4)
        output = run(cmd)
        for k in range(0, len(output), 3):              # output scrolls in, three lines per frame
            v.hold(frame(caption, sub, screen + output[:k + 3]), 1 / FPS)
        screen += output
        v.hold(frame(caption, sub, screen), hold)
    v.hold(card(*OUTRO), 8)
    code = v.close()
    if code:
        sys.exit(f"ffmpeg failed ({code})")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
