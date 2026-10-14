"""Bench grinder parameters (frame: spindle along X at y 0, z = spindle_z; Z up from the floor; operator at -Y; mm).

Named grinder_params (not params) so it can't clash with a linked design's own params module.
"""
spindle_z = 1020  # mm Wheel centre height above the floor (elbow height for most people)
wheel_d = 150  # mm Wheel diameter (150 x 20, rated 4140 rpm or more)
wheel_w = 20  # mm Wheel width
wheel_x = 115  # mm Inner face of each wheel from the motor centre
rest_gap = 2  # mm Tool rest to wheel (keep it 3 mm or less as the wheel wears)
guard_open = 65  # deg Guard opening above the horizontal (ANSI B7.1 / EN 12413 limit for bench grinders)
