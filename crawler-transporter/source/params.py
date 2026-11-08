"""Crawler transporter, millimetres.

The reference sheet is 1031 by 499 pixels over the vehicle, cab to the right.
Length is set from a seated cab, and the height follows that pixel box, so a
side elevation has the same proportions as the drawing.

Frame: X forward (cab and bumper are +X), Y to the left, Z up.
Origin on the ground, midway along the length, on the centreline.
"""

length = 6600.0
art_w = 1031.0
art_h = 499.0
height = length * art_h / art_w  # ground to the cab-roof lamps, 3194 mm

width = 2460.0
half_w = width / 2.0  # 1230, outside of the hull and of the tracks

# Hull shell. The side profile is this outline, extruded across the full width.
wall = 16.0
hull_bottom = 1360.0
hull_roof = 2500.0
hull_rear = -3100.0
hull_front = 2780.0
cab_back = 700.0
cab_roof = 3100.0
bumper_top = 1920.0
bumper_bottom = 1640.0
bumper_front = 3300.0

# Track loop. One rigid shoe band per side. The pitch line is midway in the shoe.
shoe_w = 420.0
track_y = half_w - shoe_w / 2.0  # 1020, band centre
outer_r = 670.0
inner_r = 600.0
center_z = outer_r  # outer bottom sits on the ground
pitch_r = (inner_r + outer_r) / 2.0  # 635
sx = -2234.0  # rear sprocket
ix = 2102.0  # front idler

# Road wheels roll on the inner face of the bottom shoe, with a small gap.
wheel_r = 196.0
wheel_gap = 4.0
wheel_z = (center_z - inner_r) + wheel_gap + wheel_r  # 270
wheel_w = 220.0
wheel_xs = (-1550.0, -970.0, -390.0, 190.0, 770.0, 1350.0)

sprocket_r = 520.0
tooth_tip = 590.0  # under the shoe's inner face at 600
idler_r = 560.0

# Final-drive shaft, local to a sprocket placed at y = ±track_y.
shaft_r = 32.0
bore_r = 46.0

# Side door. Hinge on the forward edge. The panel is centred on its origin in Y and Z.
door_w = 780.0
door_h = 880.0
door_t = 16.0
door_x = -80.0  # hinge
door_z = 1920.0
door_y = half_w + 6.0 + door_t / 2.0  # 1244, 6 mm off the hull
door_deg = 70.0
