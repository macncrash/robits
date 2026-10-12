"""Joints, poses and the pick-and-place animation (kept out of main.py)."""
from params import shoulder_z, elbow_z, fore_len, w_y, w2_x, grip_stroke


def add_motion(design):
    design.revolute("j1", "base", "turret", axis=((0, 0, 0), (0, 0, 1)), limits=(-180, 180))
    design.revolute("j2", "turret", "upper_arm", axis=((0, 0, shoulder_z), (0, 1, 0)), limits=(-110, 110))
    design.revolute("j3", "upper_arm", "forearm", axis=((0, 0, elbow_z), (0, 1, 0)), limits=(-160, 30))  # beyond +30 the wrist folds into the shoulder
    design.revolute("j4", "forearm", "wrist1", axis=((fore_len, 0, elbow_z), (0, 1, 0)), limits=(-180, 180))
    design.revolute("j5", "wrist1", "wrist2", axis=((0, w_y, elbow_z), (1, 0, 0)), limits=(-180, 180))
    design.revolute("j6", "wrist2", "tool", axis=((w2_x, w_y, 0), (0, 0, 1)), limits=(-360, 360))
    design.slider("grip_l", "tool", "finger_l", axis=((0, 0, 0), (1, 0, 0)), limits=(0, grip_stroke))
    design.slider("grip_r", "tool", "finger_r", axis=((0, 0, 0), (-1, 0, 0)), limits=(0, grip_stroke))
    design.couple("grip", {"grip_l": 1, "grip_r": 1}, limits=(0, grip_stroke))

    design.rigid("ua_collars", "upper_arm", "upper_arm_collars")
    design.rigid("fa_collars", "forearm", "forearm_collars")
    design.rigid("j1_stator", "base", "act_j1")
    design.rigid("j2_stator", "turret", "act_j2")
    design.rigid("j3_stator", "upper_arm", "act_j3")
    design.rigid("j4_stator", "forearm", "act_j4")
    design.rigid("j5_stator", "wrist1", "act_j5")
    design.rigid("j6_stator", "wrist2", "act_j6")

    home = dict(j1=0, j2=0, j3=0, j4=0, j5=0, j6=0, grip=0)
    design.pose("home", **home)
    design.pose("above_a", j1=-35, j2=20, j3=10, j4=-30, j5=0, j6=0, grip=0)
    design.pose("at_a", j1=-35, j2=35, j3=10, j4=-45, j5=0, j6=0, grip=0)
    design.pose("gripped_a", j1=-35, j2=35, j3=10, j4=-45, j5=0, j6=0, grip=18)
    design.pose("lift_a", j1=-35, j2=20, j3=10, j4=-30, j5=0, j6=0, grip=18)
    design.pose("above_b", j1=55, j2=20, j3=10, j4=-30, j5=0, j6=90, grip=18)
    design.pose("at_b", j1=55, j2=35, j3=10, j4=-45, j5=0, j6=90, grip=18)
    design.pose("released_b", j1=55, j2=35, j3=10, j4=-45, j5=0, j6=90, grip=0)
    design.pose("clear_b", j1=55, j2=20, j3=10, j4=-30, j5=0, j6=90, grip=0)
    design.pose("flourish", j1=0, j2=-15, j3=-40, j4=55, j5=30, j6=180, grip=10)

    design.animation("pick_and_place", [
        ("home", 0), ("above_a", 2.0), ("at_a", 3.4), ("gripped_a", 4.2), ("lift_a", 5.4),
        ("above_b", 7.4), ("at_b", 8.8), ("released_b", 9.6), ("clear_b", 10.8),
        ("flourish", 12.6), ("home", 14.5), ("home", 15.5),
    ], loop=True, check=True)
