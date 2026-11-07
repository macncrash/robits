"""Mobility of the icescape rover from the Kollmorgen card and the gear ratio.

Run: python3 analysis/hand_calcs.py

The motor is the KBM-17H01-C winding. The B winding in the shop tools has the same torque and
about twice the back-EMF, so on a 48 V pack it crawls. Numbers are the catalog values in
parts/frameless-motors/kollmorgen-kbm-17h01-c.toml. Nothing here is a measured test.
"""
import math

# Catalog, KBM-17H01-C00, page 20.
T_CONT = 2.07  # N·m
T_PEAK = 6.35  # N·m
KB = 21.5  # Vrms line-line per 1000 rpm

# Two planetary stages, each the unknown-machine 5:1, each 90% (a single stage, losses not measured).
STAGE = 5
ETA_STAGE = 0.90
RATIO = STAGE * STAGE
ETA = ETA_STAGE * ETA_STAGE

# 48 V pack. Sine PWM reaches about 0.612 of the bus as line-line RMS. That factor is the assumption.
V_BUS = 48.0
V_RMS = 0.612 * V_BUS

WHEEL_R = 0.340  # m
SCRUB = 0.150  # m, kingpin to the contact patch
MASS_CAD = 241.872  # kg, STEVE revision 5, no cells
MASS_CELLS = 12.5  # kg, 2 kWh at 160 Wh/kg, not in the CAD
MASS = MASS_CAD + MASS_CELLS
G = 9.81
N = 4

BELLY = 0.272  # m, skid underside, axles at wheel radius
WHEELBASE = 1.280  # m


def main():
    t_wheel_cont = T_CONT * RATIO * ETA
    t_wheel_peak = T_PEAK * RATIO * ETA
    f_cont = N * t_wheel_cont / WHEEL_R
    f_peak = N * t_wheel_peak / WHEEL_R
    weight = MASS * G

    n_nl = V_RMS / KB * 1000  # rpm at the motor, no load
    # Straight torque-speed line from peak (taken as stall) to no-load.
    n_cont = n_nl * (1 - T_CONT / T_PEAK)
    v_nl = (n_nl / RATIO) / 60 * 2 * math.pi * WHEEL_R
    v_cont = (n_cont / RATIO) / 60 * 2 * math.pi * WHEEL_R

    t_steer_cont = T_CONT * STAGE * ETA_STAGE
    t_steer_peak = T_PEAK * STAGE * ETA_STAGE
    fz = weight / N

    print(f"operating mass {MASS:.1f} kg  (CAD {MASS_CAD:.3f} + cells {MASS_CELLS:.1f})")
    print(f"ratio {RATIO}:1   efficiency {ETA:.2f}   bus {V_BUS:.0f} V   Vrms {V_RMS:.1f}")
    print()
    print(f"wheel torque   cont {t_wheel_cont:.1f} N·m    peak {t_wheel_peak:.1f} N·m")
    print(f"tractive force cont {f_cont:.0f} N       peak {f_peak:.0f} N")
    print(f"as a fraction of weight   cont {f_cont / weight:.2f}    peak {f_peak / weight:.2f}")
    print(f"no-load speed  {v_nl:.2f} m/s     speed at continuous torque {v_cont:.2f} m/s")
    print()
    print("grade, continuous torque, after rolling resistance:")
    for name, crr in (("hard ice", 0.02), ("packed snow", 0.10), ("soft snow", 0.20)):
        net = f_cont / weight - crr
        print(f"  {name:14} Crr {crr:.2f}   grade {math.degrees(math.atan(net)):.1f}°  ({net * 100:.0f}%)")
    print()
    print(f"steer torque at the kingpin   cont {t_steer_cont:.1f} N·m   peak {t_steer_peak:.1f} N·m")
    print(f"scrub {SCRUB * 1000:.0f} mm    load per wheel {fz:.0f} N")
    print(f"highest friction it can steer against   cont {t_steer_cont / (fz * SCRUB):.2f}   peak {t_steer_peak / (fz * SCRUB):.2f}")
    print("  ice is about 0.05–0.15, packed snow about 0.3, rock about 0.6")
    print()
    # 2 kWh, cruise on packed snow at the continuous-torque speed, plus a flat avionics draw.
    crr = 0.10
    v = v_cont
    p_mech = crr * weight * v
    p_elec = p_mech / ETA / 0.85 + 40  # 85% motor, guessed; 40 W avionics and heaters off
    hours = 2000 / p_elec
    print(f"packed-snow cruise {v:.2f} m/s   electrical {p_elec:.0f} W   2 kWh lasts {hours:.1f} h ({v * hours * 3.6:.0f} km)")
    print()
    print("belly clearance over a sine ridge, both axles on the surface, belly rigid:")
    print(f"  flat ground {BELLY * 1000:.0f} mm")
    for length, amp in ((2.0, 0.10), (2.0, 0.20), (4.0, 0.20), (4.0, 0.40)):
        gap = sine_gap(length, amp)
        flag = "  STRIKE" if gap < 0 else ""
        print(f"  wavelength {length:.0f} m  amplitude {amp * 1000:.0f} mm   gap {gap * 1000:.0f} mm{flag}")


def sine_gap(length, amp):
    """Minimum gap under the flat belly. Axle height is r above the sine, small-slope."""
    k = 2 * math.pi / length
    # Sample a crest under the middle and a crest under an axle. Report the worse.
    worst = 1e9
    for phase in (0.0, math.pi):
        def h(x):
            return amp * math.sin(k * x + phase)

        x1, x2 = -WHEELBASE / 2, WHEELBASE / 2
        z1, z2 = h(x1) + WHEEL_R, h(x2) + WHEEL_R
        pitch = math.atan2(z2 - z1, WHEELBASE)
        # Belly is 68 mm below the axle line, perpendicular to it, from 0.38 m behind
        # the rear axle to 0.14 m ahead of the front (the flat of the hull).
        drop = WHEEL_R - BELLY
        for i in range(41):
            t = -0.38 + (WHEELBASE + 0.14 + 0.38) * i / 40
            x = -WHEELBASE / 2 + t * math.cos(pitch)
            z = z1 + t * math.sin(pitch) - drop * math.cos(pitch)
            worst = min(worst, z - h(x))
    return worst


if __name__ == "__main__":
    main()
