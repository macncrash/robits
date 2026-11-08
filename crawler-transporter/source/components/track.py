"""One shoe band. A stadium ring: the shoe wrapped around the sprocket and the idler.

The links are not a chain. A closed loop of shoes cannot be a joint tree, so the
band is rigid and the wheels turn inside it. Pitch radius is the mid-shoe line.
"""
from steve import Component
from params import center_z, inner_r, ix, outer_r, shoe_w, sx

track = Component("track", name="Track band")

span = ix - sx
mid_x = (ix + sx) / 2.0
y0 = -shoe_w / 2.0

track.cylinder("rear_out", outer_r, shoe_w, at=(sx, y0, center_z), direction=(0, 1, 0))
track.cylinder("front_out", outer_r, shoe_w, at=(ix, y0, center_z), direction=(0, 1, 0), op="join")
track.box("mid_out", span, shoe_w, 2 * outer_r, at=(mid_x, 0, center_z), op="join")

track.cylinder("rear_in", inner_r, shoe_w + 20, at=(sx, y0 - 10, center_z), direction=(0, 1, 0), op="cut")
track.cylinder("front_in", inner_r, shoe_w + 20, at=(ix, y0 - 10, center_z), direction=(0, 1, 0), op="cut")
track.box("mid_in", span, shoe_w + 20, 2 * inner_r, at=(mid_x, 0, center_z), op="cut")

track.material("steel-a36", finish="painted", color="#2a2e33")
