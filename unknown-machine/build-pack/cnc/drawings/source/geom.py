"""Geometry side of the AM drawing set: STEP loading, exact hidden-line projection, section cuts, feature queries.

Runs on pythonocc-core (FreeCAD 1.1 bundles it: /Applications/FreeCAD.app/Contents/Resources/bin/python).
Every dimension on the sheets is measured from these STEP solids (STEVE design 02e31a10 revision 48 export),
never typed in: `cyl()` / `plane_z()` find the face and fail loudly if the model doesn't have it.
"""
import math
import os

import numpy as np
from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_SOLID, TopAbs_FACE, TopAbs_EDGE, TopAbs_WIRE
from OCC.Core.TopoDS import topods
from OCC.Core.BRepAdaptor import BRepAdaptor_Curve, BRepAdaptor_Surface
from OCC.Core.GCPnts import GCPnts_QuasiUniformDeflection, GCPnts_TangentialDeflection
from OCC.Core.GeomAbs import GeomAbs_Line, GeomAbs_Cylinder, GeomAbs_Plane, GeomAbs_Cone
from OCC.Core.HLRBRep import HLRBRep_Algo, HLRBRep_HLRToShape, HLRBRep_PolyAlgo, HLRBRep_PolyHLRToShape
from OCC.Core.HLRAlgo import HLRAlgo_Projector
from OCC.Core.gp import gp_Ax2, gp_Pnt, gp_Dir, gp_Vec, gp_Trsf, gp_Pln, gp_Ax3
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeHalfSpace
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut, BRepAlgoAPI_Common
from OCC.Core.BRepTools import BRepTools_WireExplorer, breptools
from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh
from OCC.Core.Bnd import Bnd_Box
from OCC.Core.BRepBndLib import brepbndlib
from OCC.Core.BRepGProp import brepgprop
from OCC.Core.GProp import GProp_GProps

HERE = os.path.dirname(os.path.abspath(__file__))
STEP_DIR = os.path.normpath(os.path.join(HERE, "..", "..", "step"))


def explore(shape, kind):
    e = TopExp_Explorer(shape, kind)
    while e.More():
        yield e.Current()
        e.Next()


def load(name, solid=None):
    r = STEPControl_Reader()
    assert r.ReadFile(os.path.join(STEP_DIR, name)) == 1, name
    r.TransferRoots()
    s = r.OneShape()
    solids = [topods.Solid(x) for x in explore(s, TopAbs_SOLID)]
    if solid is None:
        assert len(solids) == 1, (name, len(solids))
        return solids[0]
    return solid(solids)


def bbox(shape):
    b = Bnd_Box()
    brepbndlib.Add(shape, b, False)
    return b.Get()


def volume(shape):
    p = GProp_GProps()
    brepgprop.VolumeProperties(shape, p)
    return p.Mass()


# ---------------------------------------------------------------- views
class View:
    """An orthographic view: viewer on `towards` (model vector from the part to the eye), paper +x is `right`.
    Paper +y = towards x right. Points project as p2 = ((p-o).right, (p-o).up)."""

    def __init__(self, towards, right, origin=(0, 0, 0)):
        t = np.array(towards, float); t /= np.linalg.norm(t)
        r = np.array(right, float); r /= np.linalg.norm(r)
        assert abs(t @ r) < 1e-9
        self.t, self.r, self.u = t, r, np.cross(t, r)
        self.o = np.array(origin, float)

    def p(self, pt):
        d = np.array(pt, float) - self.o
        return np.array([d @ self.r, d @ self.u])

    def depth(self, pt):
        return (np.array(pt, float) - self.o) @ self.t

    def ax2(self):
        return gp_Ax2(gp_Pnt(*self.o), gp_Dir(*self.t), gp_Dir(*self.r))


def _edges_to_polylines(compound, deflection=0.01):
    out = []
    if compound is None or compound.IsNull():
        return out
    for e in explore(compound, TopAbs_EDGE):
        e = topods.Edge(e)
        c = BRepAdaptor_Curve(e)
        if c.GetType() == GeomAbs_Line:
            a, b = c.Value(c.FirstParameter()), c.Value(c.LastParameter())
            out.append(np.array([[a.X(), a.Y()], [b.X(), b.Y()]]))
            continue
        d = GCPnts_TangentialDeflection(c, 0.05, deflection)
        pts = [d.Value(i + 1) for i in range(d.NbPoints())]
        if len(pts) >= 2:
            out.append(np.array([[q.X(), q.Y()] for q in pts]))
    return out


