"""Stainless clamp band around the housing front section, with the lever lug on top."""
from steve import Component
from shapes import ring, box, xcyl

clamp_band = Component("clamp_band", name="Clamp band")
band = ring(60, 56, 12, 20).fuse(box(-8, 57, 20, 8, 74, 32)).cut(xcyl(2.6, -9, 9, 68, 26))
clamp_band.add("band", band.clean(), name="Band")
clamp_band.material("stainless-304", finish="brushed")
