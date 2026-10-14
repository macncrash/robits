"""Spindle: one 42CrMo4 through-shaft, wheel at each end. Ø30 seat for the KBM rotor (bonded, centred on the
stator), Ø24 shoulders the bearings bank against, Ø20 journals for the 6204 bearings and out to the wheels;
M20 x 1.5 ends (right-hand thread on the right, left-hand on the left, so the nuts tighten as the wheels cut)."""
from steve import Component
from grinder_shapes import xcyl

body = xcyl(15, -15.1, 15.1)
for s in (1, -1):
    body = body.fuse(xcyl(12, min(s * 15.1, s * 46), max(s * 15.1, s * 46)))
    body = body.fuse(xcyl(10, min(s * 46, s * 151), max(s * 46, s * 151)))
shaft = Component("shaft", name="Spindle shaft (42CrMo4)")
shaft.add("shaft", body.clean(), name="Spindle")
shaft.material("steel-1c60", finish="polished")
