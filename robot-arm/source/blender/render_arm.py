"""Render the STEVE robot-arm export in Blender: stills plus an animated walk-around.

Usage (from the robot-arm/ folder):
  blender -b -P source/blender/render_arm.py -- exports/stl/arm <out_dir> [--stills-only] [--preview]

<mesh_dir> is the STEVE bodies_mesh export (manifest.json + one STL per body, design frame, mm,
zero pose). Joint pivots and the pick-and-place keyframes mirror source/steve/arm/motion.py.
The animation is written straight to <out_dir>/robot_arm_walkaround.mp4 (H.264, 8 Mbit/s).
"""
import json
import math
import os
import sys

import bpy
from mathutils import Matrix, Vector

argv = sys.argv[sys.argv.index("--") + 1:]
MESH_DIR, OUT_DIR = argv[0], argv[1]
STILLS_ONLY = "--stills-only" in argv
PREVIEW = "--preview" in argv
os.makedirs(OUT_DIR, exist_ok=True)

FPS = 30
DURATION = 17.0  # s; the animation is 15.5 s, then a hold while the camera finishes its orbit
MM = 0.001

# ---------------------------------------------------------------- kinematics (mirrors motion.py)
SHOULDER_Z, ELBOW_Z, FORE_LEN, W_Y, W2_X = 300, 725, 400, 127, 556
JOINTS = [  # name, parent, pivot on the axis (mm, zero pose), axis
    ("j1", None, (0, 0, 0), "Z"),
    ("j2", "j1", (0, 0, SHOULDER_Z), "Y"),
    ("j3", "j2", (0, 0, ELBOW_Z), "Y"),
    ("j4", "j3", (FORE_LEN, 0, ELBOW_Z), "Y"),
    ("j5", "j4", (FORE_LEN + 95, W_Y, ELBOW_Z), "X"),
    ("j6", "j5", (W2_X, W_Y, 600), "Z"),
    ("grip_l", "j6", (W2_X, W_Y, 520), "+X"),
    ("grip_r", "j6", (W2_X, W_Y, 520), "-X"),
]
REVOLUTE = [(n, a) for n, _, _, a in JOINTS if n.startswith("j")]
INSTANCE_LINK = {
    "base": None, "act_j1": None,
    "turret": "j1", "act_j2": "j1",
    "upper_arm": "j2", "upper_arm_collars": "j2", "act_j3": "j2",
    "forearm": "j3", "forearm_collars": "j3", "act_j4": "j3",
    "wrist1": "j4", "act_j5": "j4",
    "wrist2": "j5", "act_j6": "j5",
    "tool": "j6", "finger_l": "grip_l", "finger_r": "grip_r",
}
POSES = {
    "home": dict(j1=0, j2=0, j3=0, j4=0, j5=0, j6=0, grip=0),
    "above_a": dict(j1=-35, j2=20, j3=10, j4=-30, j5=0, j6=0, grip=0),
    "at_a": dict(j1=-35, j2=35, j3=10, j4=-45, j5=0, j6=0, grip=0),
    "gripped_a": dict(j1=-35, j2=35, j3=10, j4=-45, j5=0, j6=0, grip=18),
    "lift_a": dict(j1=-35, j2=20, j3=10, j4=-30, j5=0, j6=0, grip=18),
    "above_b": dict(j1=55, j2=20, j3=10, j4=-30, j5=0, j6=90, grip=18),
    "at_b": dict(j1=55, j2=35, j3=10, j4=-45, j5=0, j6=90, grip=18),
    "released_b": dict(j1=55, j2=35, j3=10, j4=-45, j5=0, j6=90, grip=0),
    "clear_b": dict(j1=55, j2=20, j3=10, j4=-30, j5=0, j6=90, grip=0),
    "flourish": dict(j1=0, j2=-15, j3=-40, j4=55, j5=30, j6=180, grip=10),
}
KEYS = [("home", 0), ("above_a", 2.0), ("at_a", 3.4), ("gripped_a", 4.2), ("lift_a", 5.4),
        ("above_b", 7.4), ("at_b", 8.8), ("released_b", 9.6), ("clear_b", 10.8),
        ("flourish", 12.6), ("home", 14.5), ("home", 15.5)]
