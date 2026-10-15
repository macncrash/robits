from steve import Component
from params import *  # noqa: F403

iso4762_socket_head_cap_screw_m4x16 = Component("iso4762_socket_head_cap_screw_m4x16", name="ISO 4762 M4 x 16 (end bell screw, A2-70)")
# Standard part iso4762_socket_head_cap_screw_m4x16 from step.parts (MIT, github.com/earthtojake/step.parts): https://www.step.parts/parts/iso4762_socket_head_cap_screw_m4x16 · sha256 b5c01866b687475f93099b025611fbfea69928940574c990406316eb832640bc
iso4762_socket_head_cap_screw_m4x16.import_step("import_1", "b5c01866b687475f93099b025611fbfea69928940574c990406316eb832640bc", name="ISO 4762 M4 x 16")
iso4762_socket_head_cap_screw_m4x16.material("stainless-304", finish="brushed")   # A2-70
