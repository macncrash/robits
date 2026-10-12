from steve import Component
from params import *  # noqa: F403

iso4762_socket_head_cap_screw_m5x25 = Component("iso4762_socket_head_cap_screw_m5x25", name="ISO 4762 hexagon socket head cap screw, M5 x 25")
# Standard part iso4762_socket_head_cap_screw_m5x25 from step.parts (MIT, github.com/earthtojake/step.parts): https://www.step.parts/parts/iso4762_socket_head_cap_screw_m5x25 · sha256 21774ada0b9f8fedccae6da24e50798e4bd61a7213adb69f819adde40360ad60
iso4762_socket_head_cap_screw_m5x25.import_step("import_1", "21774ada0b9f8fedccae6da24e50798e4bd61a7213adb69f819adde40360ad60", name="ISO 4762 hexagon socket head cap screw, M5 x 25")
iso4762_socket_head_cap_screw_m5x25.material("stainless-304", finish="brushed")  # A2-70
