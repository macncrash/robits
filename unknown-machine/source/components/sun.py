"""Sun gear on the motor shaft."""
import cadquery as cq
from steve import Component
from shapes import cyl
from params import module, sun_teeth, face_width
from gearing import spur_gear

sun = Component("sun", name="Sun gear")
gear = spur_gear(module, sun_teeth, face_width).val().cut(cyl(6, face_width, 0))   # bore = shaft OD 12
sun.add("teeth", gear.translate(cq.Vector(0, 0, 48)), name="Teeth")
sun.material("steel-s235jr", finish="machined")
