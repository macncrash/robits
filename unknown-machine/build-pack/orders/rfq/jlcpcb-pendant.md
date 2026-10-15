# JLCPCB order: machine control pendant PCB (PCB + assembly)

**First, export the fabrication files from STEVE.** Open the circuit
https://stevecad.studio/?document=94f4bee3-1629-4a47-808e-e7974db7754d at revision 32, then choose Electronics →
Export → fabrication.zip. It contains the Gerbers, drill files, BOM and CPL. The zip isn't in this packet: STEVE's
API can't download it, only a signed-in person can. `fabrication/BOM-reference.csv` is a copy of the BOM to check
against.

Settings, from STEVE's fabrication checklist (also in `README.md` → ordering):

| Setting | Value |
|---|---|
| Layers | 4 |
| Thickness | 1.6 mm, 1 oz outer copper |
| Size | 80 × 110 mm |
| Finish | lead-free HASL (or ENIG) |
| Mask / silk | green / white |
| Quantity | 5 |
| Assembly | on, standard (the board has extended and through-hole parts), top side |
| Confirm parts placement | yes (first build) |

**Before paying:** upload the BOM and CPL. JLCPCB then shows live stock and price. Swap any part that is short,
using the alternates in README.md. Check every part's rotation in the placement preview.

Expected cost for 5 assembled boards: about 220–260 USD (estimate, 2026-10-15).

Upload page: https://cart.jlcpcb.com/quote
