# Raw stock for the made parts

Finished envelopes come from the STL meshes in `exports/stl` (design revision 36, mm, design frame: motor axis
+Z, pedestal toward −Y). They were read with a plain Python 3 binary-STL parser (no numpy). Stock sizes add
about 3–4 mm on the diameter and 4–5 mm on the length for facing, parting and chucking. Each turned part
also needs about 10–15 mm of extra bar to hold in the chuck, unless the shop works from a long bar.

**How the prices were found (2026-10-14).** The supplier sites (OnlineMetals, Speedy Metals, Metals Depot,
McMaster) blocked direct page loads or render their prices in JavaScript. So every price below was read from
the search engine's indexed copy of that supplier's own product page. Check each one on the live page before
buying. Two indexed copies of some Speedy Metals pages show different prices; where that happened, both are
given. OnlineMetals sells the round bar in 12" (305 mm) minimum cuts. Speedy Metals sells by the inch.

## Envelopes and stock

| Part | Material | Finished envelope (STL) | Finished volume | Stock blank | Supplier, PN, price seen |
|---|---|---|---|---|---|
| Housing | 6061-T6 (T6511 extruded bar is fine) | Ø120.0 × 80.0 (z −36..44) | 279 cm³ | Ø5" (127) round × 90 mm (3.5"). Shares one 12" bar with the front flange | OnlineMetals PN 1107, Ø5" 6061-T6511, 12" = 245.14 USD. Speedy Metals p-2478, 28.86 USD/in (12" = 309.25). McMaster made-to-order 4012N48 (price not seen) |
| Front flange | 6061-T6 | Ø120.0 × 21.0 (z 44..65) | 117 cm³ | Ø5" round × 26 mm (from the same bar) | as above |
| Rear end bell | 6061-T6 | Ø103.0 × 15.0 (z −48..−33) | 102 cm³ | Ø4.25" (108) round × 20 mm. Make it from the Ø5" bar too if that is simpler | OnlineMetals PN 17824, Ø4.25", 12" = 196.21 USD. Speedy p-2475, 14.83 USD/in (another copy shows 13.90 USD/in) |
| Rear cap (knurled) | 6061-T6 | Ø84.0 × 17.0 (z −65..−48) | 26 cm³ | Ø3.5" (88.9) round × 22 mm | OnlineMetals PN 1104, Ø3.5", 141.46 USD (shortest cut, probably 12"). Speedy p-2472, 9.43 USD/in (another copy shows 10.05 USD/in) |
| Pedestal | 6061-T6 | 130.0 (X) × 58.0 (Y, height) × 100.0 (Z) | 264 cm³ | 6061-T6511 rectangle bar 2.5" × 6" (63.5 × 152.4) × 4.25" (108) long. The 58 mm height comes out of the 63.5 mm thickness | OnlineMetals PN 19789, 2.5" × 6", 12" = 224.91 USD. Speedy p-2357, 15.68 USD/in (about 67 USD for 4.25"). 2.5" × 5" bar (127 wide) is too narrow |
| Planet carrier, rear part | 303 stainless (1.4305) | Ø66.0 × 26.5 (z 34..60.5) | 21 cm³ | Ø2.75" (69.85) round × 31 mm | OnlineMetals PN 2033, Ø2.75" 303 annealed cold finish, 12" = 183.26 USD |
| Planet carrier, front disk + hub | 303 stainless | Ø66.0 × 11.5 (z 60.5..72) | 18 cm³ | Ø2.75" round × 16 mm (same bar) | as above |
| Motor shaft + rotor hub sleeve | 4140 pre-hardened 28–32 HRC (the model uses S235; a shaft needs a better steel) | Ø34 × 120.0 overall: Ø12 shaft z −60..60, Ø30 hub sleeve and Ø34 shoulder over z −17..15.15, Ø8 bore end to end. The STL holds only the Ø12 shaft body (12 × 12 × 120); the hub comes from `source/components/rotor.py` | about 7.5 cm³ shaft + about 13 cm³ hub | One piece: 4140 HT Ø1.5" (38.1) × 130 mm. Drill the Ø8 bore from both ends (60 mm each side, 7.5 × D). Two-piece option: the shaft from Ø0.5" 4140 HT bar plus a pressed and bonded sleeve | Speedy p-74 (42R15), 4140 HT cold finished Ø1.5", 1.95 USD/in (about 10 USD). Speedy p-64 (42GR15, ground), 3.00 USD/in. Ø0.5": OnlineMetals mp-00002423, 12" = 11.99 USD; Speedy p-66, 0.37 USD/in |
| Sun gear (m1 18T) | 18CrNiMo7-6, carburised. US stock equivalent: 8620 | Ø20.0 (tip) × 12.0 face. A hub adds length if used | 1.6 cm³ | Ø1" (25.4) round × 18 mm per gear; a gear shop will want a 12" bar | Speedy p-786, 8620 cold finished Ø1", 1.26 USD/in (12" = 14.18 USD) |
| Planet gear (m1 27T) × 3 | 18CrNiMo7-6, carburised (8620) | Ø29.0 (tip) × 12.0, Ø10 bore | 5.8 cm³ each | Ø1.25" (31.75) round × 17 mm each, three from one 12" bar | Speedy p-788, 8620 Ø1.25", 1.98 USD/in (12" = 22.31 USD). OnlineMetals PN 15013, 12" = 20.32 USD |
| Ring gear (m1 72T internal) | 34CrNiMo6 Q&T. US equivalent: 4340 (through-hardened about 28–34 HRC, nitriding optional) | Ø86.0 OD × 12.0, internal teeth (tip Ø70, root Ø74.5) | 20.7 cm³ | Ø3.5" (88.9) round × 17 mm, bored out. A gear shop may prefer a ring blank or thick-wall tube | OnlineMetals PN 25270, 4340 annealed hot rolled Ø3.5", 12" = 446.71 USD (only 12" or longer seen). Most of the bar would be left over. Let the gear shop supply its own material |
| Encoder disk | 304 stainless | Ø44.0 × 1.0 | 1.3 cm³ | **Deleted.** The bought encoder kit (RLS AksIM-2 ring + readhead; see `decisions.md`) replaces the placeholder code disk and the read head | none |

