"""Urethane tyre on the lower band wheel, Ø238 x Ø250 x 20, crowned flat (a separate component only so it renders in
its own colour)."""
from steve import Component
from bandsaw_shapes import wheel
from bandsaw_params import lower_z

_, tyre = wheel(lower_z, 14)
lower_tyre = Component("lower_tyre", name="Urethane tyre (lower wheel)")
lower_tyre.add("tyre", tyre, name="Urethane tyre")
lower_tyre.material("pc", color="#9a3b1e")                  # urethane: appearance only
