"""Coolant tank (20 l) with a small submersible-style pump on the lid and its outlet; the hose runs up the back
leg to the nozzle clipped on the upper guard (hose and nozzle not modelled)."""
from steve import Component
from coldsaw_shapes import box, zcyl

tank = box(-200, -100, -650, 200, 200, -500)
pump = zcyl(30, -500, -440, 120, 50).fuse(zcyl(6, -440, -400, 120, 50))
coolant_tank = Component("coolant_tank", name="Coolant tank and pump")
coolant_tank.add("tank", tank, name="Tank")
coolant_tank.add("pump", pump.clean(), name="Pump and outlet")
coolant_tank.material("steel-s235jr", color="#3b4a3a")
