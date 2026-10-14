"""Top slide: rides the compound's dovetail, carries the 4-way tool post; screw bracket and handwheel on the
right-hand end."""
from steve import Component
from lathe_shapes import box, prism_yz, xcyl
from lathe_params import carriage_x, tool_y

xc = carriage_x + 35
body = box(xc - 45, tool_y - 20, -47.9, xc + 45, tool_y + 20, -24)
groove = [(tool_y - 15.1, -38), (tool_y + 18.1, -38), (tool_y + 15.05, -48.1), (tool_y - 12.05, -48.1)]
body = body.cut(prism_yz(groove, xc - 46, xc + 46))
bracket = box(xc + 45, tool_y - 12, -47.9, xc + 51, tool_y + 12, -21)
bracket = bracket.cut(xcyl(5.05, xc + 44, xc + 52, tool_y, -43.2))
bracket = bracket.cut(box(xc + 50.6, tool_y - 0.2, -25, xc + 51, tool_y + 0.2, -21))   # zero line by the dial's rim
body = body.fuse(bracket)
top_slide = Component("top_slide", name="Top slide")
top_slide.add("top_slide", body.clean(), name="Top slide")
top_slide.material("aluminum-6061-t6", finish="anodized", color="#1b2030")
