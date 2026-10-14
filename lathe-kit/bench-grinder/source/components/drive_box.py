"""Drive box on the front of the column: the same 240 Vac servo drive as the actuator (speed-limited to 3450 rpm
in its setup), mains switch, green start, red mushroom e-stop. Strapped to the column."""
from steve import Component
from grinder_shapes import box, ycyl

body = box(-90, -131, 580, 90, -50.8, 780)
stop = ycyl(15, -141, -131, 50, 740).fuse(ycyl(9, -137, -131, 50, 740))
start = ycyl(9, -137, -131, -40, 740)
drive_box = Component("drive_box", name="Drive box (servo drive, switches)")
drive_box.add("box", body, name="Enclosure")
drive_box.add("estop", stop.clean(), op="new", name="E-stop")
drive_box.add("start", start, op="new", name="Start button")
drive_box.material("steel-s235jr", color="#3a3f48")
drive_box.material("pc", bodies=["estop"], color="#c0262d")
drive_box.material("pc", bodies=["start"], color="#2c8a3c")
