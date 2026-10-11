"""Rear end bell: closes the can, carries the rear bearing and the encoder read head."""
from steve import Component
from shapes import ring, cyl

end_bell = Component("end_bell", name="Rear end bell")
bell = cyl(51.5, 12, -48).cut(cyl(14, 10, -46)).cut(cyl(7, 14, -49))   # 6001 seat (28 mm), shaft hole
bell = bell.fuse(ring(42, 30, 3, -36))                                  # spigot into the housing bore
end_bell.add("bell", bell.clean(), name="End bell")
end_bell.material("aluminum-6061-t6", finish="anodized", color="#1b2030")
