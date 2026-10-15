from steve import Component
from params import *  # noqa: F403

button_head_screw_m3_l0025_simple = Component("button_head_screw_m3_l0025_simple", name="ISO 7380 button head socket screw, M3 x 25 mm")
# Standard part button_head_screw_m3_l0025_simple from step.parts (MIT, github.com/earthtojake/step.parts): https://www.step.parts/parts/button_head_screw_m3_l0025_simple · sha256 8dae5a2cfe58b09784577496d9286d5fad075893505c241d7734cb254be16987
button_head_screw_m3_l0025_simple.import_step("import_1", "8dae5a2cfe58b09784577496d9286d5fad075893505c241d7734cb254be16987", name="ISO 7380 button head socket screw, M3 x 25 mm")
button_head_screw_m3_l0025_simple.material("stainless-304", finish="brushed")   # A2-70
