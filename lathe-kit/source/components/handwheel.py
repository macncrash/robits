"""Handwheel with graduated dial for the Tr10 x 2 screws (compound and tailstock quill): steel hub,
satin-aluminium Ø40 dial ring with 100 engraved lines (0.02 mm each, a long line every 10), 70 mm wheel with a
crank handle. Built along +Z from its mounting face at the origin; each instance is turned onto its screw's axis."""
from steve import Component
from lathe_shapes import handwheel_solid

handwheel = Component("handwheel", name="Handwheel with 100-line dial")
handwheel.add("handwheel", handwheel_solid(20, 100, 10), name="Handwheel")
handwheel.material("aluminum-6061-t6", finish="brushed", color="#c9ccd1")
