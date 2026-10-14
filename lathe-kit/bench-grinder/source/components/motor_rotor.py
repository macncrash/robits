"""Kollmorgen KBM-17H01-B00 frameless rotor (bought, the same rotor as the actuator's): bore 30.010, length 30.15
(catalog p. 19); OD 50 is an ESTIMATE. Bonded on the shaft's Ø30 seat, centred in the stator."""
from steve import Component
from grinder_shapes import xring

motor_rotor = Component("motor_rotor", name="Rotor KBM-17H01-B00 (Kollmorgen)")
motor_rotor.add("rotor", xring(25, 15.005, -15.075, 15.075), name="Rotor (hub + magnets)")
motor_rotor.material("steel-s235jr", color="#8a8f99")
