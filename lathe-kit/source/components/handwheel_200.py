"""Handwheel with graduated dial for the SFU1204 ball screws (carriage, cross-slide; the mill's Z): same wheel
and crank as the Tr10 ones, with a Ø60 dial ring of 200 lines (4 mm lead / 200 = 0.02 mm a line, a long line
every 10 = 0.2 mm). A spring-loaded brass drag plug in each screw's bracket stops the low-friction ball screw
from being back-driven by the cut when the wheel is let go; lock the slide for heavy cuts."""
from steve import Component
from lathe_shapes import handwheel_solid

handwheel_200 = Component("handwheel_200", name="Handwheel with 200-line dial (ball screws)")
handwheel_200.add("handwheel", handwheel_solid(30, 200, 10), name="Handwheel")
handwheel_200.material("aluminum-6061-t6", finish="brushed", color="#c9ccd1")
