"""Blade tension and tracking: a steel slider behind the upper plate carries the idler wheel's bearings and
rides in the plate's slot. The tension screw (M10) runs up from the slider through the frame's bracket to a
spring stack and a knob; turning the knob pulls the slider up and compresses the spring, and an edge line on the
slider reads against the scale on the plate (6, 10, 13 mm blades). A tracking screw at the back tilts the shaft.
Modelled at nominal tension."""
from steve import Component
from bandsaw_shapes import box, ycyl, zcyl, one
from bandsaw_params import upper_z

block = box(100, 43, upper_z - 25, 150, 73, upper_z + 25).cut(ycyl(10.05, 42, 72.5, 125, upper_z))
block = block.cut(box(149.6, 43, upper_z - 0.3, 150, 73, upper_z + 0.3))    # index line onto the scale
screw = zcyl(5, upper_z + 25, 495, 125, 58)
spring = zcyl(12, 452, 488, 125, 58).cut(zcyl(8, 451, 489, 125, 58))
knob = zcyl(18, 488, 503, 125, 58)
tracking = ycyl(5, 73, 92, 125, upper_z - 15).fuse(ycyl(11, 92, 100, 125, upper_z - 15))
tension_slider = Component("tension_slider", name="Blade tension slider, screw, spring and knobs")
tension_slider.add("slider", one(block.fuse(tracking).clean(), screw.fuse(knob).clean(), spring),
                   name="Slider, tracking knob, tension screw, spring and knob")
tension_slider.material("steel-1c60", finish="machined")
