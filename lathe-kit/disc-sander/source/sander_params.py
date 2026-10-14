"""Disc sander parameters (sander frame: disc axis along -Y through x 0, z 0, abrasive face toward the operator at
-Y; Z up; mm).

Named sander_params (not params) so it can't clash with the linked actuator's own params module.
"""
disc_d = 250  # mm Platen and PSA abrasive disc diameter (10 in)
disk_face = 65.5  # mm Actuator output disk face (y -65.5 here)
hub_t = 20  # mm 303 hub thickness (puts the platen clear of the pedestal and the guard's back wall)
platen_t = 10  # mm 6061 platen thickness
abrasive_t = 1.0  # mm PSA abrasive disc
base_z = -88  # z of the actuator pedestal's base (88 below the axis)
riser_h = 70  # mm Riser block under the pedestal: lifts the axis clear of the Ø250 disc
top_t = 10  # mm Stand top plate
table_y = -100  # y of the table's near edge and tilt axis (3.5 mm from the abrasive)
table_z = -20  # z of the table top (875 above the floor)
floor_z = -895  # z of the floor