def project(shape, view, hidden=True, smooth=False, poly=False):
    """Exact (or, poly=True, mesh-based) hidden-line removal. Returns dict of polyline lists in paper-model mm."""
    if poly:
        BRepMesh_IncrementalMesh(shape, 0.01, False, 0.2, True)
        algo = HLRBRep_PolyAlgo()
        algo.Load(shape)
        algo.Projector(HLRAlgo_Projector(view.ax2()))
        algo.Update()
        h = HLRBRep_PolyHLRToShape()
        h.Update(algo)
    else:
        algo = HLRBRep_Algo()
        algo.Add(shape)
        algo.Projector(HLRAlgo_Projector(view.ax2()))
        algo.Update()
        algo.Hide()
        h = HLRBRep_HLRToShape(algo)
    res = {"visible": _edges_to_polylines(h.VCompound()) + _edges_to_polylines(h.OutLineVCompound())}
    if smooth:
        res["smooth"] = _edges_to_polylines(h.Rg1LineVCompound())
    if hidden:
        res["hidden"] = _edges_to_polylines(h.HCompound()) + _edges_to_polylines(h.OutLineHCompound())
    return res


def section(shape, view, plane_point, keep_towards=False):
    """Cut by the plane through plane_point normal to the view direction; removes the material between the plane
    and the viewer. Returns (cut solid, list of cut-face loops in paper mm)."""
    n = view.t
    p = np.array(plane_point, float)
    # half space on the viewer's side of the plane
    pl = gp_Pln(gp_Pnt(*p), gp_Dir(*n))
    face = BRepBuilderAPI_MakeFace(pl, -1000, 1000, -1000, 1000).Face()
    ref = p + n * 10
    hs = BRepPrimAPI_MakeHalfSpace(face, gp_Pnt(*ref)).Solid()
    cut = BRepAlgoAPI_Cut(shape, hs).Shape()
    loops = []
    for f in explore(cut, TopAbs_FACE):
        f = topods.Face(f)
        s = BRepAdaptor_Surface(f)
        if s.GetType() != GeomAbs_Plane:
            continue
        ax = s.Plane().Axis()
        dn = np.array([ax.Direction().X(), ax.Direction().Y(), ax.Direction().Z()])
        loc = np.array([ax.Location().X(), ax.Location().Y(), ax.Location().Z()])
        if abs(abs(dn @ n) - 1) > 1e-7 or abs((loc - p) @ n) > 1e-6:
            continue
        face_loops = []
        for w in explore(f, TopAbs_WIRE):
            pts = []
            we = BRepTools_WireExplorer(topods.Wire(w), f)
            while we.More():
                e = we.Current()
                c = BRepAdaptor_Curve(e)
                if c.GetType() == GeomAbs_Line:
                    q = [c.Value(c.FirstParameter()), c.Value(c.LastParameter())]
                else:
                    d = GCPnts_TangentialDeflection(c, 0.05, 0.01)
                    q = [d.Value(i + 1) for i in range(d.NbPoints())]
                q = [view.p((x.X(), x.Y(), x.Z())) for x in q]
                if e.Orientation() == 1:  # reversed
                    q = q[::-1]
                pts.extend(q)
                we.Next()
            face_loops.append(np.array(pts))
        loops.append(face_loops)
    return cut, loops


# ---------------------------------------------------------------- feature queries
def faces(shape):
    for f in explore(shape, TopAbs_FACE):
        yield topods.Face(f)


def _face_range(f, axis):
    b = Bnd_Box()
    brepbndlib.Add(f, b, False)
    x0, y0, z0, x1, y1, z1 = b.Get()
    ax = np.array(axis, float)
    lo, hi = np.array([x0, y0, z0]), np.array([x1, y1, z1])
    corners = [np.array([a, b_, c]) for a in (x0, x1) for b_ in (y0, y1) for c in (z0, z1)]
    v = [c @ ax for c in corners]
    return min(v), max(v)


