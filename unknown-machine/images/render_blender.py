"""Studio renders of the actuator for the README, from STEVE's per-body mesh export (Blender 4.x, Cycles).

STEVE's viewer draws the dark anodised parts almost black, so the README stills are lit here instead: key, rim
and fill area lights over a dark graded floor, metal materials per part. Geometry is STEVE's, unchanged.

    # bodies-mesh.zip from generate_model(download=["bodies_mesh"]), unzipped into <mesh dir>
    blender -b -P unknown-machine/images/render_blender.py -- <mesh dir> <out.png> [assembled|internals|lathe]
    blender -b -P ... -- <mesh dir> <out.png> lathe x,y,z zoom   # look at a point (model mm) from closer in
    ... lathe x,y,z zoom -20:carriage,tool_post                  # and move those instances along X (a pose)

`lathe` renders the mini-lathe design (lathe-kit/), which is already Z-up, from the operator's side.
"""
import json
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector

args = sys.argv[sys.argv.index("--") + 1:]
mesh_dir, out, view = Path(args[0]), args[1], (args[2] if len(args) > 2 else "assembled")
HIDE = {"internals": ("housing", "front_flange", "screw_", "end_bell", "rear_cap", "stator")}.get(view, ())

# (base colour, metallic, roughness) by instance-name prefix; first match wins.
LOOK = [
    ("gib", ((0.72, 0.52, 0.22), 1.0, 0.30)),              # brass
    ("tungsten_holder", ((0.45, 0.10, 0.10), 0.85, 0.35)),  # red anodised
    ("grind_hub", ((0.55, 0.56, 0.58), 1.0, 0.30)), ("er16_collet_chuck", ((0.80, 0.80, 0.82), 1.0, 0.18)),
    ("drill_bit", ((0.18, 0.18, 0.20), 1.0, 0.30)), ("tungsten", ((0.62, 0.64, 0.68), 1.0, 0.22)),
    ("handwheel", ((0.80, 0.81, 0.83), 1.0, 0.28)), ("cross_wheel", ((0.80, 0.81, 0.83), 1.0, 0.28)),
    ("carriage_wheel", ((0.80, 0.81, 0.83), 1.0, 0.28)), ("compound_wheel", ((0.80, 0.81, 0.83), 1.0, 0.28)),
    ("tailstock_wheel", ((0.80, 0.81, 0.83), 1.0, 0.28)),
    ("workpiece", ((0.88, 0.88, 0.89), 1.0, 0.18)),
    ("tool_post", ((0.20, 0.21, 0.23), 1.0, 0.35)),
    ("bed", ((0.05, 0.055, 0.065), 0.8, 0.38)), ("headstock_plate", ((0.05, 0.055, 0.065), 0.8, 0.38)),
    ("foot", ((0.05, 0.055, 0.065), 0.8, 0.38)), ("leadscrew_bracket", ((0.05, 0.055, 0.065), 0.8, 0.38)),
    ("carriage", ((0.11, 0.13, 0.17), 0.85, 0.32)), ("cross_slide", ((0.11, 0.13, 0.17), 0.85, 0.32)), ("compound", ((0.11, 0.13, 0.17), 0.85, 0.32)),
    ("top_slide", ((0.11, 0.13, 0.17), 0.85, 0.32)), ("tailstock", ((0.11, 0.13, 0.17), 0.85, 0.32)),
    ("chuck", ((0.16, 0.17, 0.19), 0.9, 0.40)),
    ("read_head", ((0.10, 0.36, 0.20), 0.0, 0.45)),
    ("housing", ((0.11, 0.13, 0.17), 0.85, 0.32)),        # dark blue-grey anodise
    ("end_bell", ((0.11, 0.13, 0.17), 0.85, 0.32)),
    ("rear_cap", ((0.11, 0.13, 0.17), 0.85, 0.40)),
    ("pedestal", ((0.11, 0.13, 0.17), 0.85, 0.36)),
    ("front_flange", ((0.14, 0.16, 0.22), 0.85, 0.30)),
    ("carrier", ((0.80, 0.80, 0.80), 1.0, 0.24)),          # 303 stainless, brushed
    ("chuck_backplate", ((0.80, 0.80, 0.80), 1.0, 0.24)),
    ("lathe_chuck", ((0.16, 0.17, 0.19), 0.9, 0.40)),      # cast-iron chuck body, ground jaws
    ("ring_gear", ((0.30, 0.31, 0.33), 1.0, 0.34)),
    ("sun", ((0.62, 0.62, 0.63), 1.0, 0.28)),
    ("planet_", ((0.62, 0.62, 0.63), 1.0, 0.28)),
    ("stator", ((0.20, 0.21, 0.23), 0.6, 0.55)),
    ("motor_rotor", ((0.45, 0.47, 0.50), 1.0, 0.35)),
    ("encoder_disk", ((0.85, 0.85, 0.86), 1.0, 0.12)),
]
DEFAULT = ((0.78, 0.78, 0.79), 1.0, 0.22)                # bearings, pins, screws, dowels: bright steel

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
materials = {}


