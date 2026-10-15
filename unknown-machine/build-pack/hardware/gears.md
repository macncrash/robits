# Gears: specification, stock search and recommendation

Planetary stage from `source/params.py` and `source/components/*.py`: one stage, module 1, sun 18 T, three
planets 27 T, internal ring 72 T, 12 mm face, ratio 5:1, centre distance 22.5 mm. The loads come from
`analysis/README.md`: 20 N·m at the output, a 170 N tangential force per mesh, 657 MPa Hertz contact stress at
the sun–planet mesh and 328 MPa at the planet–ring mesh. The stock search was done on 2026-10-14. All
prices are in USD unless marked.

## Recommendation, short

- **Have all five gears made to drawing.** No catalogue sells a module 1, 72-tooth internal ring.
  KHK, QTC/SDP-SI and HPC all skip from 60 T to 80 T, and Misumi and Ondrives list no internal gear at all.
  For the sun and planets, nothing hardened is sold at 18 T and 27 T with a 12 mm face. A stock gear would
  mean a narrower face, softer teeth, a hub to remove, and a rebore that the hardened gears don't allow.
  Once the ring has to be made anyway, ordering the sun and planets from the same gear shop, cut from the same
  drawing set, costs little extra and keeps the backlash and quality matched.
- **Change the sun's bore before ordering anything (design change).** The drawing's Ø12 bore with a key will
  not work. An 18 T m1 sun has a root diameter of 15.5 mm. A DIN 6885 4 × 4 key in a Ø12 bore needs a hub
  groove 1.8 mm deep, so the bottom of the groove sits at Ø15.6, past the tooth root. Even with no key, only
  1.75 mm of rim is left under the root. The recommended fix is a **double-D drive**: two flats on the shaft
  nose, each 0.6 mm deep (10.8 mm across the flats), at z 48–60. The sun gets the matching double-D bore,
  wire-EDM cut after hardening. The flats cut inward, so the rim under the teeth stays at 1.75 mm. At the
  flats the hollow shaft (Ø12 / Ø8) keeps 1.4 mm of wall. It sees about 15 MPa of torsion at 4 N·m, which is
  low. The sun still slides off forward, so the teardown order doesn't change. The CAD needs updating:
  `rotor.py` (flats) and `sun.py` (bore).
- **Prototype stopgap, if gears are needed before the custom ones arrive.** Use rebored stock planets and an
  unhardened stock sun at reduced torque. This gives no usable ring, though. The ring has to be custom even
  for a prototype, unless the ratio changes: for example to 60 T or 80 T stock rings, which would need new sun
  and planet tooth counts that satisfy z_ring = z_sun + 2 × z_planet with (z_sun + z_ring) divisible by 3.

## Gear specification (for the RFQ drawing)

| | Sun | Planet (× 3, plus 1 spare suggested) | Ring (internal) |
|---|---|---|---|
| Module (normal) | 1 | 1 | 1 |
| Teeth | 18 | 27 | 72 |
| Pressure angle | 20° | 20° | 20° |
| Helix angle | 0° (spur) | 0° | 0° |
| Profile shift coefficient | 0 | 0 | 0 |
| Reference (pitch) diameter | 18.000 | 27.000 | 72.000 |
| Tip diameter | 20.00 | 29.00 | 70.00 (internal tip) |
| Root diameter (dedendum 1.25 m) | 15.50 | 24.50 | 74.50 |
| Root fillet radius | 0.38 (0.38 m, standard hob) | 0.38 | 0.38 |
| Face width | 12.0 | 12.0 | 12.0 |
| Bore / outer fit | Double-D: Ø12 H7 with two flats 10.8 across (see above), wire-EDM after heat treatment | Ø10 bore for the pressed-in HK0609 drawn cup. Tolerance as Schaeffler gives for drawn cups in steel housings (expected N6; **confirm in the Schaeffler catalogue**). Grind it after heat treatment | OD Ø86, press fit into the 6061 flange. See the ring fit note |
| Span measurement, nominal (no backlash allowance) | W3 = 7.632 over 3 teeth | W4 = 10.711 over 4 teeth | measure between pins; the shop chooses the pin size |
| Backlash | Thin the sun and planet teeth so the working backlash is about 0.03–0.08 mm at a 22.5 centre distance. This is a typical target for a precision actuator. Agree the tooth-thickness tolerance with the shop | | |
| Quality grade | ISO 1328-1:2013 grade 6 (about DIN 3962 class 6), teeth ground after heat treatment | ISO 1328-1 grade 6, ground | ISO 1328-1 grade 7 (about DIN class 7), shaped. Internal gears are hard to grind at this size |
| Material | 18CrNiMo7-6 (1.6587). US alternatives: AISI 9310 or 8620 (certificate required) | 18CrNiMo7-6 | 34CrNiMo6 (1.6582) +QT. US alternative: AISI 4340 |
| Heat treatment | Carburise, quench, temper | Carburise, quench, temper | Quench and temper before cutting. Optional gas nitriding after cutting |
| Surface hardness | 58–62 HRC | 58–62 HRC | QT 28–34 HRC (about 280–320 HB). If nitrided, ≥ 550 HV surface |
| Case depth | Eht 0.3–0.5 mm to 550 HV1, measured after grinding. A thin case is normal for m1: about 0.3–0.5 × m. Confirm with the heat treater | Eht 0.3–0.5 mm | Nitriding depth (Nht) 0.2–0.3 mm, if nitrided |
| Core hardness | 30–42 HRC | 30–42 HRC | — |
| Edges | Chamfer the tooth ends 0.2 × 45°; bore chamfer 0.3 (sun 0.5, per AM-13) | same | same |
| Allowable contact stress (typical ISO 6336-5 values, not vendor figures) | about 1500 MPa (carburised) vs 657 MPa needed | about 1500 MPa | QT about 700–800 MPa, nitrided about 1000 MPa, vs 328 MPa needed |

