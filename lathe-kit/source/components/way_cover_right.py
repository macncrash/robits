"""Right way cover: printed shield screwed to the carriage's right end (2 x M4 x 10), covering 40 mm of the
ways and the leadscrew toward the tailstock. Same section as the left one; prints the same way."""
from steve import Component
from lathe_shapes import way_cover
from lathe_params import carriage_x

way_cover_right = Component("way_cover_right", name="Way cover, right (3D printed)")
way_cover_right.add("cover", way_cover(carriage_x + 70, carriage_x + 110), name="Way cover")
way_cover_right.material("petg", color="#d2691e")
