"""Kollmorgen KBM-17H01-B00 frameless rotor (bought): magnets on a steel hub, bonded to the shaft's hub sleeve.

Catalog p. 19: bore 30.010 mm, length 30.15 mm. The OD (50 mm here) is an ESTIMATE: take it from the 3D model.
Centred on the stator (z -15..15.15), banked against the hub sleeve's shoulder.
"""
from steve import Component
from shapes import ring

rotor_bore, rotor_len, rotor_z = 30.010, 30.15, -15.0
rotor_od = 50.0   # ESTIMATE, not in the catalog

motor_rotor = Component("motor_rotor", name="Rotor KBM-17H01-B00 (Kollmorgen)")
motor_rotor.add("rotor", ring(rotor_od / 2, rotor_bore / 2, rotor_len, rotor_z), name="Rotor (hub + magnets)")
motor_rotor.material("steel-s235jr", color="#8a8f99")   # cold-rolled steel hub with NdFeB magnets