**Ring fit note.** The ring is pressed into a 6061 flange, and aluminium grows about twice as fast as steel
(23.6 vs about 11.5 µm/m·K). At 50 K above assembly temperature, a Ø86 fit loses about
86 × 12.1e-6 × 50 ≈ 0.05 mm of interference. Use about 0.06–0.08 mm of interference at room temperature,
for example a ring OD of Ø86 s6 (AM-15) in a flange bore of Ø86 H7. Add Loctite 638 or 648 retaining compound
in the joint. The flange wall is about 17 mm thick (Ø86 to Ø120), so the hoop stress from that fit is modest.
It has not been calculated, so check it before releasing the drawing. The ring then comes out forward with a
press, as the teardown describes.

## What buying stock would force

| Item | Stock reality | Consequence |
|---|---|---|
| Face width | Stock faces are 8 mm (KHK SSG, HPC), 10 mm (KHK MSGA/SS/SI, Ondrives) or 12 mm (Misumi GEAB, unhardened only) | Contact stress grows with 1/√b: 657 MPa at 12 mm becomes about 720 MPa at 10 mm and about 805 MPa at 8 mm. The ring and carrier spacing are designed around 12 mm |
| Bore | Stock pilot bores are 6–8 mm. KHK says its carburised MSGA/MSGB gears must not be re-machined. Gears hardened only at the teeth (SSG) and unhardened gears can be rebored | The planet's Ø10 cup bore is only possible on SSG or unhardened stock. No stock 18 T gear can take the sun's drive (see above) |
| Material and hardness | Stock options are carburised SCM415 (KHK MSGA, 18 T only, no 27 T), induction-hardened S45C (KHK SSG, Misumi GEAHBH 18 T only), or unhardened S45C | Unhardened S45C (allowable about 500–550 MPa) fails the 657 MPa sun mesh. Induction-hardened S45C (about 1100–1200 MPa) is acceptable, but at 8 mm face |
| Hub | KHK SSG/SS/MSGA have hubs (15–20 mm total length) | They would have to be parted off, which is impossible on through-carburised MSGA. Hubless KHK SSAG comes only in 25 T and 30 T |
| Ring tooth count and OD | Stock m1 rings: KHK SI1-60 (OD 90), SI1-80 (OD 110), SI1-100; SDP-SI 60/80/96/100/108 T (OD 100+); HPC IN1 58/60/100 T (OD 100/150); none at 72 T | A new tooth count means a new ratio, new sun and planets, a new flange bore and a new carrier orbit |
| Ring hardness | KHK SI is S45C under 194 HB. KHK rates SI1-60 at 5.95 N·m and SI1-80 at 6.59 N·m surface durability | Each planet–ring mesh carries about 6 N·m with load sharing, so an unhardened ring is at its limit. Hence 34CrNiMo6 QT or nitrided |

### Stock gears checked (2026-10-14)

