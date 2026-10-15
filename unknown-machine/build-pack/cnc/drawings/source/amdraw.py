"""Drafting side of the AM drawing set: ISO sheet, first-angle views, dimensions, GD&T, tables, title block.

Paper units are mm from the sheet's lower-left corner. A view maps model points to paper with
`paper = centre + scale * view.p(model_point)`, so every dimension is drawn between projected model points and its
value is the model distance between them (checked against the nominal the spec sheet gives: a mismatch raises,
which is how sheet/model disagreements are caught).
"""
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.patches import PathPatch, Polygon, Circle, Rectangle
from matplotlib.path import Path
import numpy as np
from shapely.geometry import LineString, MultiLineString, Point as SPoint, Polygon as SPolygon

SHEETS = {"A3": (420, 297), "A4": (297, 210), "A2": (594, 420)}
PT = 72 / 25.4             # points per mm
W_THICK, W_THIN = 0.5, 0.25
FONT = "DejaVu Sans"
H_DIM = 2.5               # text heights (capital height, mm)
H_NOTE = 2.5
H_LABEL = 3.5
CAP = 0.73                # DejaVu cap height / em

DISAGREEMENTS = []        # filled by checks: (part, text)


def fs(h):
    return h / CAP * PT


def fmt(v, dec=None):
    if dec is not None:
        r = f"{v:.{dec}f}"
        return r[1:] if r.startswith("-") and float(r) == 0 else r
    s = f"{v:.3f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def check(part, label, measured, nominal, tol=0.0015):
    """Model value vs the spec sheet's nominal: model wins, the difference is recorded."""
    if nominal is not None and abs(measured - nominal) > tol:
        DISAGREEMENTS.append((part, f"{label}: sheet {fmt(nominal)}, model {fmt(measured)} (drawn as the model)"))
        return False
    return True


class PView:
    def __init__(self, sheet, view, centre, scale, geo=None, loops=None, label=None, beyond=True, clip=None,
                 label_pos=None, ref=None):
        self.s, self.v, self.c, self.k = sheet, view, np.array(centre, float), scale
        self.ref = self.c if ref is None else np.asarray(ref, float)   # dimension `pos` offsets are from here
        self.geo = geo or {}
        self.loops = loops or []
        self.label, self.beyond = label, beyond
        self.label_pos = label_pos
        self.clip = None
        if clip is not None:
            self.clip_centre, self.clip_r = np.asarray(clip[0], float), clip[1]
            self.clip = True
            self.clip_poly = SPoint(*self.clip_centre).buffer(self.clip_r, 128)
            sheet.ax.add_patch(Circle(self.clip_centre, self.clip_r, fill=False, lw=W_THIN * PT, color="k"))
        self.draw()

    def P(self, pt):
        return self.c + self.k * self.v.p(pt)

    def p2(self, xy):
        """Paper point from view-plane model coordinates (right, up)."""
        return self.c + self.k * np.asarray(xy, float)

    def _clip(self, segs):
        """Clip paper polylines to the detail circle (shapely), or pass them through."""
        if self.clip is None:
            return segs
        out = []
        for sgm in segs:
            if len(sgm) < 2:
                continue
            g = LineString(sgm).intersection(self.clip_poly)
            for part in getattr(g, "geoms", [g]):
                if part.geom_type == "LineString" and not part.is_empty:
                    out.append(np.array(part.coords))
        return out

    def _lines(self, polys, **kw):
        if not polys:
            return
        segs = self._clip([self.c + self.k * p for p in polys])
        if not segs:
            return
        self.s.ax.add_collection(LineCollection(segs, **kw))
        self.s.geom_segments.extend(segs)

    def draw(self):
        ax = self.s.ax
        # hatching of cut faces (45°, clipped exactly with shapely)
        for face in self.loops:
            rings = [self.c + self.k * loop for loop in face]
            poly = SPolygon(rings[0], rings[1:]).buffer(0)
            if self.clip is not None:
                poly = poly.intersection(self.clip_poly)
            if poly.is_empty:
                continue
            x0, y0, x1, y1 = poly.bounds
            sp = 1.6 if max(x1 - x0, y1 - y0) > 12 else 1.0
            lines, t = [], x0 - (y1 - y0) - sp
            while t < x1 + sp:
                lines.append([(t, y0 - 1), (t + (y1 - y0) + 2, y1 + 1)])
                t += sp
            g = MultiLineString(lines).intersection(poly)
            segs = [np.array(gg.coords) for gg in getattr(g, "geoms", [g]) if gg.geom_type == "LineString"]
            ax.add_collection(LineCollection(segs, colors="k", linewidths=W_THIN * PT * 0.7))
            self._lines([np.vstack([loop, loop[:1]]) for loop in face], colors="k", linewidths=W_THICK * PT)
        if self.beyond:
            self._lines(self.geo.get("visible"), colors="k", linewidths=W_THICK * PT, capstyle="round")
            self._lines(self.geo.get("hidden"), colors="k", linewidths=W_THIN * PT * 1.1, linestyles=(0, (3, 1.5)))
        if self.label:
            x0, y0, x1, y1 = self.bounds()
            lx, ly = self.label_pos if self.label_pos is not None else ((x0 + x1) / 2, y1 + 6)
            self.s.text(lx, ly, self.label, h=H_LABEL, ha="center", va="bottom")

    def bounds(self):
        pts = []
        for p in (self.geo.get("visible") or []):
            pts.append(p)
        for f in self.loops:
            pts.extend(f)
        if not pts:
            return (*self.c, *self.c)
        a = self.c + self.k * np.vstack(pts)
        if self.clip is not None:
            cx, cy = self.clip_centre; r = self.clip_r
            return cx - r, cy - r, cx + r, cy + r
        return a[:, 0].min(), a[:, 1].min(), a[:, 0].max(), a[:, 1].max()

    # convenience
    def centreline(self, a, b, ext=3):
        A, B = self.P(a), self.P(b)
        d = (B - A) / np.linalg.norm(B - A)
        self.s.chain(A - d * ext, B + d * ext)

    def centremark(self, pt, r_model, ext=2.0):
        C = self.P(pt)
        rr = r_model * self.k + ext
        self.s.chain(C - (rr, 0), C + (rr, 0))
        self.s.chain(C - (0, rr), C + (0, rr))

    def pcd(self, r_model, centre=(0, 0, 0)):
        C = self.P(centre)
        self.s.ax.add_patch(Circle(C, r_model * self.k, fill=False, lw=W_THIN * PT, ls=(0, (12, 2, 1.5, 2)), color="k"))