## Buying notes

- **One aluminium bar covers three parts.** A 12" (305 mm) cut of Ø5" 6061 covers the housing (about 90 mm),
  the flange (about 26 mm) and the end bell (about 20 mm), with saw kerfs, and about 150 mm is left over.
  That is about 245 USD at OnlineMetals. Speedy Metals sells by the inch, so about 6" is roughly 175 USD.
  Most CNC shops quote their own material, so these figures are only a check on their quotes.
- **For 5 units:** the housing, flange and end bell need about 5 × 136 mm = 680 mm of Ø5" bar, or 27". Take a
  36" bar. The 303 bar needs about 5 × 50 mm = 250 mm, so a 12" cut is enough. Three planets per unit for 5
  units is 15 planets × 17 mm = 255 mm, so one 12" bar of Ø1.25" 8620 still covers it.
- **Gear blanks.** If a gear shop makes the gears (see `gears.md`), it supplies certified material.
  18CrNiMo7-6 is easy to get in Europe. In the US, 8620 or 9310 is the usual carburising grade. 9310 has
  more nickel and comes closer to 18CrNiMo7-6's core strength. Ask the shop which one it will certify.
- **Shaft steel.** The model's S235 is not a shaft material. 4140 pre-hardened (28–32 HRC) can be turned as
  supplied. The 6001 seat (Ø12 k5) and the needle-bearing journal under the HK1210 need a hardened,
  ground surface. The HK1210 has no inner ring, so its needles run straight on the shaft, which needs
  about 58 HRC there. Ask the shop to induction-harden the short journal at z 37–47 and grind it to Ø12 h6.
  The other route is a smaller shaft end with a separate inner ring, but that changes the CAD.
- **Encoder hub (new part, not in the STL set).** The AksIM-2 ring needs a small steel or aluminium hub on
  the shaft: a Ø20 g6 pilot, a Ø30 × 3 flange with M2 tapped holes on PCD 25, and a Ø12 bore. Turn it from
  Ø1.25" 6061 or 303 bar (any offcut). See `decisions.md`.
- **303 carrier.** 303 is the free-machining grade and is stocked as cold-finished annealed bar. Specify
  1.4305 / AISI 303 on the drawing.

## Shapes the shop needs to know about

- **Housing:** the fins are eight grooves 2.5 mm wide, turned 3 mm deep on a Ø96 section. The bore is
  Ø85.10 H7, 65 mm deep from the rear, with adhesive grooves 0.13–0.26 mm deep (see the README). The
  crossed-roller seat is Ø60 H7 from the front. There are 4 × M5 tapped holes on PCD 100, plus 4 radial
  M5 tapped holes and 2 × Ø4 dowel holes from below. A lathe and a 4th-axis or 3+2 mill.
- **Pedestal:** mostly a milling job. The saddle bores (Ø120 and Ø96) are cut on a horizontal setup or with
  a large boring head, about 75 % of the block becomes chips.
- **Rear cap:** a 48-groove knurl pattern. Mill it, or replace it with a standard straight knurl on a lathe.
