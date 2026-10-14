"""Hand checks for the planetary joint actuator (unknown-machine).

Run with plain Python 3 (no dependencies): python3 hand_calcs.py
Every input is an assumption stated below; change them and re-run. Linear: results scale with torque.
"""
import math

# ---- Load case: Kollmorgen KBM-17H01-B00, drive peak current limited to ~5.9 A (catalog p. 20) ----
T_motor = 4.0        # N·m peak motor torque the gears are sized for (the motor itself can make 6.14 N·m)
n_motor = 3000       # rpm motor speed for the dynamic factor and planet-pin sliding speed
K_share = 1.15       # load-sharing factor between the 3 planets (unequal sharing from tolerances)

# ---- Gear stage (from params.py) ----
m, Zs, Zp, Zr, b = 1.0, 18, 27, 72, 12.0   # module mm, teeth, face width mm
n_planets = 3
ratio = 1 + Zr / Zs
T_out = T_motor * ratio
T_ring = T_out - T_motor

d_s, d_p = m * Zs, m * Zp                    # pitch diameters, mm
Ft = T_motor * 1000 / (d_s / 2) / n_planets * K_share   # N tangential force per mesh
v = math.pi * d_s / 1000 * n_motor / 60      # m/s pitch-line speed at the sun
Kv = (6.1 + v) / 6.1                         # AGMA/Barth dynamic factor, cut teeth


def lewis_Y(z):
    """Lewis form factor, 20° full-depth (table values, linear between)."""
    table = [(12, .245), (14, .277), (16, .296), (18, .309), (20, .322), (22, .331), (24, .337), (26, .346),
             (28, .353), (30, .359), (34, .371), (38, .384), (45, .401), (50, .409), (60, .422), (75, .435)]
    for (z0, y0), (z1, y1) in zip(table, table[1:]):
        if z0 <= z <= z1:
            return y0 + (y1 - y0) * (z - z0) / (z1 - z0)
    return table[-1][1]


ZE, ZH = 189.8, 2.495                         # √MPa steel/steel, 20° pressure angle


def hertz(d1, u, internal=False):
    k = (u - 1) / u if internal else (u + 1) / u
    return ZE * ZH * math.sqrt(Ft * Kv / (b * d1) * k)


sig_sun = Ft * Kv / (b * m * lewis_Y(Zs))
sig_planet = Ft * Kv / (b * m * lewis_Y(Zp))
sH_sun = hertz(d_s, Zp / Zs)
sH_ring = hertz(d_p, Zr / Zp, internal=True)

# ---- Planet pins: ISO 2338 6 x 18, planet face 12 mm between the carrier plates (13 mm span) ----
d_pin, span = 6.0, 13.0
F_pin = 2 * Ft                                  # sun + ring tooth forces on a planet add up
M_pin = F_pin * span / 8                        # N·mm, load spread over the face, simply supported
sig_pin = 32 * M_pin / (math.pi * d_pin ** 3)
p_journal = F_pin / (d_pin * b)                 # MPa, planet sliding on the pin
n_planet_rel = Zs / Zp * n_motor * (1 - 1 / ratio)   # rpm of the planet relative to the carrier
v_journal = math.pi * d_pin / 1000 * n_planet_rel / 60
pv = p_journal * v_journal

# ---- Flange screws: 4 x M5 on PCD 100 must hold the ring-gear reaction by friction ----
mu, r_pcd, n_screws = 0.15, 0.050, 4
preload = {"A2-70 stainless": 4.0e3, "8.8 steel": 7.0e3, "12.9 steel": 10.5e3}   # N, typical at catalogue torque
slip = {k: n_screws * f * mu * r_pcd for k, f in preload.items()}
engagement = 44 - 34.5                          # mm of M5 thread in the 6061 housing

# ---- Two-piece carrier: front disk on the rear part's posts, 3 x ISO 10642 M4 on the 22.5 mm planet orbit ----
r_orbit, n_disk_screws = m * (Zs + Zp) / 2 / 1000, 3     # m
preload_m4 = 2.5e3                                        # N, A2-70 M4 at catalogue torque (≈ M5 value × stress-area ratio)
T_disk_slip = n_disk_screws * preload_m4 * mu * r_orbit   # N·m the joint holds by friction alone
T_carrier = T_out * K_share                               # worst case: all of it crosses the joint
tau_pin_joint = F_pin / (math.pi * d_pin ** 2 / 4)        # MPa if a pin carries its planet's load across the joint

