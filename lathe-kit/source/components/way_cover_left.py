"""Left way cover: printed shield screwed to the carriage's left end (2 x M4 x 10), covering 40 mm of the ways
and the leadscrew toward the headstock, where the chips and the grinding grit fall. A wear part: print another
and swap it in two minutes. 40 long, so it still clears the headstock plate at the carriage's left-hand stop."""
from steve import Component
from lathe_shapes import way_cover
from lathe_params import carriage_x

way_cover_left = Component("way_cover_left", name="Way cover, left (3D printed)")
way_cover_left.add("cover", way_cover(carriage_x, carriage_x - 40), name="Way cover")
way_cover_left.material("petg", color="#d2691e")
