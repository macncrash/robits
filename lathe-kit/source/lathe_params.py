"""Lathe kit parameters (lathe frame: spindle axis along +X at y = 0, z = 0; Z up; operator at -Y; mm).

Named lathe_params (not params) so it can't clash with the linked actuator's own params module.
"""
centre_height = 98  # mm Spindle axis above the bed ways (swing 196 over the bed)
bed_top = -98  # z of the bed ways (top of the dovetail)
bed_x0 = -50  # mm Bed starts under the headstock
bed_len = 500  # mm Bed length (about 200 mm between the chuck and the live centre)
screw_pitch = 2.0  # mm Tr10 x 2 feed screws on every slide
dial_divisions = 100  # Graduations on every dial: 2 mm / 100 = 0.02 mm per division
carriage_x = 180  # mm Carriage left edge as modelled
tool_y = -55  # mm Compound and tool post centre (in front of the axis)
tailstock_x = 330  # mm Tailstock base left edge as modelled
