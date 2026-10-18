# Assembly: from a box of parts to a running actuator

This is the reverse of the `teardown` animation in the STEVE design (02e31a10, revision 49), whose order is
collision-checked on every build. Part numbers are the drawings in [`cnc/drawings/`](cnc/drawings/); bought
parts are lines in [`hardware/bom.csv`](hardware/bom.csv).

**Before you start**
- Check every made part against its drawing's inspection notes. In particular, check the bearing seats, the
  stator bore and the gear reports.
- Do a plastic fit check first if the gears aren't in yet: [FIT-CHECK.md](FIT-CHECK.md).
- Clean everything with isopropyl alcohol. Bonded and Loctite joints must be oil-free.
- Tools:
  - an arbor press with flat, ground press tools for each bearing ring;
  - an oven (for the 2214 stator bond);
  - a torque driver;
  - DIN 471/472 circlip pliers;
  - a gaussmeter (optional).
- Torques (A2-70, dry):
  - M5: 4.0 N·m
  - M4: 2.2 N·m
  - M3: 1.0 N·m
  - M2: 0.25 N·m

  Use Loctite 243 where the steps say so.

## 1. Sub-assemblies (any order)

1. **Rotor.**
   1. Press the hub sleeve (AM-10) onto the shaft's p6 seat (AM-09) with Loctite 638, against the Ø34
      shoulder. Let it cure.
   2. Bond the KBM rotor onto the sleeve with EA 934NA. Use a room-temperature cure: Kollmorgen says never
      cure the rotor bond above 82 °C outside the stator.
   3. Keep the rotor away from steel swarf. Its magnets pick it up.
2. **Stator into the housing.**
   1. Slide the KBM stator in from the rear of the housing (AM-01) with Scotch-Weld 2214 in the six adhesive
      grooves, against the Ø81 depth-stop ledge.
   2. Lead the phase and PTC wires out to the rear before the adhesive goes on.
   3. Cure as 3M's schedule for 2214, within the stator's temperature limit.
3. **Flange and ring gear.**
   1. Press the ring gear (AM-15) into the front flange (AM-04) from the front, against the lip, with
      Loctite 638.
   2. Check the gear's runout to the flange spigot.
4. **Carrier.**
   1. Press the HK1210 (12 × 16 × 10) into the carrier's Ø16 N6 seat (AM-06). Press on the stamped end only,
      with a stepped mandrel.
   2. Press one HK0609 into each planet (AM-14).
   3. Grease the needles with Isoflex Topas NB 52.
5. **Encoder hub.**
   1. Screw the AksIM-2 ring to the encoder hub (AM-11) with 8 × M2 × 6 countersunk screws and Loctite 243.
   2. Don't touch the rubber magnet face, and keep it away from steel tools.

## 2. Gear stage and output bearing (front)

1. Press the CRBH 3510 crossed-roller bearing onto the carrier's Ø35 h5 sleeve, against the Ø41 shoulder, and fit
   the DIN 471 35 retaining ring. Press on the inner ring only.
2. Drop the planets into the carrier and push the three planet pins (6 × 18, hardened) through the carrier and
   the needle bearings. Put the sun between the planets.
3. Bolt the carrier disk (AM-07) on with 3 × M4 × 16 countersunk (Loctite 243). The sun is now caught between
   the carrier's rear plate and its front disk.
4. Check by hand: the planets turn freely, with no tight spot through a full turn of the sun.

## 3. Into the housing

1. Slide the rotor in from the rear, through the stator. Hold the shaft by its ends, because the magnets pull
   it hard against the stator.
2. From the front, fit the carrier with its crossed-roller bearing into the housing's Ø60 H7 seat. The sun slides
   onto the shaft's double-D (10.8 across the flats) and the shaft's needle journal enters the HK1210.
3. **Face the clamp ring to the parts you have** (AM-08 note 6). Measure, at 20 °C:
   - B, the crossed-roller bearing's width (it can be up to 0.12 under 10.00);
   - d, the housing's seat depth below its front face (11.50 −0.02);
   - R, the flange's Ø90 recess depth (1.00 ±0.01).

   Face the clamp ring's top to H = R + d − B + 0.02 (±0.01). With nominal parts that is 2.52. Keep the faces
   parallel within 0.01.
4. Lay the clamp ring on the bearing's outer ring.
5. Fit the flange and ring gear over the planets. Turn the output slowly by hand until the ring teeth engage,
   then push the flange home on the clamp ring.
6. **Centre the ring gear on the planets.** Fit the 4 × M5 × 30 finger-tight, then snug them to about 0.5 N·m
   while turning the output by hand through two full turns. The planets push the ring to the middle of the
   fits' clearance. Then torque to 4.0 N·m in a cross pattern, a quarter turn of the output between screws.
7. Check: the output turns through 5 full turns with no tight spot, and the backlash at the output feels the
   same at four points 90° apart. A tight spot once per output turn means the ring is off-centre: loosen and
   repeat step 6.
8. Check the clamp-ring crush: with the screws snug, the flange should stand 0.01–0.03 mm off the housing before
   the final torque. A 0.05 feeler must not enter between the flange and the housing after it.

## 4. Rear bearing, end bell and encoder

1. Press the 6001-2RS into the end bell (AM-02) and fit the DIN 472 28 ring.
2. Fit the first DIN 471 12 ring on the shaft. Slide the end bell over the shaft and onto the housing's rear
   spigot. Fit the second DIN 471 12 ring behind the bearing.
3. Fit 4 × M4 × 16 at 2.2 N·m.
4. Screw the 4 standoffs (AM-12) into the end bell's M2 holes with Loctite 243.
5. Slide the encoder hub and ring onto the shaft's g6 seat with Loctite 638 and a 0.50 mm shim against the end
   bell, as on the AM-11 note. Lock the M2 set screw, then remove the shim once the Loctite has cured.
6. Mount the AksIM-2 readhead on the standoffs with 4 × M2 × 6, sensor side toward the ring. Plug in the
   encoder cable.
7. Power the encoder alone (5 V from the drive's X10, or the RLS E201 interface) and turn the shaft by hand. The
   readhead's LED must be green all the way round. If it isn't, shim the standoffs with the RLS shims.
8. Optional: with a gaussmeter, check that the field at the ring is under 20 mT (RLS limit). If it isn't, fit a
   0.5 mm steel shield disk between the end bell and the ring.
9. Feed the cable out through the Ø7 hole and fit the rear cap (AM-03) with 3 × M3 × 25 at 1.0 N·m.

## 5. Pedestal

1. Press the two 4 m6 dowels into the pedestal (AM-05).
2. Put a thin film of thermal paste on the saddle.
3. Lower the housing onto the dowels and fit 4 × M5 × 20 from below at 4.0 N·m (Loctite 243).
4. Route the motor and encoder cables out through the side port to the M12 sockets.

## 6. Done

Go to [TEST.md](TEST.md) for the first power-up. Don't run the motor before the drive's current limits are
set as described there.