T_GRIP, T_RELEASE = 4.2, 9.6
PART_CENTER = (W2_X, W_Y, 433)  # between the pads in the zero pose (mm), fixed to the tool
PART_SIZE = 30  # mm cube

# ---------------------------------------------------------------- scene and materials
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.fps = FPS
scene.frame_start = 1
scene.frame_end = int(DURATION * FPS)


def srgb(hexstr):
    h = hexstr.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c)


def mat(name, hexcolor, metallic=0.0, rough=0.4, coat=0.0, aniso=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*srgb(hexcolor), 1)
    b.inputs["Metallic"].default_value = metallic
    b.inputs["Roughness"].default_value = rough
    b.inputs["Coat Weight"].default_value = coat
    b.inputs["Coat Roughness"].default_value = 0.08
    b.inputs["Anisotropic"].default_value = aniso
    return m


MATS = {
    "blue": mat("Blue anodized 6061", "#2f6fd6", 0.85, 0.28, coat=0.3),
    "dark": mat("Black anodized aluminium", "#22262e", 0.75, 0.32, coat=0.5),
    "gun": mat("Gunmetal anodized tube", "#3a3f48", 0.85, 0.22, coat=0.6),
    "steel": mat("Brushed stainless 304", "#c9ccd1", 1.0, 0.22, aniso=0.6),
    "rubber": mat("TPU 98A cable", "#121418", 0.0, 0.6),
    "pad": mat("TPU 60A pad", "#2f6fd6", 0.0, 0.55),
    "floor": mat("Floor", "#b9bec6", 0.0, 0.5),
    "plinth": mat("Plinth", "#4a5059", 0.2, 0.35),
    "part": mat("Workpiece", "#f08a24", 0.1, 0.35),
}


def material_for(item):
    body, material = item["body"], item.get("material") or ""
    if body == "accent":
        return MATS["blue"]
    if body == "pad":
        return MATS["pad"]
    if body == "cable":
        return MATS["rubber"]
    if material.startswith("stainless"):
        return MATS["steel"]
    if item["instance"] in ("upper_arm", "forearm"):
        return MATS["gun"]
    return MATS["dark"]


# ---------------------------------------------------------------- joints as empties
empties = {}
for name, parent, pivot, _ in JOINTS:
    e = bpy.data.objects.new(f"J_{name}", None)
    e.empty_display_size = 0.05
    e.location = Vector(pivot) * MM
    scene.collection.objects.link(e)
    if parent:
        e.parent = empties[parent]
        e.matrix_parent_inverse = Matrix.Translation(empties[parent].location).inverted()
    empties[name] = e
bpy.context.view_layer.update()
REST = {n: e.matrix_world.copy() for n, e in empties.items()}


def attach(ob, empty):
    ob.parent = empty
    ob.matrix_parent_inverse = REST[empty.name[2:]].inverted()


def set_pose(values):
    for j, axis in REVOLUTE:
        r = [0.0, 0.0, 0.0]
        r["XYZ".index(axis)] = math.radians(values[j])
        empties[j].rotation_euler = r
    g = values["grip"] * MM
    base_l = Vector(JOINTS[6][2]) * MM
    base_r = Vector(JOINTS[7][2]) * MM
    empties["grip_l"].location = base_l + Vector((g, 0, 0))
    empties["grip_r"].location = base_r - Vector((g, 0, 0))
    bpy.context.view_layer.update()


def world_point(rest_point_mm, joint, values):
    """World position of a point that sat at rest_point_mm in the zero pose and is fixed to `joint`."""
    set_pose(values)
    m = empties[joint].matrix_world @ REST[joint].inverted()
    return m @ (Vector(rest_point_mm) * MM), m.to_euler()


