"""Ø40 mild-steel bar in the vise, cut: two pieces either side of the 2.2 mm kerf; the right piece is against the
length stop."""
from steve import Component
from coldsaw_shapes import xcyl
from coldsaw_params import table_z, stock_d

r = stock_d / 2
stock = Component("stock", name="Bar Ø40 (work)")
stock.add("left", xcyl(r, -300, -1.1, -r, table_z + r), name="Bar, left")
stock.add("right", xcyl(r, 1.1, 300, -r, table_z + r), name="Bar, right (cut off)")
stock.material("steel-s235jr", finish="machined")
