# Readhead standoff (new part), 4 off

STEP: [`step/standoff.step`](step/standoff.step) (at its own origin: stud along +Z, body along −Z). Source:
`source/components/standoff.py`, design revision 48.

Holds the RLS AksIM-2 readhead MB039DCC18BENT00 on the end bell's rear face, at R24.5 on the readhead's four holes
(0°, 60°, 120°, 180°).

| | |
|---|---|
| Quantity | 4 per actuator (order a few spare) |
| Material | AISI 303 (1.4305) |
| Stock | Ø5 bar |
| Finish | Passivate |
| Process | Sliding-head (Swiss) or bar lathe: turn, thread the stud (M2-6g × 4), drill and tap the other end (M2-6H × 5), part off, face to length. 1–2 ops |

| Feature | Size and tolerance | Why |
|---|---|---|
| Body | Ø4.0 ±0.05 × **7.38 −0.02/−0.05** long (shoulder face to readhead face) | Sets the ring-to-readhead gap: RLS needs 2.88 ±0.13 from the ring mounting face to the readhead mounting surface. Make all four in one batch, length matched within 0.01, and shim with RLS MB-ACC shims until the readhead LED shows green |
| End faces | Parallel 0.01, perpendicular to the axis 0.01 | Readhead tilt < 0.2° |
| Stud | M2-6g × 4.0; a DIN 76 thread undercut at the shoulder is allowed (not in the model) | Screws into the end bell's M2 holes (Loctite 243) |
| Tapped end | M2-6H, drill Ø1.6 × 5 flat bottom, 4.4 min full thread | ISO 4762 M2 × 6 through the readhead PCB (4.4 engaged) |
| Edges | 0.2 × 45° | |

Alternative: bought M2 male-female round standoffs (Ø4, 303 or brass) faced to 7.36 ±0.01.

## DFM review

No findings beyond the general notes: a plain turned part. Its length is the critical number.
