from steve import Component
from params import *  # noqa: F403

bearing_6001_2rs_sealed_simple = Component("bearing_6001_2rs_sealed_simple", name="Rear bearing 6001-2RS (12 x 28 x 8)")
# Standard part bearing_6001_2rs_sealed_simple from step.parts (MIT, github.com/earthtojake/step.parts): https://www.step.parts/parts/bearing_6001_2rs_sealed_simple · sha256 4ec6075a1b382c5be23de54b9aff3a5c29f7ca90d02a6a27feeb9b0059066cbf
bearing_6001_2rs_sealed_simple.import_step("import_1", "4ec6075a1b382c5be23de54b9aff3a5c29f7ca90d02a6a27feeb9b0059066cbf", name="Bearing")
bearing_6001_2rs_sealed_simple.material("steel-1c60", finish="polished")
