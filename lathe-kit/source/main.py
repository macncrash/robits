"""Manual mini lathe built on the unknown-machine joint actuator: the accessory catalogue.

Hand controls only, like a classic hobby lathe ("what is old is new again"): every slide is moved by a Tr10 x 2
screw and a handwheel with a 100-line dial (0.02 mm per line), the compound has a +-60 degree scale, and the
tailstock quill is engraved in mm.

- Headstock: the actuator (linked design, revision 36) on its pedestal, on a headstock plate, with the 303
  backplate and a bought 80 mm 3-jaw chuck. 5:1 planetary, 18 N m short-term / 10 N m continuous at the spindle,
  up to 1060 rpm: low speed and high torque, right for HSS on steel (Ø20 mild steel: about 400-480 rpm).
- Bed: 6061 dovetail flat bed, 500 long, centre height 98 (swing 196), two feet.
- Carriage on a brass gib, moved by the leadscrew and the handwheel at the right end.
- Cross-slide and compound (swivel +-60 degrees, top slide), 4-way tool post for 8 mm HSS on centre.
- Tailstock with a 20 mm quill (MT1), MT1 live centre, quill screw and handwheel, quill and base locks.

Frame: spindle axis along +X (y 0, z 0), Z up, operator at -Y. The actuator, backplate and chuck are modelled
in the actuator's own frame and placed with one turn (120 degrees about (1, 1, 1): its axis -> X, its up -> Z).
"""
from steve import Design
from lathe_params import screw_pitch, carriage_x, tool_y, tailstock_x
from links import actuator, chuck_backplate
from components.headstock_plate import headstock_plate
from components.bed import bed_c as bed
from components.bed_foot import bed_foot
from components.carriage import carriage
from components.gib import gib
from components.cross_slide import cross_slide
from components.compound import compound
from components.top_slide import top_slide
from components.tool_post import tool_post
from components.tool_bit import tool_bit
from components.tailstock import tailstock
from components.quill import quill_c as quill
from components.live_center import live_center
from components.leadscrew import leadscrew
from components.leadscrew_bracket import leadscrew_bracket
from components.handwheel import handwheel
from components.lathe_chuck_80 import lathe_chuck_80
from components.workpiece import workpiece

TURN = ((0, 0, 0), ((1, 1, 1), 120))                 # actuator frame -> lathe frame
xc = carriage_x + 35                                  # carriage / cross-slide / compound centre line
mm_per_degree = screw_pitch / 360

design = Design("Manual mini lathe (unknown-machine accessory catalogue)")
design.add(actuator(), at=TURN, name="headstock")
design.add(chuck_backplate(), at=TURN, name="chuck_backplate")
design.add(lathe_chuck_80, at=TURN, name="chuck")
for part in (headstock_plate, bed, carriage, gib, cross_slide, compound, top_slide, tool_post, tool_bit, tailstock,
             quill, live_center, leadscrew, workpiece):
    design.add(part)
design.add(bed_foot, name="foot_left")
design.add(bed_foot, at=(390, 0, 0), name="foot_right")
design.add(leadscrew_bracket, name="leadscrew_bracket_right")
design.add(leadscrew_bracket, at=(-485, 0, 0), name="leadscrew_bracket_left")
# Handwheels: each turned from +Z onto its screw's axis, mounting face against its bearing.
design.add(handwheel, at=((460, -67.5, -120), ("Y", 90)), name="carriage_wheel")
design.add(handwheel, at=((xc, -101, -75.2), ("X", 90)), name="cross_wheel")
design.add(handwheel, at=((xc + 51, tool_y, -43.2), ("Y", 90)), name="compound_wheel")
design.add(handwheel, at=((tailstock_x + 80, 0, 0), ("Y", 90)), name="tailstock_wheel")

# --- Motion: every slide is screw-driven from its handwheel (2 mm per turn) ---
design.revolute("leadscrew_turn", "bed", "leadscrew", axis=((0, -67.5, -120), (1, 0, 0)))
design.rigid("carriage_wheel_key", "leadscrew", "carriage_wheel")
design.slider("carriage_slide", "bed", "carriage", axis="X", limits=(-45, 60))
design.couple("carriage_feed", {"leadscrew_turn": 1, "carriage_slide": -mm_per_degree})
design.rigid("gib_fit", "carriage", "gib")
design.slider("cross_travel", "carriage", "cross_slide", axis="Y", limits=(-40, 0))
design.revolute("cross_wheel_turn", "cross_slide", "cross_wheel", axis=((xc, -101, -75.2), (0, -1, 0)))
design.couple("cross_feed", {"cross_wheel_turn": 1, "cross_travel": mm_per_degree})
design.revolute("compound_angle", "cross_slide", "compound", axis=((xc, tool_y, -56), (0, 0, 1)), limits=(-60, 60))
design.slider("top_travel", "compound", "top_slide", axis="X", limits=(-20, 20))
design.revolute("compound_wheel_turn", "top_slide", "compound_wheel", axis=((xc + 51, tool_y, -43.2), (1, 0, 0)))
design.couple("compound_feed", {"compound_wheel_turn": 1, "top_travel": mm_per_degree})
design.rigid("tool_post_stud", "top_slide", "tool_post")
design.rigid("tool_clamped", "tool_post", "tool_bit")
design.slider("tailstock_slide", "bed", "tailstock", axis="X", limits=(0, 60))
design.slider("quill_travel", "tailstock", "quill", axis="X", limits=(0, 30))
design.rigid("centre_in_taper", "quill", "live_center")
design.revolute("tailstock_wheel_turn", "tailstock", "tailstock_wheel", axis=((tailstock_x + 80, 0, 0), (1, 0, 0)))
design.couple("quill_feed", {"tailstock_wheel_turn": 1, "quill_travel": mm_per_degree})

design.pose("ready", carriage_feed=0, cross_feed=-900)
design.animation("turning_pass", [({"carriage_feed": 0, "cross_feed": -900}, 0), ({"cross_feed": 0}, 1.5),
                                  ({"carriage_feed": 7200}, 7), ({"cross_feed": -900}, 8),
                                  ({"carriage_feed": 0}, 10)], loop=True, easing="ease")

# --- Designed contacts; everything else must not touch ---
for a, b in [("headstock", "headstock_plate"), ("headstock_plate", "bed"), ("foot_*", "bed"),
             ("chuck_backplate", "headstock"), ("chuck", "chuck_backplate"), ("workpiece", "chuck"),
             ("workpiece", "live_center"), ("carriage", "bed"), ("gib", "carriage"), ("gib", "bed"),
             ("cross_slide", "carriage"), ("compound", "cross_slide"), ("top_slide", "compound"),
             ("tool_post", "top_slide"), ("tool_bit", "tool_post"), ("tool_bit", "workpiece"),
             ("tailstock", "bed"), ("quill", "tailstock"), ("live_center", "quill"),
             ("leadscrew_bracket_*", "bed"), ("leadscrew", "leadscrew_bracket_*"), ("leadscrew", "carriage"),
             ("leadscrew", "carriage_wheel"), ("carriage_wheel", "leadscrew_bracket_right"),
             ("leadscrew_bracket_left", "headstock_plate"), ("cross_wheel", "cross_slide"),
             ("compound_wheel", "top_slide"), ("tailstock_wheel", "tailstock")]:
    design.contact(a, b, kind="seated")
design.fit_check("fit", motion=False)

result = design.result()