def detail(sheet, parent, centre, r, scale, at, name, label_dy=None):
    """Detail view of `parent` around model point `centre` (radius r, model mm) drawn at paper `at`."""
    C = parent.P(centre)
    sheet.ax.add_patch(Circle(C, r * parent.k, fill=False, lw=W_THIN * PT, color="k"))
    d = np.array([1, 1]) / math.sqrt(2)
    sheet.text(*(C + d * (r * parent.k + 1.2)), name, h=H_LABEL, ha="left", va="bottom")
    k = scale
    centre2 = parent.v.p(centre)
    pv = PView(sheet, parent.v, np.asarray(at, float) - k * centre2, k, geo=parent.geo, loops=parent.loops,
               clip=(at, r * k), beyond=parent.beyond)
    pv.ref = np.asarray(at, float)
    sc = f"{int(k)}:1" if k >= 1 else f"1:{int(round(1 / k))}"
    sheet.text(at[0], at[1] + r * k + (label_dy if label_dy is not None else 2.5), f"DETAIL {name} ({sc})",
               h=H_LABEL, ha="center", va="bottom")
    return pv


def cutting_line(sheet, pv, a, b, name, look, ext=4.0):
    """Section cutting plane on a view: chain line from model a to b, thick ends, arrows in paper direction `look`
    (the direction the section is viewed in), letters at the arrows."""
    A, B = pv.P(a), pv.P(b)
    u = (B - A) / np.linalg.norm(B - A)
    A1, B1 = A - u * ext, B + u * ext
    sheet.chain(A1, B1)
    for E, s in ((A1, 1), (B1, -1)):
        sheet.line([E, E + u * s * 5], w=0.7)
        L = np.asarray(look, float); L /= np.linalg.norm(L)
        base = E + u * s * 1.5
        sheet.line([base - L * 6, base])
        sheet.arrow(base, L, L=3, Wd=1.2)
        sheet.text(*(base - L * 7.5 - (0, 1.5)), name, h=H_LABEL, ha="center")


