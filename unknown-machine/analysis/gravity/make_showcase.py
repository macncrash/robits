"""Join the Gravity sim render and the animated chart into one video to show people (Pillow + ffmpeg).

    python3 unknown-machine/analysis/gravity/make_showcase.py <gravity render .mp4>

Copies the render to actuator-envelope-sim.mp4, puts a title, legend and caption over it, then appends
../motor-curves-chart.mp4 (python3 unknown-machine/analysis/motor_curves.py --render) -> ../motor-showcase.mp4.
"""
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import motor_curves as mc  # noqa: E402

W, H = 1920, 1080
FONT = "/System/Library/Fonts/Helvetica.ttc"


def overlay(path):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    f = lambda s, b=False: ImageFont.truetype(FONT, s, index=1 if b else 0)
    d.rectangle([0, 0, W, 150], fill=(15, 18, 24, 215))
    d.text((60, 30), "30,000 simulated actuators, each spinning up against its own load", font=f(40, True),
           fill="#f0efec")
    d.text((60, 90), f"Kollmorgen KBM-17H01-B00 + {mc.RATIO:.0f}:1 planetary on a {mc.BUS:.0f} V bus. Each dot is one"
           " actuator: right = output speed, up = output torque, depth = power. Simulated in Gravity.",
           font=f(24), fill="#8a8f98")
    d.rectangle([0, H - 120, W, H], fill=(15, 18, 24, 215))
    x = 60
    for key, label, _ in mc.LIMITS:
        d.rounded_rectangle([x, H - 74, x + 32, H - 60], radius=4, fill=mc.SERIES[key])
        d.text((x + 44, H - 82), label, font=f(26), fill="#c3c2b7")
        x += 44 + d.textlength(label, font=f(26)) + 60
    d.text((W - 60, H - 82), "Flat top: current limit.  Roll-off: back-EMF reaches the bus.", font=f(24),
           fill="#8a8f98", anchor="ra")
    img.save(path)


def main():
    render = Path(sys.argv[1])
    sim = HERE / "actuator-envelope-sim.mp4"
    shutil.copyfile(render, sim)
    ov = HERE / "overlay.png"
    overlay(ov)
    chart = HERE.parent / "motor-curves-chart.mp4"
    out = HERE.parent / "motor-showcase.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(sim), "-i", str(ov), "-i", str(chart),
                    "-filter_complex",
                    "[0:v][1:v]overlay=0:0,format=yuv420p,setsar=1[a];[2:v]format=yuv420p,setsar=1[b];"
                    "[a][b]concat=n=2:v=1:a=0[v]",
                    "-map", "[v]", "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-movflags", "+faststart",
                    str(out)], check=True)
    ov.unlink()
    print(f"wrote {sim.relative_to(HERE.parent.parent)}, {out.relative_to(HERE.parent.parent)}")


if __name__ == "__main__":
    main()
