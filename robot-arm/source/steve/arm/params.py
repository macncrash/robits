"""Six-axis robot arm parameters (mm). Lanes are the Y offsets of each link's centreline."""
base_h = 110  # mm Pedestal height (J1 actuator sits on top)
shoulder_z = 300  # mm Shoulder (J2) axis height
upper_len = 425  # mm Shoulder-to-elbow length
fore_len = 400  # mm Elbow-to-wrist (J3 to J4) length
ua_y = 127  # mm Upper-arm lane (Y offset)
fa_y = 36  # mm Forearm lane (Y offset)
w_y = 127  # mm Wrist lane (Y offset)
grip_stroke = 30  # mm Travel of each finger
elbow_z = shoulder_z + upper_len
a5_x = fore_len + 95
w2_x = fore_len + 156
a6_z = elbow_z - 89.5  # J6 sits 2 mm below the J5 housing (fit check: they touched)