def material(look):
    if look not in materials:
        (r, g, b), metal, rough = look
        m = bpy.data.materials.new(f"m{len(materials)}")
        m.use_nodes = True
        p = m.node_tree.nodes["Principled BSDF"]
        p.inputs["Base Color"].default_value = (r, g, b, 1)
        p.inputs["Metallic"].default_value = metal
        p.inputs["Roughness"].default_value = rough
        materials[look] = m
    return materials[look]


parts = bpy.data.objects.new("actuator", None)
scene.collection.objects.link(parts)
for item in json.load(open(mesh_dir / "manifest.json"))["items"]:
    name = item["instance"].split("/")[-1]
    if any(name.startswith(h) for h in HIDE):
        continue
    bpy.ops.wm.stl_import(filepath=str(mesh_dir / item["file"]))
    ob = bpy.context.selected_objects[0]
    ob.name = name
    ob.parent = parts
    if len(args) > 5 and any(name.startswith(n) for n in args[5].split(":")[1].split(",")):
        ob.location.x += float(args[5].split(":")[0])     # mm, before the parent's scale
    bpy.ops.object.shade_auto_smooth(angle=math.radians(35))
    look = next((v for k, v in LOOK if name.startswith(k)), DEFAULT)
    ob.data.materials.append(material(look))

# Design frame is mm with the pedestal toward -Y: stand it up (pedestal down, output toward the camera side).
parts.scale = (0.001, 0.001, 0.001)
parts.rotation_euler = (0, 0, 0) if view == "lathe" else (math.radians(90), 0, 0)
bpy.context.view_layer.update()
pts = [ob.matrix_world @ Vector(c) for ob in parts.children for c in ob.bound_box]
lo = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
hi = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
parts.location = (-(lo.x + hi.x) / 2, -(lo.y + hi.y) / 2, -lo.z)
centre = Vector((0, 0, (hi.z - lo.z) / 2))
size = (hi - lo).length
zoom = 1.0
if len(args) > 4:                                    # close-up on a point given in model mm
    focus = Vector([float(v) for v in args[3].split(",")]) * 0.001
    centre = focus + Vector(parts.location)
    zoom = float(args[4])

# Floor: dark, slightly glossy, fading into the background.
bpy.ops.mesh.primitive_plane_add(size=40 * size)
floor = bpy.context.object
fm = bpy.data.materials.new("floor")
fm.use_nodes = True
fp = fm.node_tree.nodes["Principled BSDF"]
fp.inputs["Base Color"].default_value = (0.018, 0.020, 0.025, 1)
fp.inputs["Roughness"].default_value = 0.35
floor.data.materials.append(fm)

world = bpy.data.worlds.new("world")
scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.012, 0.014, 0.018, 1)
world.node_tree.nodes["Background"].inputs["Strength"].default_value = 1.0


def area_light(name, loc, power, size_m, colour):
    data = bpy.data.lights.new(name, "AREA")
    data.energy, data.size, data.color = power * size ** 2, size_m, colour   # W, scaled to the object's size (m)
    ob = bpy.data.objects.new(name, data)
    scene.collection.objects.link(ob)
    ob.location = Vector(loc) * size
    direction = centre - ob.location
    ob.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


area_light("key", (-1.6, -1.8, 2.0), 260, 1.0 * size, (1.0, 0.96, 0.90))     # warm key, front left above
area_light("rim", (1.8, 1.6, 1.4), 320, 0.6 * size, (0.80, 0.88, 1.0))      # cool rim, behind right
area_light("fill", (2.0, -1.4, 0.4), 60, 1.2 * size, (0.90, 0.94, 1.0))    # soft fill, right low
area_light("top", (0.0, 0.0, 2.6), 90, 1.5 * size, (1.0, 1.0, 1.0))        # softbox over the top

cam_data = bpy.data.cameras.new("cam")
cam_data.lens = 70
cam = bpy.data.objects.new("cam", cam_data)
scene.collection.objects.link(cam)
cam.location = centre + (Vector((0.55, -1.9, 0.95)) if view == "lathe" else Vector((-1.15, -2.05, 1.05))) * size * zoom
cam.rotation_euler = (centre - cam.location).to_track_quat("-Z", "Y").to_euler()
scene.camera = cam

scene.render.engine = "CYCLES"
scene.cycles.samples = 160
scene.cycles.use_denoising = True
scene.render.resolution_x, scene.render.resolution_y = 1600, 1200
scene.view_settings.view_transform = "AgX"
scene.view_settings.look = "AgX - Medium High Contrast"
scene.render.filepath = out
bpy.ops.render.render(write_still=True)
