# Bought parts: carts by supplier

`by-supplier/*.csv` splits `bom.csv` into one list per supplier, ready to type or paste into each shop's cart.
Every line carries a status:

- **confirmed:** the part number and spec were seen on the supplier's page on 2026-10-14. Order it as listed.
- **to-confirm:** check what the notes say before ordering (class 70, exact code, price).
- **quote:** ask the supplier. This covers the Kollmorgen motor kit (KBM-17H01-B00; confirm the code, the
  inductance and the PTC curve) and the AKD-P00306 drive (ask an authorised distributor which generation is
  current: NBAN, NCAN or NDAN).
- **not yet sourced:** these lines need choosing first.

Request text for Kollmorgen or a distributor:

> Please quote 1 and 5 of: Kollmorgen KBM-17H01-B00 frameless motor kit (or the current equivalent code), and
> AKD-P00306-N?AN-0000 servo drive (current hardware generation), with lead times. Please also confirm the
> KBM-17H01-B00's line-line inductance and PTC resistance curve, and whether the AKD reads the motor PTC on
> X10 pins 8/9 when FB1.SELECT = 34 (BiSS-C).
