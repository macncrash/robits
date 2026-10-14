"""Lathe kit parameters (lathe frame: spindle axis along +X at y = 0, z = 0; Z up; operator at -Y; mm).

Named lathe_params (not params) so it can't clash with the linked actuator's own params module.
"""
centre_height = 98  # mm Spindle axis above the bed ways (swing 196 over the bed)
bed_top = -98  # z of the bed ways (top of the dovetail)
bed_x0 = -50  # mm Bed starts under the headstock
bed_len = 500  # mm Bed length (about 200 mm between the chuck and the live centre)
screw_pitch = 2.0  # mm Tr10 x 2 screws on the compound and the tailstock quill
dial_divisions = 100  # Graduations on the Tr10 x 2 dials: 2 mm / 100 = 0.02 mm per division
ball_lead = 4.0  # mm SFU1204 ball screws on the carriage and the cross-slide
ball_dial_divisions = 200  # Graduations on the ball-screw dials: 4 mm / 200 = 0.02 mm per division
carriage_x = 180  # mm Carriage left edge as modelled
tool_y = -55  # mm Compound and tool post centre (in front of the axis)
tailstock_x = 330  # mm Tailstock base left edge as modelled
# Milling attachment (branch "milling"): the actuator moves from the headstock plate onto the column's Z slide.
mill_spindle_x = 215  # mm Mill spindle axis x (over the carriage centre line as modelled)
mill_spindle_y = -45  # mm Mill spindle axis y (over the vise on the cross-slide)
mill_head_z = 133  # mm Where the actuator's frame origin sits on the Z slide as modelled (cutter tip at z -9)