# ---------------------------------------------------------------- meshes
manifest = json.load(open(os.path.join(MESH_DIR, "manifest.json")))
for item in manifest["items"]:
    bpy.ops.wm.stl_import(filepath=os.path.join(MESH_DIR, item["file"]), global_scale=MM)
    ob = bpy.context.selected_objects[0]
    ob.name = f"{item['instance']}.{item['body']}"
    ob.data.materials.clear()
    ob.data.materials.append(material_for(item))
    bpy.ops.object.shade_auto_smooth(angle=math.radians(35))
    link = INSTANCE_LINK.get(item["instance"])
    if link:
        attach(ob, empties[link])

# ---------------------------------------------------------------- floor, plinths, workpiece
bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 0, 0))
bpy.context.object.data.materials.append(MATS["floor"])

pos_a, rot_a = world_point(PART_CENTER, "j6", POSES["gripped_a"])
pos_b, rot_b = world_point(PART_CENTER, "j6", POSES["at_b"])
half = PART_SIZE * MM / 2
for tag, p in (("A", pos_a), ("B", pos_b)):
    h = p.z - half
    bpy.ops.mesh.primitive_cylinder_add(radius=0.07, depth=h, location=(p.x, p.y, h / 2), vertices=96)
    plinth = bpy.context.object
    plinth.name = f"plinth_{tag}"
    plinth.data.materials.append(MATS["plinth"])
    bpy.ops.object.shade_smooth()
print(f"pick point A {tuple(round(v * 1000) for v in pos_a)} mm, B {tuple(round(v * 1000) for v in pos_b)} mm")


def make_part(name, loc, rot_z):
    bpy.ops.mesh.primitive_cube_add(size=PART_SIZE * MM, location=loc, rotation=(0, 0, rot_z))
    ob = bpy.context.object
    ob.name = name
    bev = ob.modifiers.new("bevel", "BEVEL")
    bev.width = 0.002
    bev.segments = 3
    ob.data.materials.append(MATS["part"])
    return ob


part_a = make_part("part_at_A", pos_a, rot_a.z)
part_b = make_part("part_at_B", pos_b, rot_b.z)
set_pose(POSES["home"])
part_c = make_part("part_carried", Vector(PART_CENTER) * MM, 0)
attach(part_c, empties["j6"])

# ---------------------------------------------------------------- camera, lights, world
target = bpy.data.objects.new("target", None)
HOME_TARGET = Vector((0.2, 0.05, 0.5))
target.location = HOME_TARGET
scene.collection.objects.link(target)
cam_data = bpy.data.cameras.new("cam")
cam_data.lens = 40
cam_data.clip_start = 0.05
cam = bpy.data.objects.new("cam", cam_data)
scene.collection.objects.link(cam)
scene.camera = cam
track = cam.constraints.new("TRACK_TO")
track.target = target
track.track_axis = "TRACK_NEGATIVE_Z"
track.up_axis = "UP_Y"


def place_camera(angle_deg, height, radius):
    a = math.radians(angle_deg)
    cam.location = (target.location.x + radius * math.cos(a), target.location.y + radius * math.sin(a), height)


def light(name, loc, energy, size, color):
    ld = bpy.data.lights.new(name, "AREA")
    ld.energy = energy
    ld.color = color
    ld.size = size
    ob = bpy.data.objects.new(name, ld)
    ob.location = loc
    c = ob.constraints.new("TRACK_TO")
    c.target = target
    c.track_axis = "TRACK_NEGATIVE_Z"
    c.up_axis = "UP_Y"
    scene.collection.objects.link(ob)


light("key", (2.0, -2.2, 2.6), 900, 2.0, (1.0, 0.97, 0.93))
light("fill", (-2.4, -0.8, 1.4), 260, 3.0, (0.85, 0.9, 1.0))
light("rim", (-0.6, 2.6, 2.2), 700, 1.5, (0.8, 0.88, 1.0))

world = bpy.data.worlds.new("world")
scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes["Background"]
bg.inputs["Color"].default_value = (*srgb("#7d848e"), 1)
bg.inputs["Strength"].default_value = 0.5