# ---- Motor: KBM-17H01-B00 winding B (catalog p. 20) and the bonded joints (mounting guide pp. 90-95) ----
Kt, Rm, Tc, T_cont_duty = 0.681, 6.02, 2.06, 1.3   # N·m/Arms, ohm line-line, N·m continuous rating, N·m duty torque
K_per_W = (72.9 - 25) / 40                          # K/W housing rise above air, bolted to the pedestal, base insulated (STEVE, 40 W)
K_per_W_band = (88.2 - 25) / 40                     # K/W the same, on the old clamp band (no heat path into the pedestal)
P_cu = lambda T: 1.5 * (T / Kt) ** 2 * Rm          # W copper loss, three-phase from line-line resistance (at 25 °C)
I_limit = T_motor / Kt                             # Arms drive peak-current limit for 4 N·m
r_stator, L_stator, bonded = 84.963 / 2000, 57.80 / 1000, 0.5   # m, m, adhesive over at least half the bore
r_rotor, L_rotor = 30.010 / 2000, 30.15 / 1000      # m rotor bore and length on the hub sleeve
tau_stator_bond = T_motor / (2 * math.pi * r_stator ** 2 * L_stator * bonded) / 1e6   # MPa
tau_rotor_bond = T_motor / (2 * math.pi * r_rotor ** 2 * L_rotor) / 1e6               # MPa
lap_shear_2214 = 30.0                               # MPa, typical for 3M Scotchweld 2214 on aluminium/steel

# ---- Pedestal mount: 4 x ISO 4762 M5 x 20 A2-70 from below into the housing, 2 x 4 mm dowels ----
n_mount, r_saddle = 4, 0.056                        # screws, m saddle radius (friction acts at the housing OD)
slip_mount = n_mount * preload["A2-70 stainless"] * mu * r_saddle   # N·m about the axis, by friction alone
mount_engagement = 54.2 - 44.0                      # mm of M5 thread in the housing (surface at x 16 to the screw tip)

# ---- Bearings (catalogue ratings, check the maker's datasheet) ----
C0_61806, C0_6001 = 2.9e3, 2.36e3               # N static load ratings (61806 was the first output bearing)
Fr_out, Fa_out, arm = 150.0, 100.0, 23.0         # N, N, mm overhung load case and its lever to the bearing
P0_out = max(Fr_out, 0.6 * Fr_out + 0.5 * Fa_out)
M_out = Fr_out * arm / 1000                      # N·m tilting moment on a single deep-groove bearing

if __name__ == "__main__":
    print(f"Ratio {ratio:.1f}:1, output torque {T_out:.0f} N·m, ring reaction {T_ring:.0f} N·m")
    print(f"Tooth force per mesh Ft = {Ft:.0f} N (K_share {K_share}), v = {v:.2f} m/s, Kv = {Kv:.2f}")
    print(f"Lewis bending: sun {sig_sun:.0f} MPa, planet {sig_planet:.0f} MPa")
    print(f"Hertz contact: sun-planet {sH_sun:.0f} MPa, planet-ring {sH_ring:.0f} MPa")
    print(f"Planet pin: load {F_pin:.0f} N, bending {sig_pin:.0f} MPa, journal p {p_journal:.1f} MPa,"
          f" v {v_journal:.2f} m/s, PV {pv:.2f} MPa·m/s")
    for k, s in slip.items():
        print(f"Flange slip torque with {k} screws: {s:.1f} N·m vs {T_ring:.0f} N·m needed (x{s / T_ring:.2f})")
    print(f"M5 thread engagement in aluminium: {engagement:.1f} mm = {engagement / 5:.1f} d (aim >= 2 d)")
    print(f"Carrier joint: 3 x M4 friction holds {T_disk_slip:.1f} N·m vs {T_carrier:.0f} N·m worst case"
          f" (x{T_disk_slip / T_carrier:.2f}); planet pins as dowels: {tau_pin_joint:.0f} MPa shear each")
    print(f"Motor: copper loss {P_cu(T_cont_duty):.0f} W at {T_cont_duty} N·m duty, {P_cu(Tc):.0f} W at the"
          f" {Tc} N·m continuous rating; peak-current limit {I_limit:.1f} A for {T_motor} N·m")
    print(f"Housing on the pedestal in still air at {K_per_W:.2f} K/W (was {K_per_W_band:.2f} on the band): about {25 + K_per_W * P_cu(T_cont_duty):.0f} °C at the duty torque"
          f" (copper only), {25 + K_per_W * P_cu(Tc):.0f} °C at the motor's full continuous rating")
    print(f"Pedestal screws: friction holds {slip_mount:.0f} N·m about the axis vs {T_out:.0f} N·m output reaction"
          f" (x{slip_mount / T_out:.1f}), plus 2 dowels; {mount_engagement:.1f} mm = {mount_engagement / 5:.1f} d of M5 thread")
    print(f"Bond shear at {T_motor} N·m: stator {tau_stator_bond * 1000:.0f} kPa (half the bore bonded),"
          f" rotor {tau_rotor_bond * 1000:.0f} kPa vs about {lap_shear_2214:.0f} MPa lap shear")
    print(f"Output bearing CRBH 3510: {Fr_out:.0f} N radial, {Fa_out:.0f} N axial, {M_out:.2f} N·m tilting moment;"
          f" check the maker's moment rating (the old 61806: s0 {C0_61806 / P0_out:.0f} on force alone)")
