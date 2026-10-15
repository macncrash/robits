"""Build one zip per vendor from the build pack: python3 make_packets.py (from build-pack/orders/).

Each packet holds what that vendor needs to quote, plus an RFQ.md with the request text. The files themselves
stay where they live in the build pack; this only bundles them. Re-run after any change.
"""
import csv
import zipfile
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
PACK = HERE.parent
GEARS = ("sun", "planet", "ring_gear")
DRAW = sorted((PACK / "cnc/drawings").glob("AM-*.pdf"))
SHEET_FOR = {"motor_shaft": "rotor", "rotor_hub": "rotor"}


def drawing_part(pdf):                       # AM-09-motor_shaft.pdf -> motor_shaft
    return pdf.stem.split("-", 2)[2]


def packet(name, files, rfq):
    out = HERE / f"{name}.zip"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("RFQ.md", rfq)
        for arc, src in files:
            z.write(src, arc)
    print(f"{out.name}: {len(files) + 1} files, {out.stat().st_size / 1e6:.1f} MB")


def rfq(name):
    return (HERE / "rfq" / f"{name}.md").read_text()


# 1. CNC shop: every machined part except the gears.
files = []
for pdf in DRAW:
    part = drawing_part(pdf)
    sheet = SHEET_FOR.get(part, part)
    if sheet in GEARS:
        continue
    files.append((f"drawings/{pdf.name}", pdf))
for step in sorted((PACK / "cnc/step").glob("*.step")):
    if step.stem not in GEARS:
        files.append((f"step/{step.name}", step))
for md in sorted((PACK / "cnc").glob("*.md")):
    if md.stem not in GEARS:
        files.append((f"specs/{md.name}", md))
packet("cnc-shop", files, rfq("cnc-shop"))

# 2. Gear shop: sun, planets, ring.
files = [(f"drawings/{p.name}", p) for p in DRAW if drawing_part(p) in GEARS]
files += [(f"step/{g}.step", PACK / f"cnc/step/{g}.step") for g in GEARS]
files += [(f"specs/{g}.md", PACK / f"cnc/{g}.md") for g in GEARS]
files.append(("specs/gears.md", PACK / "hardware/gears.md"))
packet("gear-shop", files, rfq("gear-shop"))

# 3. JLCPCB: the pendant board. fabrication.zip is exported from STEVE by hand (see RFQ.md).
files = [(f"{p.relative_to(PACK / 'pcb')}", p) for p in sorted((PACK / "pcb").rglob("*")) if p.is_file()]
packet("jlcpcb-pendant", files, rfq("jlcpcb-pendant"))

# 4. 3D printing: the pendant enclosure.
files = [(p.name, p) for p in sorted((PACK / "print/pendant").glob("*.stl"))]
packet("print-pendant", files, rfq("print-pendant"))

# 5. Bought parts, one CSV per supplier.
rows = list(csv.DictReader(open(PACK / "hardware/bom.csv")))
by = defaultdict(list)
for r in rows:
    if r["make_or_buy"] in ("buy", "make + buy"):
        by[r["supplier"] or "not yet sourced"].append(r)
files = []
tmp = HERE / ".carts"
tmp.mkdir(exist_ok=True)
for supplier, items in sorted(by.items()):
    slug = "".join(c if c.isalnum() else "-" for c in supplier.lower()).strip("-")[:40]
    path = tmp / f"{slug}.csv"
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(items)
    files.append((f"by-supplier/{slug}.csv", path))
files.append(("bom.csv", PACK / "hardware/bom.csv"))
files += [(p.name, PACK / "hardware" / p.name) for p in (PACK / "hardware").glob("*.md")]
packet("hardware", files, rfq("hardware"))
for p in tmp.glob("*.csv"):
    p.unlink()
tmp.rmdir()

# 6. Everything: the whole build pack in one zip.
files = [(str(p.relative_to(PACK)), p) for p in sorted(PACK.rglob("*"))
         if p.is_file() and "orders" not in p.relative_to(PACK).parts[:1]]
files += [(f"orders/rfq/{p.name}", p) for p in sorted((HERE / "rfq").glob("*.md"))]
packet("actuator-build-pack", files, rfq("everything"))
