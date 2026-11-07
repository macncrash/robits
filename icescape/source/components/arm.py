"""Swing arm. Inboard face is the swing axis. Outboard face is tangent to the steer actuator,
which bolts to that face and does not turn with the wheel.
"""
from steve import Component
from params import arm_y0, arm_y1, arm_z, arm_h, arm_t

arm = Component("arm", name="Swing arm")
arm.box(
    "beam",
    arm_t,
    arm_y1 - arm_y0,
    arm_h,
    at=(0, (arm_y0 + arm_y1) / 2, arm_z),
)
arm.material("aluminum-6061-t6", finish="anodized", color="#3a424c")
