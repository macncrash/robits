"""Carriage leadscrew: Tr10 x 2 (rolled, steel) along the front of the bed, turned by the handwheel at the
right end; 2 mm of carriage travel per turn."""
from steve import Component
from lathe_shapes import xcyl

leadscrew = Component("leadscrew", name="Leadscrew Tr10 x 2")
leadscrew.add("screw", xcyl(5, -35, 470, -67.5, -120), name="Leadscrew")
leadscrew.material("steel-1c60", finish="machined")