def cylinders(shape):
    out = []
    for f in faces(shape):
        s = BRepAdaptor_Surface(f)
        if s.GetType() != GeomAbs_Cylinder:
            continue
        c = s.Cylinder()
        ax = c.Axis()
        d = np.array([ax.Direction().X(), ax.Direction().Y(), ax.Direction().Z()])
        if d[np.argmax(abs(d))] < 0:
            d = -d
        loc = np.array([ax.Location().X(), ax.Location().Y(), ax.Location().Z()])
        # extent along the axis from the face's vertices/bbox (bbox is conservative on curved faces: use uv bounds)
        u0, u1, v0, v1 = breptools.UVBounds(f)
        pa = s.Value(u0, v0); pb = s.Value(u0, v1)
        ta = (np.array([pa.X(), pa.Y(), pa.Z()]) - loc) @ d
        tb = (np.array([pb.X(), pb.Y(), pb.Z()]) - loc) @ d
        lo, hi = sorted((ta, tb))
        base = loc - (loc @ d) * d if abs(d @ np.array([0, 0, 1])) > 0.999 else loc
        out.append(dict(r=c.Radius(), axis=d, loc=loc, t0=loc @ d + lo, t1=loc @ d + hi, face=f,
                        span=math.degrees(u1 - u0)))
    return out


class Q:
    """Queries on one solid. Lengths in mm in the model frame."""

    def __init__(self, shape):
        self.shape = shape
        self.cyls = cylinders(shape)

    def cyl(self, d, axis=(0, 0, 1), at=None, z=None, tol=0.02, n=None):
        """Cylindrical faces of diameter ~d with axis parallel to `axis`, optionally through point `at` (x, y) /
        containing axial coordinate z. Returns merged dict(d, z0, z1, centres) of the matches."""
        ax = np.array(axis, float); ax /= np.linalg.norm(ax)
        m = []
        for c in self.cyls:
            if abs(2 * c["r"] - d) > tol or abs(abs(c["axis"] @ ax) - 1) > 1e-6:
                continue
            perp = c["loc"] - (c["loc"] @ ax) * ax
            if at is not None:
                tgt = np.array(at, float)
                tgt = tgt - (tgt @ ax) * ax
                if np.linalg.norm(perp - tgt) > 0.05:
                    continue
            if z is not None and not (c["t0"] - 1e-6 <= z <= c["t1"] + 1e-6):
                continue
            m.append((c, perp))
        if not m:
            raise LookupError(f"no cylinder Ø{d} axis {axis} at {at} z {z}")
        centres = []
        for c, perp in m:
            if not any(np.linalg.norm(perp - q) < 0.05 for q in centres):
                centres.append(perp)
        if n is not None and len(centres) != n:
            raise LookupError(f"Ø{d}: expected {n} axes, found {len(centres)}")
        return dict(d=2 * m[0][0]["r"], z0=min(c["t0"] for c, _ in m), z1=max(c["t1"] for c, _ in m),
                    centres=centres, n=len(centres))

    def planes(self, normal=(0, 0, 1)):
        nn = np.array(normal, float)
        out = []
        for f in faces(self.shape):
            s = BRepAdaptor_Surface(f)
            if s.GetType() != GeomAbs_Plane:
                continue
            ax = s.Plane().Axis()
            d = np.array([ax.Direction().X(), ax.Direction().Y(), ax.Direction().Z()])
            if abs(abs(d @ nn) - 1) > 1e-7:
                continue
            loc = np.array([ax.Location().X(), ax.Location().Y(), ax.Location().Z()])
            out.append(round(loc @ nn, 4))
        return sorted(set(out))

    def plane(self, value, normal=(0, 0, 1), tol=0.005):
        for v in self.planes(normal):
            if abs(v - value) <= tol:
                return v
        raise LookupError(f"no plane at {value} normal {normal}; have {self.planes(normal)}")

    def cones(self):
        out = []
        for f in faces(self.shape):
            s = BRepAdaptor_Surface(f)
            if s.GetType() == GeomAbs_Cone:
                c = s.Cone()
                out.append(dict(half_angle=math.degrees(c.SemiAngle()), r=c.RefRadius(),
                                loc=(c.Location().X(), c.Location().Y(), c.Location().Z())))
        return out


def radial_extent(shape):
    """Min and max distance of the shape's vertices from the Z axis."""
    from OCC.Core.TopAbs import TopAbs_VERTEX
    from OCC.Core.BRep import BRep_Tool
    rs = []
    for v in explore(shape, TopAbs_VERTEX):
        p = BRep_Tool.Pnt(topods.Vertex(v))
        rs.append(math.hypot(p.X(), p.Y()))
    return min(rs), max(rs)
