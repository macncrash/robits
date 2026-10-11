"""Output bearing, thin-section 61806 (30 x 42 x 7), carries the planet carrier in the bulkhead."""
from steve import Component
from shapes import ball_bearing

output_bearing = Component("output_bearing", name="Output bearing 61806")
outer, inner, balls = ball_bearing(15, 21, 7, 37)
output_bearing.add("outer", outer, name="Outer race")
output_bearing.add("inner", inner, op="new", name="Inner race")
output_bearing.add("balls", balls, op="new", name="Balls")
output_bearing.material("steel-1c60", finish="polished")
