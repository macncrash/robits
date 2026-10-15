from steve import Component
from params import *  # noqa: F403

iso4762_socket_head_cap_screw_m2x6 = Component("iso4762_socket_head_cap_screw_m2x6", name="ISO 4762 hexagon socket head cap screw, M2 x 6")
# Standard part iso4762_socket_head_cap_screw_m2x6 from step.parts (MIT, github.com/earthtojake/step.parts): https://www.step.parts/parts/iso4762_socket_head_cap_screw_m2x6 · sha256 3135fd06ae85e89634148a1a50ce0087a3ceb2fb07e091d720c40c54bc0c5a3e
iso4762_socket_head_cap_screw_m2x6.import_step("import_1", "3135fd06ae85e89634148a1a50ce0087a3ceb2fb07e091d720c40c54bc0c5a3e", name="ISO 4762 hexagon socket head cap screw, M2 x 6")
iso4762_socket_head_cap_screw_m2x6.material("stainless-304", finish="brushed")   # A2-70
