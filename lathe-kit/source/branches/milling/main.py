"""Manual mini lathe, branch "milling": the milling attachment.

The headstock plate comes off the bed and the milling column bolts on in its place (the same 4 x M6). The
actuator moves from the plate onto the column's Z slide (the same 4 x M8 through its pedestal), turned so the
spindle points down, with an ER20 collet adapter on the output disk in place of the chuck backplate. The work
goes in a 60 mm vise on the cross-slide in place of the compound. No separate T-slot table: the lathe's own
slides are the mill's axes.

- X: the carriage on the bed (SFU1204 ball screw, 200-line dial, 0.02 mm a line).
- Y: the cross-slide (SFU1204, 0.02 mm a line).
- Z: the column's slide on its own SFU1204 ball screw, handwheel on top (0.02 mm a line), with a drag plug and
  a lock lever so the head can't run down under its own weight.
- Spindle: 0-1060 rpm, 18 N m short-term. Slow for small cutters in aluminium (Ø6 at 1060 rpm is 20 m/min):
  this is a steel-and-brass mill with HSS, or bigger cutters and fly cutters in aluminium.

Frame as the lathe: x along the bed, Z up, operator at -Y. The actuator and its tooling are modelled in the
actuator's frame and placed with one turn (180 degrees about (1, 1, 0): its axis -> -Z, its pedestal -> -X).
"""
from steve import Design
from lathe_params import ball_lead, carriage_x, mill_spindle_x, mill_spindle_y, mill_head_z
from links import actuator
from components.bed import bed_c as bed
from components.bed_foot import bed_foot
from components.carriage import carriage
from components.carriage_nut import carriage_nut
from components.cross_screw import cross_screw
from components.cross_nut import cross_nut
from components.way_cover_left import way_cover_left
from components.way_cover_right import way_cover_right
from components.gib import gib
from components.cross_slide import cross_slide
from components.leadscrew import leadscrew
from components.leadscrew_bracket import leadscrew_bracket
from components.handwheel_200 import handwheel_200
from components.mill_column import mill_column
from components.z_slide import z_slide
from components.z_screw import z_screw
from components.z_nut import z_nut
from components.er20_mill_adapter import er20_mill_adapter
from components.end_mill import end_mill
from components.mill_vise import mill_vise
from components.mill_vise_jaw import mill_vise_jaw
from components.mill_vise_screw import mill_vise_screw
from components.mill_workpiece import mill_workpiece

MILL = ((mill_spindle_x, mill_spindle_y, mill_head_z), ((1, 1, 0), 180))   # actuator frame -> spindle down
xc = carriage_x + 35
ball_mm_per_degree = ball_lead / 360

design = Design("Manual mini lathe (unknown-machine accessory catalogue)")
design.add(actuator(), at=MILL, name="headstock")
design.add(er20_mill_adapter, at=MILL, name="er20_mill_adapter")
design.add(end_mill, at=MILL, name="end_mill")
for part in (bed, carriage, carriage_nut, gib, way_cover_left, way_cover_right, cross_slide, cross_screw, cross_nut,
             leadscrew, mill_column, z_slide, z_screw, z_nut, mill_vise, mill_vise_jaw, mill_vise_screw,
             mill_workpiece):
    design.add(part)
design.add(bed_foot, name="foot_left")
design.add(bed_foot, at=(390, 0, 0), name="foot_right")
design.add(leadscrew_bracket, name="leadscrew_bracket_right")
design.add(leadscrew_bracket, at=(-485, 0, 0), name="leadscrew_bracket_left")
design.add(handwheel_200, at=((460, -67.5, -120), ("Y", 90)), name="carriage_wheel")
design.add(handwheel_200, at=((xc, -101, -75.2), ("X", 90)), name="cross_wheel")
design.add(handwheel_200, at=(79, mill_spindle_y, 245), name="z_wheel")

