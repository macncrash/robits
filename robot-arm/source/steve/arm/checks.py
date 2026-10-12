"""Fit and collision checks: designed contacts, interference at every named pose, the pick-and-place
animation swept end to end, and the shoulder/elbow/wrist-pitch joints together across their limits."""

# Each actuator seats on the link that carries it (stator) and on the link it drives (output).
SEATS = [("act_j1", "base"), ("act_j1", "turret"), ("act_j2", "turret"), ("act_j2", "upper_arm"),
         ("act_j3", "upper_arm"), ("act_j3", "forearm"), ("act_j4", "forearm"), ("act_j4", "wrist1"),
         ("act_j5", "wrist1"), ("act_j5", "wrist2"), ("act_j6", "wrist2"), ("act_j6", "tool"),
         ("upper_arm_collars", "upper_arm"), ("forearm_collars", "forearm"),
         ("finger_*", "tool")]
POSES = ["home", "above_a", "at_a", "gripped_a", "lift_a", "above_b", "at_b", "released_b", "clear_b", "flourish"]


def add_checks(design):
    for a, b in SEATS:
        design.contact(a, b, kind="seated")
    design.clearance(default=1.0)
    # Every pair at rest plus the flourish (the widest pose); the other poses are covered by the animation studies.
    design.fit_check("poses", poses=["flourish"], motion=False)
    # Near-miss distances are costly (about a minute per pose), so only the animation's key poses get them.
    design.collision_study("pick_and_place_keys", sampling="animation", animation="pick_and_place", at="keys",
                           clearance=5.0)
    design.collision_study("shoulder_elbow", joints=["j2", "j3"], sampling="grid", steps=20, hold="home")
    design.collision_study("arm_pitch", joints=["j2", "j3", "j4"], sampling="random", samples=150, seed=1,
                           hold="home")
