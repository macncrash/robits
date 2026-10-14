from steve import Component
from params import *  # noqa: F403

iso4762_socket_head_cap_screw_m5x30 = Component("iso4762_socket_head_cap_screw_m5x30", name="ISO 4762 hexagon socket head cap screw, M5 x 30")
# Standard part iso4762_socket_head_cap_screw_m5x30 from step.parts (MIT, github.com/earthtojake/step.parts): https://www.step.parts/parts/iso4762_socket_head_cap_screw_m5x30 · sha256 b0452d734dbd9fde05914f9866c34c69ec9cc253f26e39c04573c02297d82c42
iso4762_socket_head_cap_screw_m5x30.import_step("import_1", "b0452d734dbd9fde05914f9866c34c69ec9cc253f26e39c04573c02297d82c42", name="ISO 4762 hexagon socket head cap screw, M5 x 30")
iso4762_socket_head_cap_screw_m5x30.material("stainless-304", finish="brushed")  # A2-70
