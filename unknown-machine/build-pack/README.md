# Build pack: ordering a real actuator

Everything needed to have the [planetary joint actuator](../README.md) made by people with factories, without a
phone call: drawings a CNC shop and a gear shop can quote from, a sourced bill of materials, the control
pendant's board ready for JLCPCB, its printed case, and the assembly and test procedures.

**Order page:** [Actuator Order Desk](https://claude.ai/artifact/GE1qHx8ANFBGFs6aFWnunC) walks through five
orders. For each one it gives the packet, the vendor's quote page and the request text. You place every order;
nothing here has been ordered.

| Folder / file | What it is |
|---|---|
| [`cnc/`](cnc/) | 15 made parts: process sheets with fits and tolerances, STEP files (`step/`), ISO drawings AM-01 … AM-15 (`drawings/`) |
| [`hardware/`](hardware/) | `bom.csv` (every line confirmed / to-confirm / quote), drive and encoder decisions, drive interface, gears, raw stock, cost estimate |
| [`pcb/`](pcb/) | Machine control pendant: requirements, wiring to the drive, ordering steps, bring-up, firmware spec, TSX source |
| [`print/pendant/`](print/pendant/) | The pendant's PETG case, two STLs in print orientation |
| [`ASSEMBLY.md`](ASSEMBLY.md) | Box of parts to finished actuator, the reverse of the collision-checked teardown |
| [`TEST.md`](TEST.md) | Insulation and winding checks, drive settings, first spin, E-stop, run-in, output checks |
| [`orders/`](orders/) | One zip per vendor (`make_packets.py` rebuilds them), the request texts (`rfq/`), the order page source (`page/`) |

**Sources (STEVE):**
- Actuator design `02e31a10-ac9e-489a-8c91-1a4ce6a43b71`, revision 48, mirrored in [`../source/`](../source/).
  It links carrier rev 8, carrier disk rev 5 and pedestal rev 8.
- [Pendant circuit](https://stevecad.studio/?document=94f4bee3-1629-4a47-808e-e7974db7754d), revision 32, Ready to
  order.
- [Pendant enclosure](https://stevecad.studio/?document=4032528e-7594-4bb4-b2b7-6de9d52228b1), revision 11.

The lathe kit and the other shop machines still link the actuator at revision 36.

## What changed to make it buildable (revision 36 → 48)

- **Sun gear drive.** A key can't fit the sun: a 4 × 4 key in the Ø12 bore would cut through the 18 T root. The
  sun is now driven by a double-D, two flats 10.8 mm across.
- **Pilot needle bearing.** The HK1210 is 12 × 16 × 10. Its carrier seat was Ø18 and is now Ø16 N6.
- **Retention that was missing.**
  - End bell: 4 × M4 screws.
  - Rear cap: 3 × M3 screws.
  - Crossed-roller bearing: a clamp ring and a retaining ring.
  - 6001: retaining-ring grooves for its rings.
- **Encoder.** The placeholder disk and read head are replaced by an RLS AksIM-2 (BiSS-C, absolute) on a new hub
  and standoffs.
- **Manufacturing review (CNC).**
  - Relief grooves at shoulders.
  - Lead-in chamfers.
  - Root fillets on the gears.
  - Adhesive grooves in the stator bore.
  - Fillets on the carrier.
  - The cap's flutes are now cut on a C-axis.
  - The shaft is 42CrMo4 with a hardened, ground needle journal.

Fit check (2,016 pairs) and the teardown collision check pass on revision 48.

## Still open before ordering

1. **Motor.** Confirm the KBM-17H01-B00 order code and its inductance with Kollmorgen. The AKD needs at least
   2.5 mH.
2. **Motor PTC.** Ask whether the AKD reads the motor PTC with BiSS-C feedback. If not, fit a PTC relay.
3. **Planet pins.** Hardened dowels are m6, but INA asks for an h6 raceway. Confirm with Schaeffler, or change
   to h6 pins.
4. **Pendant files.** Export the pendant's `fabrication.zip` from STEVE. Its API can't download it.
5. **Prices.** Quotes are still needed for the CNC parts, the gears, the motor and the drive. The cost range
   (about $8–17k for one unit) is mostly estimates until those quotes arrive.
