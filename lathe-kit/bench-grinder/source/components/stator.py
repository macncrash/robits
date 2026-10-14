"""Kollmorgen KBM-17H01-B00 frameless stator (bought, the same as the actuator's): OD 84.963, length 57.80
(catalog p. 19); the 52 mm bore is an ESTIMATE. Bonded into the barrel, centred on the motor (x -28.9..28.9)."""
from steve import Component
from grinder_shapes import xring

stator = Component("stator", name="Stator KBM-17H01-B00 (Kollmorgen)")
stator.add("stator", xring(42.4815, 26, -28.9, 28.9), name="Stator (sleeve, laminations, encapsulated windings)")
stator.material("steel-s235jr", color="#5b5f66")
