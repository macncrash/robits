"""Icescape rover, millimetres and degrees.

Mission 0 is the Antarctic foam-filled tire. Mission 1 is the offworld metal wheel.
The corner frame has its origin at the wheel centre, +X forward, +Y outboard on the
left-hand part, +Z up. The right-hand corners are the same part turned 180° about Z.
"""

mission = 0  # 0 Antarctic tire, 1 offworld metal wheel

wheel_r = 340.0  # mm outer radius, both missions, so the stance does not change
half_wb = 640.0  # mm axle ahead of and behind the centre
half_track = 590.0  # mm wheel centre from the centreline
belly = 280.0  # mm hull underside above the ice

# Linked joint actuator (press3 shell of the unknown-machine module).
act_diameter = 120.0  # mm flange OD
act_length = 110.0  # mm overall, axis centred on the part origin
act_half = 55.0  # mm length / 2

# Corner, local to the wheel centre.
steer_y = -150.0  # mm kingpin, inboard of the tire
steer_z = 135.0  # mm steer-actuator centre; output face is 55 mm below this
drive_y = -205.0  # mm drive-actuator origin; output face is 55 mm outboard of this
hub_y0 = -150.0  # mm hub, from the drive output face
hub_y1 = -82.0

arm_y0 = -300.0  # mm inboard face, also the swing-axis plane
arm_y1 = -210.0  # mm outboard face, tangent to the steer actuator
arm_z = 145.0
arm_h = 36.0
arm_t = 50.0  # mm across X

# Swing and steer stops. The swing is small so the arm stays inside the clevis gap.
arm_deg = 6.0
steer_deg = 22.0