# --- Motion: X carriage, Y cross-slide, Z column slide; every one a 4 mm-lead ball screw ---
design.revolute("leadscrew_turn", "bed", "leadscrew", axis=((0, -67.5, -120), (1, 0, 0)))
design.rigid("carriage_wheel_key", "leadscrew", "carriage_wheel")
design.slider("carriage_slide", "bed", "carriage", axis="X", limits=(-30, 60))
design.couple("carriage_feed", {"leadscrew_turn": 1, "carriage_slide": -ball_mm_per_degree})
design.rigid("carriage_nut_fit", "carriage", "carriage_nut")
design.rigid("gib_fit", "carriage", "gib")
design.rigid("way_cover_left_screws", "carriage", "way_cover_left")
design.rigid("way_cover_right_screws", "carriage", "way_cover_right")
design.rigid("cross_nut_fit", "carriage", "cross_nut")
design.slider("cross_travel", "carriage", "cross_slide", axis="Y", limits=(-40, 0))
design.revolute("cross_wheel_turn", "cross_slide", "cross_wheel", axis=((xc, -101, -75.2), (0, -1, 0)))
design.rigid("cross_screw_key", "cross_wheel", "cross_screw")
design.couple("cross_feed", {"cross_wheel_turn": 1, "cross_travel": ball_mm_per_degree})
design.rigid("vise_on_stud", "cross_slide", "mill_vise")
design.rigid("vise_jaw_closed", "mill_vise", "mill_vise_jaw")
design.rigid("vise_screw_in", "mill_vise_jaw", "mill_vise_screw")
design.rigid("work_clamped", "mill_vise", "mill_workpiece")
design.revolute("z_turn", "mill_column", "z_screw", axis=((79, mill_spindle_y, 0), (0, 0, 1)))
design.rigid("z_wheel_key", "z_screw", "z_wheel")
design.slider("z_travel", "mill_column", "z_slide", axis="Z", limits=(-80, 40))
design.couple("z_feed", {"z_turn": 1, "z_travel": -ball_mm_per_degree})
design.rigid("z_nut_fit", "z_slide", "z_nut")
design.rigid("head_on_slide", "z_slide", "headstock")
design.rigid("adapter_on_disk", "headstock", "er20_mill_adapter")
design.rigid("cutter_in_collet", "er20_mill_adapter", "end_mill")

# Slotting: carry on the slot 20 mm along X, lift the cutter 5 mm, come back, go down again.
design.animation("slotting", [({"carriage_feed": 0, "z_feed": 0}, 0), ({"carriage_feed": 1800}, 6),
                              ({"z_feed": -450}, 7), ({"carriage_feed": 0}, 11), ({"z_feed": 0}, 12)],
                 loop=True, easing="ease")

# --- Designed contacts; everything else must not touch ---
for a, b in [("mill_column", "bed"), ("foot_*", "bed"), ("leadscrew_bracket_left", "mill_column"),
             ("z_slide", "mill_column"), ("z_nut", "z_slide"), ("z_screw", "z_nut"), ("z_screw", "mill_column"),
             ("z_screw", "z_wheel"), ("z_wheel", "mill_column"), ("headstock", "z_slide"),
             ("er20_mill_adapter", "headstock"), ("end_mill", "er20_mill_adapter"),
             ("carriage", "bed"), ("gib", "carriage"), ("gib", "bed"),
             ("carriage_nut", "carriage"), ("leadscrew", "carriage_nut"), ("way_cover_*", "carriage"),
             ("cross_nut", "carriage"), ("cross_screw", "cross_nut"), ("cross_screw", "cross_slide"),
             ("cross_screw", "cross_wheel"), ("cross_screw", "carriage"), ("cross_slide", "carriage"),
             ("mill_vise", "cross_slide"), ("mill_vise_jaw", "mill_vise"), ("mill_vise_screw", "mill_vise"),
             ("mill_vise_screw", "mill_vise_jaw"), ("mill_workpiece", "mill_vise"),
             ("mill_workpiece", "mill_vise_jaw"),
             ("leadscrew_bracket_*", "bed"), ("leadscrew", "leadscrew_bracket_*"), ("leadscrew", "carriage"),
             ("leadscrew", "carriage_wheel"), ("carriage_wheel", "leadscrew_bracket_right"),
             ("cross_wheel", "cross_slide")]:
    design.contact(a, b, kind="seated")
design.fit_check("fit", motion=False)

result = design.result()