def view_arrow(sheet, tip, look, name):
    """Reference arrow for a view in the direction `look`, with its letter."""
    L = np.asarray(look, float); L /= np.linalg.norm(L)
    tip = np.asarray(tip, float)
    sheet.line([tip - L * 9, tip], w=0.35)
    sheet.arrow(tip, L, L=3, Wd=1.2)
    sheet.text(*(tip - L * 12 - (0, 1.8)), name, h=H_LABEL, ha="center")


class Sheet:
    def __init__(self, size="A3", title_info=None):
        self.W, self.H = SHEETS[size]
        self.size = size
        self.fig = plt.figure(figsize=(self.W / 25.4, self.H / 25.4))
        self.ax = self.fig.add_axes([0, 0, 1, 1])
        self.ax.set_xlim(0, self.W); self.ax.set_ylim(0, self.H)
        self.ax.set_aspect("equal"); self.ax.axis("off")
        self.texts = []
        self.geom_segments = []
        self.frame()

    # ---------------------------------------------------------- primitives
    def line(self, pts, w=W_THIN, **kw):
        pts = np.asarray(pts, float)
        self.ax.plot(pts[:, 0], pts[:, 1], color="k", lw=w * PT, solid_capstyle="butt", **kw)

    def chain(self, a, b, w=W_THIN):
        self.ax.plot([a[0], b[0]], [a[1], b[1]], color="k", lw=w * PT, ls=(0, (12, 2, 1.5, 2)))

    def text(self, x, y, s, h=H_DIM, ha="left", va="baseline", rot=0, bold=False, check=True, **kw):
        t = self.ax.text(x, y, s, fontsize=fs(h), ha=ha, va=va, rotation=rot, family=FONT,
                         fontweight="bold" if bold else "normal", rotation_mode="anchor", **kw)
        if check:
            self.texts.append(t)
        return t

    def arrow(self, tip, direction, L=2.6, Wd=0.9):
        d = np.asarray(direction, float); d /= np.linalg.norm(d)
        n = np.array([-d[1], d[0]])
        tip = np.asarray(tip, float)
        base = tip - d * L
        self.ax.add_patch(Polygon([tip, base + n * Wd / 2, base - n * Wd / 2], closed=True, color="k", lw=0))

    # ---------------------------------------------------------- frame and title block
    def frame(self):
        W, H = self.W, self.H
        self.ax.add_patch(Rectangle((0, 0), W, H, fill=False, lw=0.1, color="#888"))
        self.ax.add_patch(Rectangle((20, 10), W - 30, H - 20, fill=False, lw=0.7 * PT, color="k"))
        # centring marks
        for a, b in (((W / 2 + 10, 5), (W / 2 + 10, 10)), ((W / 2 + 10, H - 10), (W / 2 + 10, H - 5)),
                     ((15, H / 2), (20, H / 2)), ((W - 10, H / 2), (W - 5, H / 2))):
            self.line([a, b], w=0.7)
        # zones
        nx = 8 if self.size == "A3" else 6
        ny = 6 if self.size == "A3" else 4
        for i in range(nx + 1):
            x = 20 + (W - 30) * i / nx
            self.line([(x, 5), (x, 10)]); self.line([(x, H - 10), (x, H - 5)])
        for j in range(ny + 1):
            y = 10 + (H - 20) * j / ny
            self.line([(15, y), (20, y)]); self.line([(W - 10, y), (W - 5, y)])
        for i in range(nx):
            x = 20 + (W - 30) * (i + 0.5) / nx
            self.text(x, 6.3, str(i + 1), h=2.5, ha="center", check=False)
            self.text(x, H - 8.7, str(i + 1), h=2.5, ha="center", check=False)
        for j in range(ny):
            y = 10 + (H - 20) * (j + 0.5) / ny
            L = "ABCDEFGH"[ny - 1 - j]
            self.text(17.5, y, L, h=2.5, ha="center", va="center", check=False)
            self.text(W - 7.5, y, L, h=2.5, ha="center", va="center", check=False)

    def title_block(self, f):
        """ISO 7200-style block, 180 wide, bottom right."""
        W = self.W
        x0, x1 = W - 10 - 180, W - 10
        y0 = 10
        rows = [8, 8, 8, 8, 11, 12]  # bottom up
        ys = np.cumsum([y0] + rows)
        top = ys[-1]
        self.ax.add_patch(Rectangle((x0, y0), 180, top - y0, fill=False, lw=0.7 * PT))
        for y in ys[1:-1]:
            self.line([(x0, y), (x1, y)], w=0.35)

        def cell(xa, xb, r, label, value, h=2.5, bold=False):
            ya, yb = ys[r], ys[r + 1]
            if xa > x0:
                self.line([(xa, ya), (xa, yb)], w=0.35)
            self.text(xa + 1.2, yb - 2.2, label, h=1.5, check=False, color="#333")
            if isinstance(value, (list, tuple)):
                for i, v in enumerate(value):
                    self.text(xa + 1.5, yb - 2.6 - (i + 1) * (h + 1.3), v, h=h, check=False, bold=bold)
            else:
                self.text(xa + 1.5, ya + 1.6, value, h=h, check=False, bold=bold)

        # row 0 (bottom): drawing number, revision, sheet, size, date
        cell(x0, x0 + 70, 0, "DRAWING / PART NUMBER", f["number"], h=3.2, bold=True)
        cell(x0 + 70, x0 + 85, 0, "REV", f.get("revision", "A"), h=3.2, bold=True)
        cell(x0 + 85, x0 + 105, 0, "SHEET", "1/1")
        cell(x0 + 105, x0 + 125, 0, "SIZE", self.size)
        cell(x0 + 125, x1, 0, "DATE OF ISSUE", f.get("date", "2026-10-14"))
        # row 1: title
        cell(x0, x1 - 40, 1, "TITLE", f["title"], h=3.2, bold=True)
        cell(x1 - 40, x1, 1, "QTY PER ACTUATOR", f["qty"], h=3.0, bold=True)
        # row 2: material, scale
        cell(x0, x1 - 40, 2, "MATERIAL", f["material"], h=2.3)
        cell(x1 - 40, x1, 2, "SCALE", f["scale"], h=3.0)
        # row 3: finish
        cell(x0, x1 - 40, 3, "FINISH / HEAT TREATMENT", f["finish"], h=2.0)
        cell(x1 - 40, x1, 3, "UNITS", "mm")
        # row 4: tolerances, projection
        cell(x0, x0 + 95, 4, "GENERAL TOLERANCES", ["ISO 2768-mK   (ISO 22081)", "Edges ISO 13715 " + f.get("edges", "-0.3 (0.2-0.4)")], h=2.2)
        cell(x0 + 95, x1, 4, "PROJECTION", "", h=2.2)
        self.projection_symbol(x0 + 100, ys[4] + 1.6)
        self.text(x0 + 124, ys[4] + 4.0, "FIRST ANGLE", h=2.2, check=False)
        self.text(x0 + 124, ys[4] + 1.3, "ISO 128 / ISO 5456-2", h=1.6, check=False)
        # row 5: project / owner / drawn by
        cell(x0, x0 + 70, 5, "PROJECT", ["Unknown machine actuator"], h=2.4, bold=True)
        cell(x0 + 70, x0 + 125, 5, "DRAWN BY", ["Claude for macncrash"], h=2.2)
        cell(x0 + 125, x1, 5, "SOURCE (MODEL GOVERNS)", [f["source"][0], f["source"][1]], h=1.7)
        # revision table above the block
        ry = top
        self.ax.add_patch(Rectangle((x0, ry), 180, 10, fill=False, lw=0.35 * PT))
        self.line([(x0, ry + 5), (x1, ry + 5)], w=0.25)
        for xx in (x0 + 12, x0 + 140, x0 + 162):
            self.line([(xx, ry), (xx, ry + 10)], w=0.25)
        for xx, s in ((x0 + 1.5, "REV"), (x0 + 13.5, "DESCRIPTION"), (x0 + 141.5, "DATE"), (x0 + 163.5, "BY")):
            self.text(xx, ry + 6.4, s, h=1.8, check=False)
        for xx, s in ((x0 + 1.5, "A"), (x0 + 13.5, "First release for quotation and manufacture"),
                      (x0 + 141.5, "2026-10-14"), (x0 + 163.5, "Claude")):
            self.text(xx, ry + 1.4, s, h=2.0, check=False)
        self.tb_top = ry + 10
        self.tb_x0 = x0

    def projection_symbol(self, x, y):
        """First-angle symbol: truncated cone seen from its small end, placed on the side of its large end."""
        h1, h2, L = 3.0, 6.0, 7.0
        cy = y + h2 / 2 + 0.2
        tx0 = x
        # trapezoid: narrow end on the left, wide end on the right
        self.line([(tx0, cy - h1 / 2), (tx0 + L, cy - h2 / 2), (tx0 + L, cy + h2 / 2), (tx0, cy + h1 / 2),
                   (tx0, cy - h1 / 2)], w=0.35)
        cx = tx0 + L + 3 + h2 / 2 + 1
        for r in (h1 / 2, h2 / 2):
            self.ax.add_patch(Circle((cx, cy), r, fill=False, lw=0.35 * PT))
        self.chain((tx0 - 1.5, cy), (cx + h2 / 2 + 1.5, cy))
        self.chain((cx, cy - h2 / 2 - 1.5), (cx, cy + h2 / 2 + 1.5))

    # ---------------------------------------------------------- dimensions
    def dim(self, pv, a, b, d="h", pos=0.0, text=None, nominal=None, part=None, label=None, prefix="", suffix="",
            tol="", dec=None, tshift=0.0, outside=False, ext_a=True, ext_b=True, paper=False, h=H_DIM, aligned_dir=None):
        """Linear dimension between model points a and b (paper=True: paper points). d: 'h' (paper x), 'v'
        (paper y). pos: the dimension line's paper coordinate relative to the view centre (y for 'h', x for
        'v'). Returns the dimension line's end points."""
        A = np.asarray(a, float) if paper else pv.P(a)
        B = np.asarray(b, float) if paper else pv.P(b)
        if d == "h":
            val = abs(B[0] - A[0]) / (1 if paper else pv.k)
            yl = (pv.ref[1] if pv else 0) + pos
            A2, B2 = np.array([A[0], yl]), np.array([B[0], yl])
            ea, eb = A, B
        else:
            val = abs(B[1] - A[1]) / (1 if paper else pv.k)
            xl = (pv.ref[0] if pv else 0) + pos
            A2, B2 = np.array([xl, A[1]]), np.array([xl, B[1]])
            ea, eb = A, B
        if part is not None:
            check(part, label or text or prefix, val, nominal)
        # extension lines
        for E, L2, on in ((ea, A2, ext_a), (eb, B2, ext_b)):
            v = L2 - E
            n = np.linalg.norm(v)
            if on and n > 1.2:
                u = v / n
                self.line([E + u * 1.0, L2 + u * 2.0], w=W_THIN)
        # dimension line + arrows
        u = (B2 - A2); Ln = np.linalg.norm(u); u = u / Ln if Ln else np.array([1.0, 0])
        if outside:
            self.line([A2 - u * 7, B2 + u * 7])
            self.arrow(A2, u); self.arrow(B2, -u)
        else:
            self.line([A2, B2])
            self.arrow(A2, -u); self.arrow(B2, u)
        s = text if text is not None else f"{prefix}{fmt(val, dec)}{(' ' + tol) if tol else ''}{suffix}"
        mid = (A2 + B2) / 2 + u * tshift
        if d == "h":
            self.text(mid[0], mid[1] + 0.9, s, h=h, ha="center", va="bottom")
        else:
            self.text(mid[0] - 0.9, mid[1], s, h=h, ha="center", va="bottom", rot=90)
        return A2, B2, val

    def leader(self, tip, at, lines, h=H_DIM, arrow=True, dot=False, side=None, shoulder=4.0, tip_dir=None):
        """Leader from paper point `tip` to text at paper `at` with a horizontal shoulder."""
        tip, at = np.asarray(tip, float), np.asarray(at, float)
        if side is None:
            side = "right" if at[0] >= tip[0] else "left"
        sgn = 1 if side == "right" else -1
        self.line([tip, at, at + (sgn * shoulder, 0)])
        if arrow:
            self.arrow(tip, tip - at)
        if dot:
            self.ax.add_patch(Circle(tip, 0.45, color="k"))
        if isinstance(lines, str):
            lines = [lines]
        x = at[0] + sgn * (shoulder + 0.8)
        ha = "left" if sgn > 0 else "right"
        n = len(lines)
        for i, s in enumerate(lines):
            yy = at[1] + 0.8 - i * (h + 1.6) + (0 if n == 1 else (n - 1) * (h + 1.6) / 2)
            self.text(x, yy - h / 2, s, h=h, ha=ha, va="baseline")
        return at + (sgn * shoulder, 0)

    # ---------------------------------------------------------- GD&T
    def datum(self, foot, direction, label, L=6.0, on_line=True):
        """Datum feature symbol: filled triangle on the feature line at `foot`, connected along `direction`
        (paper unit vector away from the feature) to a boxed letter."""
        foot = np.asarray(foot, float)
        d = np.asarray(direction, float); d /= np.linalg.norm(d)
        n = np.array([-d[1], d[0]])
        s = 1.6
        self.ax.add_patch(Polygon([foot + n * s, foot - n * s, foot + d * s * 1.6], closed=True, color="k", lw=0))
        box_c = foot + d * (L + 3.0)
        self.line([foot + d * s * 1.2, box_c - d * 3.0])
        self.ax.add_patch(Rectangle(box_c - 3.0, 6, 6, fill=False, lw=0.35 * PT))
        self.text(box_c[0], box_c[1] - 1.25, label, h=2.6, ha="center", check=True)
        return box_c

    SYMBOLS = ("perpendicularity", "parallelism", "flatness", "cylindricity", "circularity", "coaxiality",
               "position", "circular_runout", "total_runout", "symmetry", "straightness", "profile_surface")

    def _symbol(self, kind, c, s=3.0):
        x, y = c
        L = lambda pts: self.line(pts, w=0.3)  # noqa: E731
        if kind == "perpendicularity":
            L([(x - s / 2, y - s / 2), (x + s / 2, y - s / 2)]); L([(x, y - s / 2), (x, y + s / 2)])
        elif kind == "parallelism":
            L([(x - s / 2, y - s / 2), (x - s / 6, y + s / 2)]); L([(x + s / 6, y - s / 2), (x + s / 2, y + s / 2)])
        elif kind == "flatness":
            L([(x - s / 2, y - s / 3), (x + s / 4, y - s / 3), (x + s / 2, y + s / 3), (x - s / 4, y + s / 3),
               (x - s / 2, y - s / 3)])
        elif kind == "cylindricity":
            self.ax.add_patch(Circle((x, y), s / 3, fill=False, lw=0.3 * PT))
            L([(x - s / 2, y - s / 2), (x - s / 6, y + s / 2)]); L([(x + s / 6, y - s / 2), (x + s / 2, y + s / 2)])
        elif kind == "circularity":
            self.ax.add_patch(Circle((x, y), s / 2.4, fill=False, lw=0.3 * PT))
        elif kind == "coaxiality":
            self.ax.add_patch(Circle((x, y), s / 2.2, fill=False, lw=0.3 * PT))
            self.ax.add_patch(Circle((x, y), s / 4.5, fill=False, lw=0.3 * PT))
        elif kind == "position":
            self.ax.add_patch(Circle((x, y), s / 3, fill=False, lw=0.3 * PT))
            L([(x - s / 2, y), (x + s / 2, y)]); L([(x, y - s / 2), (x, y + s / 2)])
        elif kind == "circular_runout":
            L([(x - s / 3, y - s / 2), (x + s / 3, y + s / 2)])
            self.arrow((x + s / 3, y + s / 2), (2 / 3, 1), L=1.3, Wd=0.9)
        elif kind == "total_runout":
            L([(x - s / 2, y - s / 2), (x + s / 2, y - s / 2)])
            for dx in (-s / 2, 0):
                L([(x + dx, y - s / 2), (x + dx + s / 2.5, y + s / 2)])
                self.arrow((x + dx + s / 2.5, y + s / 2), (0.8, 2), L=1.2, Wd=0.8)
        elif kind == "symmetry":
            L([(x - s / 2, y), (x + s / 2, y)]); L([(x - s / 3, y + s / 3), (x + s / 3, y + s / 3)])
            L([(x - s / 3, y - s / 3), (x + s / 3, y - s / 3)])
        elif kind == "straightness":
            L([(x - s / 2, y), (x + s / 2, y)])
        elif kind == "profile_surface":
            from matplotlib.patches import Wedge
            self.ax.add_patch(Wedge((x, y - s / 3), s / 2, 0, 180, fill=False, lw=0.3 * PT))
        else:
            raise ValueError(kind)

    def fcf(self, x, y, kind, tol, datums=(), dia=False, h=5.0, anchor="left"):
        """Feature control frame with its lower-left corner at (x, y) (anchor='right': lower-right)."""
        tol_s = ("Ø" if dia else "") + tol
        tw = max(8.0, 1.8 * len(tol_s) + 2.5)
        cells = [h] + [tw] + [max(6.0, 2.2 * len(dd) + 2.4) for dd in datums]
        wtot = sum(cells)
        if anchor == "right":
            x = x - wtot
        self.ax.add_patch(Rectangle((x, y), wtot, h, fill=False, lw=0.35 * PT))
        xx = x
        for i, w in enumerate(cells):
            if i:
                self.line([(xx, y), (xx, y + h)], w=0.35)
            if i == 0:
                self._symbol(kind, (xx + w / 2, y + h / 2), s=h * 0.62)
            elif i == 1:
                self.text(xx + w / 2, y + 1.3, tol_s, h=2.4, ha="center")
            else:
                self.text(xx + w / 2, y + 1.3, datums[i - 2], h=2.4, ha="center")
            xx += w
        return x, y, x + wtot, y + h

    def fcf_leader(self, frame, tip, from_side="left"):
        x0, y0, x1, y1 = frame
        start = np.array([x0, (y0 + y1) / 2]) if from_side == "left" else (
            np.array([x1, (y0 + y1) / 2]) if from_side == "right" else (
                np.array([(x0 + x1) / 2, y0]) if from_side == "bottom" else np.array([(x0 + x1) / 2, y1])))
        tip = np.asarray(tip, float)
        if from_side in ("left", "right"):
            knee = np.array([start[0] + (-3 if from_side == "left" else 3), start[1]])
        else:
            knee = np.array([start[0], start[1] + (-3 if from_side == "bottom" else 3)])
        self.line([start, knee, tip])
        self.arrow(tip, tip - knee)

    def rough(self, x, y, text, angle=0.0, removal=True):
        """ISO 21920-1 surface texture symbol standing with its tip at (x, y) (upright)."""
        h = 3.6
        a = np.array([x, y])
        l1 = a + np.array([-h / math.tan(math.radians(60)), h])
        l2 = a + np.array([2 * h / math.tan(math.radians(60)), 2 * h])
        self.line([l1, a, l2], w=0.3)
        if removal:   # bar closing the V at the short leg's height: material removal required
            self.line([l1, a + np.array([h / math.tan(math.radians(60)), h])], w=0.3)
        self.line([l2, l2 + (len(text) * 1.55 + 1, 0)], w=0.3)
        self.text(l2[0] + 0.6, l2[1] - 3.1, text, h=2.0)

    def rough_leader(self, tip, at, text):
        """Leader from a surface (arrow at tip) to a horizontal shoulder carrying the roughness symbol."""
        tip, at = np.asarray(tip, float), np.asarray(at, float)
        sgn = 1 if at[0] >= tip[0] else -1
        self.line([tip, at, at + (sgn * 12, 0)])
        self.arrow(tip, tip - at)
        sx = at[0] + (3 if sgn > 0 else -9)
        self.rough(sx, at[1], text)

    # ---------------------------------------------------------- tables, notes
    def table(self, x, y, cols, rows, h=2.2, row_h=4.6, header=True, title=None, bold_first_col=False):
        """Table with top-left corner at (x, y); cols: widths; rows: lists of cell strings."""
        if title:
            self.text(x, y + 1.5, title, h=2.5, bold=True)
        W = sum(cols)
        n = len(rows)
        self.ax.add_patch(Rectangle((x, y - n * row_h), W, n * row_h, fill=False, lw=0.35 * PT))
        for i in range(1, n):
            self.line([(x, y - i * row_h), (x + W, y - i * row_h)], w=0.5 if (header and i == 1) else 0.2)
        xx = x
        for w in cols[:-1]:
            xx += w
            self.line([(xx, y), (xx, y - n * row_h)], w=0.2)
        for i, r in enumerate(rows):
            xx = x
            for j, (w, c) in enumerate(zip(cols, r)):
                self.text(xx + 1.0, y - (i + 1) * row_h + (row_h - h) / 2 + 0.1, c, h=h,
                          bold=(header and i == 0) or (bold_first_col and j == 0))
                xx += w
        return x + W, y - n * row_h

    def notes(self, x, y, lines, h=2.3, title="NOTES", width=125, gap=1.4):
        import textwrap
        if title:
            self.text(x, y, title, h=2.6, bold=True)
            y -= h + gap + 1.5
        chars = int(width / (h * 0.80))
        for i, ln in enumerate(lines):
            parts = textwrap.wrap(ln, chars - 4)
            for k, p in enumerate(parts):
                if k == 0:
                    self.text(x, y, f"{i + 1}.", h=h)
                self.text(x + 4.5, y, p, h=h)
                y -= h + gap
            y -= 0.6
        return y

    # ---------------------------------------------------------- checks and output
    def overlaps(self):
        self.fig.canvas.draw()
        r = self.fig.canvas.get_renderer()
        inv = self.ax.transData.inverted()
        boxes = []
        for t in self.texts:
            if not t.get_text().strip():
                continue
            bb = t.get_window_extent(r)
            (x0, y0), (x1, y1) = inv.transform([(bb.x0, bb.y0), (bb.x1, bb.y1)])
            boxes.append((t.get_text(), x0 + 0.15, y0 + 0.15, x1 - 0.15, y1 - 0.15))
        bad = []
        for i in range(len(boxes)):
            for j in range(i + 1, len(boxes)):
                a, b = boxes[i], boxes[j]
                if a[1] < b[3] and b[1] < a[3] and a[2] < b[4] and b[2] < a[4]:
                    bad.append(("text/text", a[0], b[0]))
        # text over view geometry
        if self.geom_segments:
            P = np.vstack([np.vstack([s[:-1], s[1:]]) if len(s) > 1 else s for s in self.geom_segments])
            mids = []
            for s in self.geom_segments:
                for k in range(len(s) - 1):
                    for f in (0.25, 0.5, 0.75):
                        mids.append(s[k] * (1 - f) + s[k + 1] * f)
            P = np.vstack([P, np.array(mids)]) if mids else P
            for name, x0, y0, x1, y1 in boxes:
                inside = (P[:, 0] > x0) & (P[:, 0] < x1) & (P[:, 1] > y0) & (P[:, 1] < y1)
                if inside.any():
                    bad.append(("text/geometry", name, int(inside.sum())))
        for name, x0, y0, x1, y1 in boxes:
            if x0 < 20 or x1 > self.W - 10 or y0 < 10 or y1 > self.H - 10:
                bad.append(("outside frame", name, ""))
            if hasattr(self, "tb_top") and x1 > self.tb_x0 and y0 < self.tb_top and name not in ("",):
                pass
        return bad

    def save(self, path_pdf, png=None, dpi=110):
        self.fig.savefig(path_pdf, format="pdf")
        if png:
            self.fig.savefig(png, dpi=dpi)
        plt.close(self.fig)


