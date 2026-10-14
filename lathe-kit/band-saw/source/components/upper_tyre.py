"""Urethane tyre on the upper band wheel, Ø238 x Ø250 x 20, crowned flat (a separate component only so it renders in
its own colour)."""
from steve import Component
from bandsaw_shapes import wheel
from bandsaw_params import upper_z

_, tyre = wheel(upper_z, 14)
upper_tyre = Component("upper_tyre", name="Urethane tyre (upper wheel)")
upper_tyre.add("tyre", tyre, name="Urethane tyre")
upper_tyre.material("pc", color="#9a3b1e")                  # urethane: appearance only
