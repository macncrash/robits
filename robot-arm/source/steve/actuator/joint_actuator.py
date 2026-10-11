"""Joint actuator (press3)

Rotary joint actuator reverse-engineered from the press3 "rotary joint actuator" render: a finned
motor can with a knurled encoder cap, a stainless clamp band with lug and thumb screw, a top rail,
a front flange with a blue anodized bolt ring and a recessed stainless output (toothed strain-wave
ring + hub with bore). Optional foot mount (pedestal) as in the render.

Frame: axis along +Z, centred on the origin; the output faces +Z at z = length / 2. The top rail
points to +Y and the foot (pedestal = 1) to -Y.
Parameters: diameter (flange OD), length (overall), pedestal (1 = foot mount, 0 = bare joint module
used inside the robot arm), fin_count (cooling grooves).
"""
import math
import cadquery as cq
from steve import Model

diameter = 120  # mm Flange outer diameter
length = 130  # mm Overall length along the axis
pedestal = 1  # count 1 = foot mount as in the render, 0 = bare joint module
fin_count = 9  # count Cooling grooves on the motor can

model = Model()

R = diameter / 2
L = length
z0 = -L / 2


def cyl(r, h, z):
    return cq.Solid.makeCylinder(r, h, cq.Vector(0, 0, z), cq.Vector(0, 0, 1))


def ring(ro, ri, h, z):
    return cyl(ro, h, z).cut(cyl(ri, h, z))


# Motor can: knurled encoder cap, rear housing, finned section, front flange.
cap = cyl(0.70 * R, 0.10 * L, z0)
for k in range(40):
    a = 360.0 * k / 40
    tooth = cq.Solid.makeBox(0.025 * R, 0.035 * R, 0.08 * L, cq.Vector(0.70 * R - 0.018 * R, -0.0175 * R, z0 + 0.01 * L))
    cap = cap.cut(tooth.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), a))
rear = cyl(0.86 * R, 0.20 * L, z0 + 0.10 * L)
fins = cyl(0.80 * R, 0.32 * L, z0 + 0.30 * L)
pitch = 0.32 * L / (fin_count + 1)
for k in range(1, fin_count + 1):
    fins = fins.cut(ring(0.81 * R, 0.75 * R, 0.35 * pitch, z0 + 0.30 * L + k * pitch - 0.175 * pitch))
front = cyl(R, 0.25 * L, z0 + 0.70 * L)
housing = cap.fuse(rear).fuse(fins).fuse(front)
# Output recess in the front face.
housing = housing.cut(cyl(0.66 * R, 0.16 * L, z0 + 0.84 * L + 0.001))
# Top rail along the can.
rail = cq.Solid.makeBox(0.30 * R, 0.16 * R, 0.52 * L, cq.Vector(-0.15 * R, 0.80 * R, z0 + 0.18 * L))
housing = housing.fuse(rail).clean()
model.add("housing", housing, name="Housing")

# Blue bolt ring on the front face, four counterbored screws.
bolt_r = 0.83 * R
accent = ring(R, 0.66 * R, 0.05 * L, z0 + 0.95 * L)
screws = None
for k in range(4):
    a = math.radians(45 + 90 * k)
    x, y = bolt_r * math.cos(a), bolt_r * math.sin(a)
    accent = accent.cut(cq.Solid.makeCylinder(0.075 * R, 0.05 * L, cq.Vector(x, y, z0 + 0.95 * L), cq.Vector(0, 0, 1)))
    head = cq.Solid.makeCylinder(0.055 * R, 0.04 * L, cq.Vector(x, y, z0 + 0.95 * L), cq.Vector(0, 0, 1))
    head = head.cut(cq.Solid.makeBox(0.05 * R, 0.05 * R, 0.03 * L, cq.Vector(x - 0.025 * R, y - 0.025 * R, z0 + 0.96 * L)))
    screws = head if screws is None else screws.fuse(head)
model.add("accent", accent, op="new", name="Blue bolt ring")

# Stainless output: toothed strain-wave ring, disk and hub with bore.
teeth = ring(0.64 * R, 0.56 * R, 0.10 * L, z0 + 0.86 * L)
for k in range(72):
    groove = cq.Solid.makeBox(0.03 * R, 0.012 * R, 0.10 * L, cq.Vector(0.555 * R, -0.006 * R, z0 + 0.86 * L))
    teeth = teeth.cut(groove.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), 5.0 * k))
disk = cyl(0.56 * R, 0.03 * L, z0 + 0.86 * L)
hub = cyl(0.18 * R, 0.12 * L, z0 + 0.86 * L)
output = teeth.fuse(disk).fuse(hub).cut(cyl(0.07 * R, 0.2 * L, z0 + 0.8 * L)).clean()
model.add("output", output, op="new", name="Output flange")

# Stainless clamp band with lug and knurled thumb screw (on +X), plus a rail cap screw.
band = ring(0.90 * R, 0.80 * R, 0.08 * L, z0 + 0.62 * L)
lug = cq.Solid.makeBox(0.22 * R, 0.20 * R, 0.08 * L, cq.Vector(0.82 * R, -0.10 * R, z0 + 0.62 * L))
thumb = cq.Solid.makeCylinder(0.07 * R, 0.16 * R, cq.Vector(0.93 * R, 0.10 * R, z0 + 0.66 * L), cq.Vector(0, 1, 0))
rail_screw = cq.Solid.makeCylinder(0.07 * R, 0.10 * R, cq.Vector(0, 0.96 * R, z0 + 0.62 * L), cq.Vector(0, 1, 0))
hardware = band.fuse(lug).fuse(thumb).fuse(rail_screw).fuse(screws).clean()
model.add("hardware", hardware, op="new", name="Clamp band and screws")

if pedestal:
    foot_y = -1.08 * R
    block = cq.Solid.makeBox(0.90 * R, 0.80 * R + 0.02, 0.70 * L, cq.Vector(-0.45 * R, foot_y, z0 + 0.15 * L))
    block = block.cut(cyl(0.86 * R, 0.72 * L, z0 + 0.14 * L)).cut(cyl(R, 0.30 * L, z0 + 0.70 * L))
    window = cq.Solid.makeBox(1.0 * R, 0.18 * R, 0.16 * L, cq.Vector(-0.5 * R, foot_y + 0.28 * R, z0 + 0.25 * L))
    block = block.cut(window)
    plate = (cq.Workplane("XZ", origin=(0, foot_y, 0)).center(0, 0)
             .rect(1.6 * R, 1.05 * L).extrude(0.12 * R)
             .edges("|Y").fillet(0.12 * R)
             .faces("<Y").workplane()
             .rect(1.3 * R, 0.85 * L, forConstruction=True).vertices().hole(0.12 * R)
             .val())
    foot = block.fuse(plate).clean()
    model.add("foot", foot, op="new", name="Foot mount")

model.material("aluminum-6061-t6", finish="anodized", color="#1b2030")
model.material("aluminum-6061-t6", bodies=["accent"], finish="anodized", color="#2f6fd6")
model.material("stainless-304", bodies=["output", "hardware"], finish="brushed")

result = model.result()