scene.render.engine = "BLENDER_EEVEE_NEXT"
scene.eevee.taa_render_samples = 16 if PREVIEW else 48
scene.eevee.use_raytracing = True
scene.view_settings.view_transform = "AgX"
scene.view_settings.look = "AgX - Medium High Contrast"
scene.render.resolution_x = 1280 if PREVIEW else 1920
scene.render.resolution_y = 720 if PREVIEW else 1080
scene.render.image_settings.file_format = "PNG"

# ---------------------------------------------------------------- stills (before any keyframes)
STILLS = [  # file, pose, camera angle, height, radius, parts visible (A, carried, B)
    ("hero_home", "home", -55, 1.3, 2.7, (True, False, False)),
    ("side_home", "home", -90, 0.7, 2.8, (True, False, False)),
    ("pick_closeup", "gripped_a", -100, 0.45, 0.9, (False, True, False)),
    ("rear_three_quarter", "above_b", 135, 1.5, 2.8, (False, True, False)),
    ("flourish", "flourish", -25, 1.0, 3.0, (False, False, True)),
]
for f_name, pose, ang, h, r, (va, vc, vb) in STILLS:
    set_pose(POSES[pose])
    target.location = pos_a if pose == "gripped_a" else HOME_TARGET
    place_camera(ang, h, r)
    part_a.hide_render, part_c.hide_render, part_b.hide_render = not va, not vc, not vb
    scene.render.filepath = os.path.join(OUT_DIR, f"{f_name}.png")
    bpy.ops.render.render(write_still=True)
target.location = HOME_TARGET

if STILLS_ONLY:
    sys.exit(0)

# ---------------------------------------------------------------- arm keyframes
for pose, t in KEYS:
    f = 1 + round(t * FPS)
    set_pose(POSES[pose])
    for j, _ in REVOLUTE:
        empties[j].keyframe_insert("rotation_euler", frame=f)
    for g in ("grip_l", "grip_r"):
        empties[g].keyframe_insert("location", frame=f)
for e in empties.values():
    if e.animation_data:
        for fc in e.animation_data.action.fcurves:
            for kp in fc.keyframe_points:
                kp.interpolation = "SINE"
                kp.easing = "EASE_IN_OUT"

# Workpiece hand-off: at A until gripped, carried until released, then at B.
f_grip, f_release = 1 + round(T_GRIP * FPS), 1 + round(T_RELEASE * FPS)


def visible_between(ob, first, last):
    for f, hidden in ((0, True), (first, False), (last + 1, True)):
        ob.hide_render = hidden
        ob.hide_viewport = hidden
        ob.keyframe_insert("hide_render", frame=f)
        ob.keyframe_insert("hide_viewport", frame=f)
    for fc in ob.animation_data.action.fcurves:
        for kp in fc.keyframe_points:
            kp.interpolation = "CONSTANT"


visible_between(part_a, 0, f_grip - 1)
visible_between(part_c, f_grip, f_release - 1)
visible_between(part_b, f_release, scene.frame_end + 10)

# ---------------------------------------------------------------- walk-around camera
n = scene.frame_end
for f in range(1, n + 1, 5):
    u = (f - 1) / (n - 1)
    place_camera(-60 + 360.0 * u, 1.3 + 0.35 * math.sin(2 * math.pi * u), 2.85 + 0.25 * math.cos(2 * math.pi * u))
    cam.keyframe_insert("location", frame=f)
place_camera(300, 1.3, 3.1)
cam.keyframe_insert("location", frame=n)

bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT_DIR, "robot_arm_scene.blend"))
# Encode straight to H.264 (no intermediate frames on disk).
scene.render.image_settings.file_format = "FFMPEG"
ff = scene.render.ffmpeg
ff.format = "MPEG4"
ff.codec = "H264"
ff.constant_rate_factor = "NONE"
ff.video_bitrate = 8000
ff.maxrate = 10000
ff.gopsize = FPS
ff.audio_codec = "NONE"
scene.render.filepath = os.path.join(OUT_DIR, "robot_arm_walkaround.mp4")
bpy.ops.render.render(animation=True)
