"""Disc guard, 2 mm steel sheet, welded: a back wall ring between the platen and the actuator, a rim band round
the whole disc (the face stays open), and a dust hood low on the right-hand side (the disc turns anticlockwise
seen from the front: the work is done on the left, down-running half and the dust is carried round under the
disc into the hood), with a 2.5 in (Ø63) port pointing to the back for a shop vacuum. Two feet bolt it to the
stand top; it doesn't touch the actuator.
"""
from steve import Component
from sander_shapes import box, ycyl, sector_xz
from sander_params import base_z, riser_h

y0, y1 = -99, -74                                    # front edge of the band, back face of the back wall
top = base_z - riser_h
wall = ycyl(135, y1 - 2, y1).cut(ycyl(64, y1 - 2, y1))
band = ycyl(135, y0, y1).cut(ycyl(133, y0, y1))
hood = sector_xz(133, 184, -58, -34, y0, y1).cut(sector_xz(135, 182, -56, -36, y0 + 2, y1 - 2))
port_x, port_z = 104.9, -108.6                       # r 151 at -46 degrees
port = ycyl(31.5, y1 - 2, 40, port_x, port_z)
legs = box(-20, y1 - 2, top, 20, y1, -130).fuse(box(-30, -90, top, 30, y1, top + 3))
legs = legs.fuse(box(-105, y1 - 2, top, -85, y1, -88)).fuse(box(-115, -90, top, -75, y1, top + 3))
guard_body = wall.fuse(band).fuse(hood).fuse(port).fuse(legs)
guard_body = guard_body.cut(sector_xz(130, 182, -56, -36, y0 + 2, y1 - 2))      # band open into the hood
guard_body = guard_body.cut(ycyl(29.5, y1 - 3, 41, port_x, port_z))            # port bore
guard_body = guard_body.cut(ycyl(64, y1 - 3, y1 + 1))                          # keep the centre clear
guard = Component("guard", name="Disc guard and dust hood")
guard.add("guard", guard_body.clean(), name="Guard")
guard.material("steel-s235jr", color="#2b2f36")      # powder coated
