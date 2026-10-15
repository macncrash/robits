"""Fill the order page from the BOM and the RFQ texts: python3 page/make_page.py -> page/order-desk.html."""
import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ORDERS = HERE.parent
KEEP = ("line", "qty", "item", "maker_pn", "supplier", "url", "unit_price", "currency", "status", "make_or_buy")
bom = [{k: r[k] for k in KEEP} for r in csv.DictReader(open(ORDERS.parent / "hardware/bom.csv"))
       if r["make_or_buy"] not in ("delete", "none", "make")]
rfq = {p.stem: p.read_text() for p in (ORDERS / "rfq").glob("*.md")}
page = (HERE / "template.html").read_text()
page = page.replace("__BOM__", json.dumps(bom, ensure_ascii=False)).replace("__RFQ__", json.dumps(rfq, ensure_ascii=False))
(HERE / "order-desk.html").write_text(page)
print(len(bom), "bought lines")
