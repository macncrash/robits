"""Torque-speed and power-speed limits of the actuator at its output (KBM-17H01-B00 + 5:1 planetary, 325 V bus).

The same steady-state model as the Gravity sim (gravity/actuator_envelope.js): the drive gives
I(w) = min(I_limit, (V_avail - Ke w) / (sqrt(3) R_ph)), with V_avail = 0.95 V_bus / sqrt(2) line-line rms;
torque Kt I with catalog saturation above the continuous current; output = motor x ratio x gear efficiency.
Inductance, iron and friction losses and field weakening are left out (see the README's caveats).

    python3 unknown-machine/analysis/motor_curves.py            # numbers + motor-curves.csv
    python3 unknown-machine/analysis/motor_curves.py --render   # also motor-curves.png and motor-curves-chart.mp4
                                                                  # (Pillow + ffmpeg)
"""
import csv
import math
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
KT, KE_V_PER_KRPM, R_LL = 0.681, 41.2, 6.02          # catalog p. 20, winding B
I_CONT, I_PEAK, T_PEAK = 3.11, 10.9, 6.14             # A rms, A rms, N m (catalog p. 20)
BUS, RATIO, ETA = 325.0, 5.0, 0.97                    # V DC (240 Vac drive), 1 + 72/18, planetary efficiency (assumed)
I_DRIVE = 5.9                                         # A rms drive peak limit (4.0 N m, what the gears are sized for)
KE = KE_V_PER_KRPM * 60 / (2 * math.pi) / 1000        # V s/rad line-line rms
R_PH = R_LL / 2
V_AVAIL = 0.95 * BUS / math.sqrt(2)
SAT = 1 - T_PEAK / (KT * I_PEAK)                      # torque lost to saturation at the catalog peak current

LIMITS = [  # (key, label, current limit) in legend order
    ("cont", f"Continuous rating ({I_CONT} A)", I_CONT),
    ("drive", f"Drive peak limit ({I_DRIVE} A)", I_DRIVE),
    ("peak", f"Motor peak ({I_PEAK} A, catalog)", I_PEAK),
]


def motor_torque(i):
    s = SAT * (i - I_CONT) / (I_PEAK - I_CONT) if i > I_CONT else 0.0
    return KT * i * (1 - s)


def point(w_motor, i_limit):
    """Output torque (N m), output power (W), current (A), copper loss (W) at a motor speed (rad/s)."""
    i = max(0.0, min(i_limit, (V_AVAIL - KE * w_motor) / (math.sqrt(3) * R_PH)))
    t_out = motor_torque(i) * RATIO * ETA
    w_out = w_motor / RATIO
    return t_out, t_out * w_out, i, 3 * i * i * R_PH


def curve(i_limit, steps=400):
    w_max = V_AVAIL / KE
    rows = []
    for k in range(steps + 1):
        w = w_max * k / steps
        t, p, i, pcu = point(w, i_limit)
        rows.append((w / RATIO * 60 / (2 * math.pi), t, p, i, pcu))
    return rows


def corner(i_limit):
    w = (V_AVAIL - math.sqrt(3) * R_PH * i_limit) / KE         # where the voltage limit meets the current limit
    t, p, i, pcu = point(w, i_limit)
    return w / RATIO * 60 / (2 * math.pi), t, p, i, pcu


def summary():
    no_load = V_AVAIL / KE / RATIO * 60 / (2 * math.pi)
    out = [f"Bus {BUS:.0f} V DC -> {V_AVAIL:.0f} V rms line-line available; ratio {RATIO:.0f}:1 at {ETA:.0%}"
           f"; no-load output speed {no_load:.0f} rpm"]
    for _, label, il in LIMITS:
        n, t, p, i, pcu = corner(il)
        best = max(curve(il), key=lambda r: r[2])
        eff = p / (p / ETA + pcu) if p else 0
        out.append(f"{label}: {t:.1f} N m flat to {n:.0f} rpm (corner {p / 1000:.2f} kW, {pcu:.0f} W copper,"
                   f" {eff:.0%} efficient); max power {best[2] / 1000:.2f} kW at {best[0]:.0f} rpm")
    return out