| Vendor, part | Teeth | Face | Bore / hub | Material, hardness | Grade | Price seen | Source |
|---|---|---|---|---|---|---|---|
| KHK MSGA1-18 | 18 | 10 | 8, hub Ø15 | SCM415 carburised, 55–60 HRC | JIS N5 | 71.93 (list page) | catalog.khkgears.us/viewitems/spur-gears/ground-spur-gears-msga-msgb |
| KHK MSGA/MSGB m1 27 T | does not exist (m1: 18, 20, 24, 25, 30…) | | | | | | same page |
| KHK SSG1-18 | 18 | 8 | 6, hub Ø15 | S45C, teeth 50–60 HRC | N7 | not shown | catalog.khkgears.us/item/spur-gears/ground-spur-gears-ssg/ssg1-18 |
| KHK SSG1-27 / SSG1-27J10 | 27 | 8 | 8, hub Ø20 / 10 + keyway | S45C, teeth 50–60 HRC | N7 | not shown (J series is made to order) | …/ssg1-27, …/ssg1-27j10 |
| KHK SI1-60 / SI1-80 / SI1-100 (internal) | 60 / 80 / 100 | 10 | OD 90 / 110 / — | S45C under 194 HB | N8 | 73.01 / 91.64 / 118.26 | …/steel-internal-gears-si/si1-60 |
| Misumi GEAB / GEAHB 1.0-18, 1.0-27 | 18, 27 | selectable, 12 listed (verify) | bore P H7, 1 mm steps | S45C unhardened | about N8 | not seen | de.misumi-ec.com/files/images/products/docs/gears.pdf |
| Misumi GEAHBH 1.0-18 | 18 (no 27) | about 10 | 6–10 | S45C induction hardened 51–55 HRC | about N6 | not seen | same PDF |
| SDP-SI S1E10ZM10S060 / S080 (internal) | 60 / 80 | 10 | OD 100 | 303 stainless | ISO 7 | 93.30 / 104.93 (search snippet) | shop.sdp-si.com/s1e10zm10s060.html |
| SDP-SI S10S10M018P1008G | 18 | 10 | 8 | AISI 4135 | | 143.63, 12-week lead (snippet) | shop.sdp-si.com/s10s10m018p1008g.html |
| HPC Europe IN1-58 / IN1-60 / IN1-100 (internal) | 58 / 60 / 100 (others on request) | 8 | OD 100 / 100 / 150 | steel | | 60.97 / 61.75 / 105.97 (as printed, probably EUR) | shop.hpceurope.com/pdf/gbPDFauto/IN1.pdf |
| Ondrives UPSG1.0 series | m1: 10–15, 25, 29, 50+ (no 18 or 27) | 10 | 10 H6, keyed | 805M20 case hardened 58–62 HRC, ground | DIN 4f24 | not seen | ondrives.com/ground-spur-gears |
| Boston Gear | inch diametral pitch only; no metric m1 found | | | | | | |

## Gear shops that take RFQs online (none contacted)

| Shop | RFQ page | What it says it does |
|---|---|---|
| KHK USA, made to print (made by Kohara Gear, Japan) | https://khkgears.us/rfq-custom-gears/ | Spur, helical and **internal** gears m0.5–14 up to Ø700, quality N5–N12, materials including 4115, 4140, 8620, 1045. The page doesn't say whether carburising or grinding is offered: ask |
| Gear Motions (Syracuse NY, USA) | https://www.gearmotions.com/about-us/contact-us/ (drawing upload) | Cut and ground gears up to AGMA Q15, prototype quantities, internal gears listed. Ask about heat treatment |
| Ondrives (UK) | https://www.ondrives.com ("Ask an Engineer") | Already makes case-hardened, ground m1 spur gears in 805M20. Ask whether they will make internal gears |
| Also: SDP-SI custom gears | https://www.sdp-si.com/Custom-Gear-Manufacturing/ | m0.5–3, quotes from a drawing, lists planetary systems |
| Also: Rush Gears | https://www.rushgears.com/tech-tools/rfq | Upload up to 9 files. Quantities 10–1000, so prototype quantities may be too small |

What to send: a drawing with the table above for each gear, STEP files (`exports/step/components/sun.step`,
`planet.step` and `ring_gear.step`; the sun bore must be updated to the double-D first), quantities of
1 + 3 (+1 spare planet) for one unit and 5 + 15 for five units, a material certificate, and a gear
inspection report (profile, lead and pitch per ISO 1328, plus a hardness and case-depth report).
