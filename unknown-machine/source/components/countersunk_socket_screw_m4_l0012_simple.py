from steve import Component
from params import *  # noqa: F403

countersunk_socket_screw_m4_l0012_simple = Component("countersunk_socket_screw_m4_l0012_simple", name="ISO 10642 countersunk socket screw, M4 x 12")
# Standard part countersunk_socket_screw_m4_l0012_simple from step.parts (MIT, github.com/earthtojake/step.parts): https://www.step.parts/parts/countersunk_socket_screw_m4_l0012_simple · sha256 ccfae69e6c481fa0886dedd0dcc21241c1a1769e53cd1f825d424de4965380e6
countersunk_socket_screw_m4_l0012_simple.import_step("import_1", "ccfae69e6c481fa0886dedd0dcc21241c1a1769e53cd1f825d424de4965380e6", name="Screw")
countersunk_socket_screw_m4_l0012_simple.material("stainless-304", finish="brushed")   # A2-70