# ---------------------------------------------------------------- rendering (Pillow + ffmpeg)
W, H = 1920, 1080
SURFACE, INK, INK2, MUTED, GRID = "#0f1218", "#f0efec", "#c3c2b7", "#8a8f98", "#262b35"
SERIES = {"cont": "#3987e5", "drive": "#d95926", "peak": "#199e70"}   # validated dark slots 1-3 (dataviz skill)
FONT = "/System/Library/Fonts/Helvetica.ttc"


def fonts():
    from PIL import ImageFont
    f = lambda size, bold=False: ImageFont.truetype(FONT, size, index=1 if bold else 0)
    return {"title": f(40, True), "sub": f(24), "axis": f(22), "tick": f(20), "label": f(22, True), "read": f(24)}


PLOT_X0, PLOT_X1 = 150, 1500
TOP = (200, 610)      # torque panel y range
BOT = (680, 960)      # power panel y range
N_MAX, T_MAX, P_MAX = 1200, 32, 2500


def xs(n):
    return PLOT_X0 + n / N_MAX * (PLOT_X1 - PLOT_X0)


def yt(t):
    return TOP[1] - t / T_MAX * (TOP[1] - TOP[0])


def yp(p):
    return BOT[1] - p / P_MAX * (BOT[1] - BOT[0])


def frame(curves, upto_rpm, show_notes, F):
    from PIL import Image, ImageDraw
    img = Image.new("RGB", (W, H), SURFACE)
    d = ImageDraw.Draw(img)
    d.text((PLOT_X0 - 90, 40), "What the joint actuator delivers at its output", font=F["title"], fill=INK)
    d.text((PLOT_X0 - 90, 96), f"Kollmorgen KBM-17H01-B00 + {RATIO:.0f}:1 planetary, {BUS:.0f} V DC bus (240 Vac drive)."
           " Model: back-EMF and winding resistance from the catalog; inductance and iron loss ignored.",
           font=F["sub"], fill=MUTED)
    # grids, ticks, axis titles (recessive)
    for n in range(0, N_MAX + 1, 200):
        for y0, y1 in (TOP, BOT):
            d.line([(xs(n), y0), (xs(n), y1)], fill=GRID, width=1)
        d.text((xs(n), BOT[1] + 12), f"{n}", font=F["tick"], fill=MUTED, anchor="ma")
    for t in range(0, T_MAX + 1, 5):
        d.line([(PLOT_X0, yt(t)), (PLOT_X1, yt(t))], fill=GRID, width=1)
        d.text((PLOT_X0 - 14, yt(t)), f"{t}", font=F["tick"], fill=MUTED, anchor="rm")
    for p in range(0, P_MAX + 1, 500):
        d.line([(PLOT_X0, yp(p)), (PLOT_X1, yp(p))], fill=GRID, width=1)
        d.text((PLOT_X0 - 14, yp(p)), f"{p / 1000:.1f}", font=F["tick"], fill=MUTED, anchor="rm")
    d.text((PLOT_X0, TOP[0] - 36), "Output torque (N·m)", font=F["axis"], fill=INK2)
    d.text((PLOT_X0, BOT[0] - 36), "Output power (kW)", font=F["axis"], fill=INK2)
    d.text(((PLOT_X0 + PLOT_X1) / 2, BOT[1] + 46), "Output speed (rpm)", font=F["axis"], fill=INK2, anchor="ma")
    # curves, 2 px-equivalent lines (3 px at 1080p), drawn up to the sweep speed
    for key, label, il in LIMITS:
        rows = [r for r in curves[key] if r[0] <= upto_rpm]
        if len(rows) > 1:
            d.line([(xs(r[0]), yt(r[1])) for r in rows], fill=SERIES[key], width=4, joint="curve")
            d.line([(xs(r[0]), yp(r[2])) for r in rows], fill=SERIES[key], width=4, joint="curve")
    # legend (always present for 3 series), right of the plot
    lx, ly = PLOT_X1 + 40, TOP[0] + 10
    for k, (key, label, il) in enumerate(LIMITS):
        d.rounded_rectangle([lx, ly + k * 44 + 6, lx + 28, ly + k * 44 + 18], radius=4, fill=SERIES[key])
        d.text((lx + 40, ly + k * 44), label.split(" (")[0], font=F["tick"], fill=INK2)
        d.text((lx + 40, ly + k * 44 + 22), "(" + label.split(" (")[1], font=F["tick"], fill=MUTED)
    if show_notes:
        n, t, p, i, pcu = corner(I_DRIVE)
        d.ellipse([xs(n) - 8, yt(t) - 8, xs(n) + 8, yt(t) + 8], fill=SERIES["drive"], outline=SURFACE, width=3)
        d.ellipse([xs(n) - 8, yp(p) - 8, xs(n) + 8, yp(p) + 8], fill=SERIES["drive"], outline=SURFACE, width=3)
        d.text((xs(n) - 70, yt(t) - 16), f"Corner: {t:.1f} N·m up to {n:.0f} rpm", font=F["label"], fill=INK, anchor="rb")
        d.text((xs(n) - 16, yp(p) + 16), f"Peak {p / 1000:.2f} kW at the corner", font=F["label"], fill=INK, anchor="ra")
        nc, tc, pc, _, _ = corner(I_CONT)
        d.text((xs(80), yt(tc) - 10), f"{tc:.1f} N·m all day (housing bolted to metal)", font=F["tick"], fill=INK2, anchor="lb")
        nl = V_AVAIL / KE / RATIO * 60 / (2 * math.pi)
        d.text((xs(nl) + 10, yt(1.5)), f"No load\n{nl:.0f} rpm", font=F["tick"], fill=INK2, anchor="la")
        d.text((PLOT_X1 + 40, BOT[0]), "Voltage-limited\nabove the corner:\nback-EMF uses up\nthe 325 V bus", font=F["tick"], fill=MUTED)
    return img


