"""Mobility of the crawler transporter. Prints the numbers the README quotes.

The CAD mass is the STEVE build, revision 2. The cells and the crew are not
solids. Rolling resistance and drive efficiency are typical figures, not
measurements. The 80:1 final drive is a chosen ratio, not a cut gearbox.
"""
import math

# Grams from the revision 2 build, one of each component.
PARTS_G = {
    "hull": 6302139.202,
    "track": 2922222.054,
    "idler": 492832.949,
    "sprocket": 464853.804,
    "road_wheel": 107790.889,
    "door": 27035.520,
}
COUNT = {"hull": 1, "track": 2, "idler": 2, "sprocket": 2, "road_wheel": 12, "door": 2}

cad_kg = sum(PARTS_G[k] * COUNT[k] for k in PARTS_G) / 1000.0
cells_kg = 800.0  # about 128 kWh at 160 Wh/kg, the figure used for the icescape pack
crew_kg = 180.0
mass = cad_kg + cells_kg + crew_kg

pitch_r = 0.635  # m, mid-shoe
contact_m = 4.336  # sprocket centre to idler centre
shoe_w = 0.42
area = 2.0 * contact_m * shoe_w

ratio = 80.0
eff = 0.90
crr_firm = 0.07
crr_soft = 0.15
grade = 0.10
speed = 10.0 / 3.6  # m/s
g = 9.81

weight = mass * g
sprocket_rpm = speed / (2.0 * math.pi * pitch_r) * 60.0
motor_rpm = sprocket_rpm * ratio


def torque(force):
    """N·m at one sprocket, then at one motor, for a force shared by two tracks."""
    per = force / 2.0
    at_sprocket = per * pitch_r
    at_motor = at_sprocket / (ratio * eff)
    return at_sprocket, at_motor


firm = crr_firm * weight
soft = crr_soft * weight
climb = firm + grade * weight
_, motor_firm = torque(firm)
sprocket_climb, motor_climb = torque(climb)
power_firm = firm * speed

# Static tip about the outer edge of the downhill track. Geometry only.
com_z = 1.330  # m, the build's centre of mass
outer_y = 1.230  # m, outside of the shoe
tip_deg = math.degrees(math.atan(outer_y / com_z))

gp = weight / area / 1000.0

print(f"cad mass        {cad_kg:.1f} kg")
print(f"operating mass  {mass:.1f} kg   (cad {cad_kg:.1f} + cells {cells_kg:.0f} + crew {crew_kg:.0f})")
print(f"pitch radius    {pitch_r:.3f} m    contact {contact_m:.3f} m x {shoe_w:.2f} m, both tracks")
print(f"ground pressure {gp:.1f} kPa")
print(f"com height      {com_z:.3f} m    static tip {tip_deg:.1f} deg about the outer shoe edge")
print()
print(f"cruise          {speed * 3.6:.1f} km/h    sprocket {sprocket_rpm:.1f} rpm    motor {motor_rpm:.0f} rpm at {ratio:.0f}:1")
print(f"firm, Crr {crr_firm:.2f}   force {firm:.0f} N    motor {motor_firm:.1f} N·m each    power {power_firm / 1000:.1f} kW")
print(f"soft, Crr {crr_soft:.2f}   force {soft:.0f} N    motor {torque(soft)[1]:.1f} N·m each")
print(f"firm + {grade:.0%} grade   sprocket {sprocket_climb:.0f} N·m    motor {motor_climb:.1f} N·m each")
print()
print(f"cells {cells_kg:.0f} kg at 160 Wh/kg is {cells_kg * 160 / 1000:.0f} kWh")
print(f"at {power_firm / 1000:.1f} kW that is {cells_kg * 160 / power_firm:.1f} h, {cells_kg * 160 / power_firm * speed * 3.6:.0f} km, before other losses")
