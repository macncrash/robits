"""Six-axis robot arm (press3)

Collaborative-style 6-DOF arm reverse-engineered from the press3 robot-arm tee: stepped pedestal,
turret, shoulder, long upper arm, elbow, forearm with blue collars, a three-joint wrist with a
cable loop, and a two-finger claw gripper. Every joint is the linked "Joint actuator (press3)"
part (pedestal = 0) at a size that suits its load.

Zero pose (as modelled): upper arm vertical, forearm horizontal along +X, gripper pointing down.
Joint axes: J1 Z, J2 Y (shoulder), J3 Y (elbow), J4 Y (wrist pitch), J5 X (wrist yaw), J6 Z (tool roll);
the fingers slide along X, coupled as "grip".
"""
from steve import Design
from params import base_h, shoulder_z, elbow_z, fore_len, ua_y, fa_y, w_y, a5_x, w2_x, a6_z, grip_stroke
from components.base import base
from components.turret import turret
from components.upper_arm import upper_arm
from components.forearm import forearm
from components.upper_arm_collars import upper_arm_collars
from components.forearm_collars import forearm_collars
from components.wrist1 import wrist1
from components.wrist2 import wrist2
from components.tool import tool
from components.finger_l import finger_l
from components.finger_r import finger_r
from links import actuator
from motion import add_motion
from checks import add_checks

design = Design("Six-axis robot arm (press3)")
design.add(base)
design.add(turret)
design.add(upper_arm)
design.add(forearm)
design.add(upper_arm_collars)
design.add(forearm_collars)
design.add(wrist1)
design.add(wrist2)
design.add(tool)
design.add(finger_l)
design.add(finger_r)

# Joint actuators: output flange toward the child link.
design.add(actuator(diameter=140, length=100, pedestal=0), name="act_j1", at=(0, 0, base_h + 50))
design.add(actuator(diameter=140, length=130, pedestal=0), name="act_j2", at=((0, 0, shoulder_z), ("X", -90)))
design.add(actuator(diameter=120, length=110, pedestal=0), name="act_j3", at=((0, ua_y, elbow_z), ("X", 90)))
design.add(actuator(diameter=100, length=100, pedestal=0), name="act_j4", at=((fore_len, fa_y, elbow_z), ("X", -90)))
design.add(actuator(diameter=90, length=90, pedestal=0), name="act_j5", at=((a5_x, w_y, elbow_z), ("Y", 90)))
design.add(actuator(diameter=90, length=85, pedestal=0), name="act_j6", at=((w2_x, w_y, a6_z), ("X", 180)))

add_motion(design)
add_checks(design)
result = design.result()
