"""Band saw parameters (saw frame: the blade's cutting run is vertical at x 0, y 0, teeth toward the operator at
-Y; the wheels turn in the XZ plane with their centres at x 125; the table top is z 0; Z up; mm).

Named bandsaw_params (not params) so it can't clash with the linked actuator's own params module.
"""
wheel_r = 125  # mm Wheel radius over the tyre (Ø250 wheels)
wheel_x = 125  # mm Wheel centres (the cutting run of the blade at x 0, the return run at x 250)
blade_t = 0.65  # mm Bi-metal blade thickness
blade_w = 13  # mm Blade width modelled (6-13 mm blades fit the guides)
blade_len = 1829  # mm Blade length (72 in, a stock length)
lower_z = -245  # z of the lower (driven) wheel centre
upper_z = 275.9  # z of the upper (idler) wheel centre at nominal tension: (1829 - 2 pi 125.3) / 2 = 520.9 above
guide_z = 60  # z of the upper guide's bottom face as modelled (40 mm of stock under it; 0-100 range)
belt_c = 238.22  # mm Centre distance, 20T to 100T HTD 8M on a 1000-8M-30 belt
motor_z = -483.22  # z of the actuator axis (lower wheel centre minus belt_c)
motor_y = -20.5  # y of the actuator frame's origin: its output face (actuator z 65.5) at y 45
stand_top = -583.22  # z of the stand's top surface (pedestal base at motor_z - 88, on a 12 mm motor plate)
floor_z = -1000  # z of the floor: table top 1000 mm high
