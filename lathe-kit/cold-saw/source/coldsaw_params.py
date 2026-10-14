"""Cold saw parameters (saw frame: stock along X, blade in the YZ plane at x 0, operator at -Y, Z up; the stand
top is z 0; mm). Modelled with the head down at the end of a cut.

Named coldsaw_params (not params) so it can't clash with the linked actuator's own params module.
"""
blade_d = 250  # mm HSS cold-saw blade diameter
blade_t = 2.0  # mm Blade thickness (kerf about 2.2)
blade_y = -20  # mm Blade axis y (over the stock's centre)
blade_z = 150  # mm Blade axis z with the head down (blade 5 mm into the turntable slot)
table_z = 30  # mm Work table: top of the turntable and the base's pads
stock_d = 40  # mm Round bar in the vise, back against the fence at y 0
gear_x = 74  # mm Worm axis and actuator axis x
worm_z = 213  # mm Worm axis z (blade axis + the NMRV063's 63 mm centre distance)
act_y = 222.5  # mm Actuator frame origin y (output disk face at y 157)
pivot_y = 300  # mm Chop pivot axis y
pivot_z = 110  # mm Chop pivot axis z
ratio = 20  # Worm gearbox ratio
floor_z = -900  # z of the floor (stand top at 900)
