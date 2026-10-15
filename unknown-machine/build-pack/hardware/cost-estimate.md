# First-article cost estimate

Built from `bom.csv` on 2026-10-14. All figures are in USD.

**Prices in other currencies** were converted at assumed rates of 1 EUR = 1.10 USD, 1 GBP = 1.30 USD and
1 CAD = 0.72 USD. Check the rates on the day.

**Columns:**
- **Qty 1** is the cost of one complete unit.
- **Qty 5** is the cost of five complete units, all together.

**The three kinds of figure:**
- **price seen**: a price read on a supplier page or a search snippet of that page. The BOM's status column
  says which.
- **estimate, pending quotes**: my rough range for a CNC or gear part. Nobody has quoted these yet. Each
  includes the shop's material and setup. Setup dominates at qty 1, which is why 5 units cost much less than
  5 × one unit.
- **allowance, no price seen**: a planning number only. The Kollmorgen motor kit is quote-only, and its
  allowance was not taken from any source.

**What is left out:**
- shipping, VAT and duty (except where a seller's price includes them)
- anodising
- inspection reports
- the PCB pendant
- the control cabinet
- the lines marked "-", which are deleted or not costed

Small parts (screws, pins, circlips) are sold in packs and usually have minimum order charges, so their real
cost is higher than qty × unit price.

## Totals

| Group | Qty 1 | Qty 5 (5 units) |
|---|---|---|
| CNC parts (lines 1-10) | 1,860–4,380 | 5,160–11,450 |
| Gears (13-15) | 1,550–4,700 | 2,900–7,900 |
| Motor kit allowance (16) | 800–1,500 | 3,500–7,000 |
| Servo drive (17) | 2,473–4,024 | 12,365–20,120 |
| Encoder kit + tool (18-24) | 530–539 | 1,606–1,622 |
| Bearings, pins, screws, rings (25-39) | 166–470 | 814–2,336 |
| Adhesives, grease, paste (40-46) | 403–423 | 403–423 |
| Cables, connectors, electrical (47-54) | 232–675 | 1,164–3,376 |
| **Total** | **about 8,000–16,700** | **about 27,900–54,200 (about 5,600–10,800 per unit)** |

Where the money goes:

- **Drive: 2,473–4,024 per unit.** The low end is an unused surplus unit, not from an authorised
  distributor. Ask a distributor for a quote on a new one.
- **CNC parts: 1,900–4,400 per unit.** Nobody has quoted these. Get at least two quotes, for example from
  Xometry, Protolabs, PCBWay or a local shop. These parts are mostly simple turned work, so a local lathe
  shop may come in under the low end.
- **Gears: 1,550–4,700 per unit.** The ring gear is the biggest unknown. The ring and the sun shown here
  already include the redesign: the sun's double-D bore and the gear spec in `gears.md`.

## Per line

| BOM line | Item | Qty per unit | Qty 1 | Qty 5 (5 units) | Basis |
|---|---|---|---|---|---|
| 1 | Motor housing | 1 | 400–900 | 1,250–2,500 | estimate, pending quotes |
| 2 | Rear end bell | 1 | 150–350 | 400–900 | estimate, pending quotes |
| 3 | Encoder cap (knurled rear cap) | 1 | 120–300 | 300–750 | estimate, pending quotes |
| 4 | Front flange | 1 | 150–350 | 400–900 | estimate, pending quotes |
| 5 | Pedestal | 1 | 300–700 | 900–2,000 | estimate, pending quotes |
| 6 | Motor shaft + rotor hub sleeve | 1 | 250–600 | 600–1,500 | estimate, pending quotes |
| 7 | Planet carrier, rear part | 1 | 250–600 | 700–1,500 | estimate, pending quotes |
| 8 | Planet carrier, front disk + output hub | 1 | 150–350 | 400–900 | estimate, pending quotes |
| 9 | Encoder hub (new part) | 1 | 60–150 | 150–350 | estimate, pending quotes |
| 10 | Encoder readhead standoffs (new parts) | 4 | 30–80 | 60–150 | estimate, pending quotes |
| 11 | Encoder code disk (placeholder) | 1 | - | - | not costed |
| 12 | Encoder read head (placeholder) | 1 | - | - | not costed |
| 13 | Sun gear m1 18T | 1 | 250–700 | 500–1,400 | estimate, pending quotes |
| 14 | Planet gear m1 27T | 3 | 500–1,500 | 900–2,500 | estimate, pending quotes |
| 15 | Ring gear m1 72T internal | 1 | 800–2,500 | 1,500–4,000 | estimate, pending quotes |
| 16 | Frameless motor kit (stator + rotor) | 1 | 800–1,500 | 3,500–7,000 | allowance, no price seen |
| 17 | Servo drive | 1 | 2,473–4,024 | 12,365–20,120 | price seen |
| 18 | Encoder readhead | 1 | 168 | 839 | price seen |
| 19 | Encoder ring | 1 | 84 | 420 | price seen |
| 20 | Encoder cable | 1 | 11 | 55 | price seen |
| 21 | Encoder shims | 5 | 20 | 41 | price seen |
| 22 | Ring screws | 8 | 3–8 | 5–15 | estimate, pending quotes |
| 23 | Readhead screws | 4 | 2–6 | 4–10 | estimate, pending quotes |
| 24 | BiSS USB interface (tool, one per workshop) | 1 | 242 | 242 | price seen |
| 25 | Rear bearing 6001-2RS | 1 | 4 | 19 | price seen |
| 26 | Output bearing, crossed roller | 1 | 131–421 | 654–2,105 | price seen |
| 27 | Planet needle bearing HK0609 | 4 | 13 | 53 | price seen |
| 28 | Pilot needle bearing HK1210 | 1 | 4 | 18 | price seen |
| 29 | Planet pin, hardened ground dowel | 3 | 1 | 4 | price seen |
| 30 | Pedestal locating dowel | 2 | 0 | 2 | price seen |
| 31 | Flange screw | 4 | 1 | 5 | price seen |
| 32 | Pedestal screw | 4 | 1 | 5 | price seen |
| 33 | Carrier disk screw | 3 | 1 | 7 | price seen |
| 34 | End bell to housing screws (M4 × 16, in rev 48) | 4 | 1–3 | 5–15 | estimate, pending quotes |
| 35 | Rear cap to end bell screws (M3 × 25, in rev 48) | 3 | 1–3 | 5–15 | estimate, pending quotes |
| 36 | Shaft retaining ring at the 6001 | 2 | 1 | 6 | price seen |
| 37 | Bore retaining ring at the 6001 | 1 | 2 | 6 | price seen |
| 38 | Wave spring for the 6001 (optional) | 1 | - | - | not costed |
| 39 | Output bearing clamp ring (CNC, quoted with the made parts) + DIN 471 35 ring | 1 | 1–3 | 5–15 | estimate, pending quotes |
| 40 | Sun key | 0 | - | - | not costed |
| 41 | Stator adhesive | 1 | 97 | 97 | price seen |
| 42 | Rotor adhesive | 1 | 165 | 165 | price seen |
| 43 | Thermal paste, housing to saddle (replaces the pad) | 1 | 10–30 | 10–30 | estimate, not priced |
| 44 | Thread locker | 1 | 26 | 26 | price seen |
| 45 | Retaining compound | 1 | 21 | 21 | price seen |
| 46 | Grease, gears and needle bearings | 1 | 84 | 84 | price seen |
| 47 | Motor phase + PTC cable (m) | 5 | 51–169 | 257–844 | price seen |
| 48 | Motor power connector at the pedestal port | 1 | 30–80 | 150–400 | estimate, pending quotes |
| 49 | Mating motor cable plug | 1 | 30–80 | 150–400 | estimate, pending quotes |
| 50 | Encoder connector at the pedestal port | 1 | 36 | 182 | price seen |
| 51 | Encoder extension cable to the drive | 1 | 40–90 | 200–450 | estimate, pending quotes |
| 52 | Encoder emulation cable to the pendant | 1 | 15–40 | 75–200 | estimate, pending quotes |
| 53 | Motor PTC relay (fallback) | 1 | 0–120 | 0–600 | estimate, pending quotes |
| 54 | 24 V supply for the drive | 1 | 30–60 | 150–300 | estimate, pending quotes |
| | **Total** | | **8,047–16,714** | **27,925–54,170** | |
