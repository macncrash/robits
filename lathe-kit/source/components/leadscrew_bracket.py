"""Leadscrew bracket: bolts to the bed's front face (2 x M6) and carries the screw in a bronze bush; the right
one has the zero line for the dial engraved by the dial's rim. Modelled at the right end (x 440..460)."""
from steve import Component
from lathe_shapes import box, xcyl

bracket = box(440, -80, -135, 460, -50, -98)
bracket = bracket.cut(xcyl(5.05, 439, 461, -67.5, -120))
bracket = bracket.cut(box(459.6, -67.7, -102, 460, -67.3, -98))
leadscrew_bracket = Component("leadscrew_bracket", name="Leadscrew bracket")
leadscrew_bracket.add("bracket", bracket.clean(), name="Bracket")
leadscrew_bracket.material("aluminum-6061-t6", finish="anodized", color="#15171c")
