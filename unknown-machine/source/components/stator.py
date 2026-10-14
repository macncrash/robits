"""Kollmorgen KBM-17H01-B00 frameless stator (bought), bonded into the housing bore against the depth-stop ledge.

Envelope from the KBM selection guide p. 19: OD 84.963 mm, length 57.80 mm (sleeve, laminations and encapsulated
windings). The bore (52 mm here) is an ESTIMATE: take it from Kollmorgen's 3D model (kollmorgen.com/kbm).
Front face 2 mm behind the bulkhead floor (Kollmorgen's minimum end-turn clearance), so z -28.8..29.
"""
from steve import Component
from shapes import ring

stator_od, stator_len, stator_front = 84.963, 57.80, 29.0
stator_bore = 52.0   # ESTIMATE, not in the catalog

stator = Component("stator", name="Stator KBM-17H01-B00 (Kollmorgen)")
stator.add("stator", ring(stator_od / 2, stator_bore / 2, stator_len, stator_front - stator_len),
           name="Stator (sleeve, laminations, encapsulated windings)")
stator.material("steel-s235jr", color="#5b5f66")   # mixed steel / copper / epoxy; catalog mass 1.05 kg with rotor
