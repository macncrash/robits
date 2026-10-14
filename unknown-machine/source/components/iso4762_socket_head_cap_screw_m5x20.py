from steve import Component
from params import *  # noqa: F403

iso4762_socket_head_cap_screw_m5x20 = Component("iso4762_socket_head_cap_screw_m5x20", name="ISO 4762 hexagon socket head cap screw, M5 x 20")
# Standard part iso4762_socket_head_cap_screw_m5x20 from step.parts (MIT, github.com/earthtojake/step.parts): https://www.step.parts/parts/iso4762_socket_head_cap_screw_m5x20 · sha256 bac42c77e9e668699efa72502f61009c8ff6d897a8cf5ea3576254da6fb89c4c
iso4762_socket_head_cap_screw_m5x20.import_step("import_1", "bac42c77e9e668699efa72502f61009c8ff6d897a8cf5ea3576254da6fb89c4c", name="ISO 4762 hexagon socket head cap screw, M5 x 20")
iso4762_socket_head_cap_screw_m5x20.material("stainless-304", finish="brushed")  # A2-70