def triad(sheet, pv, at, L=8.0):
    """Model axes as seen in the view (ties hole tables to the STEP frame)."""
    at = np.asarray(at, float)
    for name, vec in (("X", (1, 0, 0)), ("Y", (0, 1, 0)), ("Z", (0, 0, 1))):
        d = np.array([np.dot(vec, pv.v.r), np.dot(vec, pv.v.u)])
        if np.linalg.norm(d) < 0.5:
            dot = np.dot(vec, pv.v.t)
            sheet.ax.add_patch(Circle(at, 1.2, fill=False, lw=0.25 * PT))
            if dot > 0:
                sheet.ax.add_patch(Circle(at, 0.35, color="k"))
            else:
                sheet.line([at - 0.85, at + 0.85], w=0.25); sheet.line([at + (-0.85, 0.85), at + (0.85, -0.85)], w=0.25)
            sheet.text(at[0] - 2.2, at[1] - 3.6, name, h=2.0, ha="center", check=False)
            continue
        d = d / np.linalg.norm(d)
        sheet.line([at, at + d * L], w=0.3)
        sheet.arrow(at + d * L, d, L=1.8, Wd=0.8)
        sheet.text(*(at + d * (L + 2.2) - (0, 1.0)), name, h=2.0, ha="center", check=False)


def tag(sheet, pv, pt, name, off=(3.5, 3.5)):
    P = pv.P(pt)
    sheet.text(P[0] + off[0], P[1] + off[1], name, h=2.0, ha="center", va="center", check=False)