def readout(img, curves, rpm, F):
    """Moving operating point on the drive-limit curve, with its numbers."""
    from PIL import ImageDraw
    d = ImageDraw.Draw(img)
    row = min(curves["drive"], key=lambda r: abs(r[0] - rpm))
    n, t, p, i, pcu = row
    for y in (yt(t), yp(p)):
        d.ellipse([xs(n) - 9, y - 9, xs(n) + 9, y + 9], fill=INK, outline=SERIES["drive"], width=3)
    d.text((PLOT_X1 + 40, TOP[0] + 190), f"{n:5.0f} rpm\n{t:5.1f} N·m\n{p / 1000:5.2f} kW\n{i:5.1f} A rms",
           font=F["read"], fill=INK, spacing=8)


def render():
    from PIL import Image  # noqa: F401  (fail early without Pillow)
    F = fonts()
    curves = {key: curve(il) for key, _, il in LIMITS}
    still = frame(curves, N_MAX + 1, True, F)
    still.save(HERE / "motor-curves.png")
    fps, sweep_s, hold_s = 30, 7, 5
    out = HERE / "motor-curves-chart.mp4"
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                           "-r", str(fps), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                           "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out)], stdin=subprocess.PIPE)
    no_load = V_AVAIL / KE / RATIO * 60 / (2 * math.pi)
    for k in range(sweep_s * fps):
        s = k / (sweep_s * fps - 1)
        rpm = no_load * (s * s * (3 - 2 * s))
        img = frame(curves, rpm, False, F)
        readout(img, curves, rpm, F)
        ff.stdin.write(img.tobytes())
    data = still.tobytes()
    for _ in range(hold_s * fps):
        ff.stdin.write(data)
    ff.stdin.close()
    if ff.wait():
        sys.exit("ffmpeg failed")
    print(f"wrote {HERE.name}/motor-curves.png, {HERE.name}/{out.name}")


def main():
    for line in summary():
        print(line)
    with open(HERE / "motor-curves.csv", "w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["limit", "current_limit_arms", "output_rpm", "output_torque_nm", "output_power_w", "current_arms",
                     "copper_loss_w"])
        for key, _, il in LIMITS:
            for r in curve(il, 120):
                wr.writerow([key, il] + [round(v, 3) for v in r])
    if "--render" in sys.argv:
        render()


if __name__ == "__main__":
    main()
