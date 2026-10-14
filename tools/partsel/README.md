# partsel: part selector

Checks candidate bought parts against a project's requirements and says which ones fit, which don't and why,
with every number traced back to the vendor document it came from. Plain Python 3.11+, no installs.

```
python3 tools/partsel/partsel.py unknown-machine/requirements/motor.toml           # summary table
python3 tools/partsel/partsel.py unknown-machine/requirements/motor.toml --detail  # reasons + a source for every value
python3 tools/partsel/partsel.py unknown-machine/requirements/motor.toml --json    # for other tools
python3 tools/partsel/partsel.py unknown-machine/requirements/motor.toml --brief   # one line per part
python3 tools/partsel/partsel.py unknown-machine/requirements/motor.toml --brief --set bus_vdc=48   # what-if
```

`--set key=value` overrides a value in the requirements' `[operating]` table for one run (repeatable), so
"what if we used a 48 V drive, or ran at 4000 rpm?" needs no file edit.

Verdicts: **PASS** (every hard check met), **FAIL** (a hard check not met), **CHECK** (nothing failed, but the
card is missing a value a check needs, so the part can't be confirmed yet). Checks marked `prefer = true`
(supplier country, mass) only change the ranking.

## Part cards

One TOML file per orderable part in [`parts/<category>/`](../../parts/). Each value names its source and page:

```toml
id = "kollmorgen-kbm-17h01-b"
category = "frameless-motors"
maker = "Kollmorgen"
country = "US"
model = "KBM-17H01-B00"

[sources]
catalog = { title = "Kollmorgen KBM Series Selection Guide", url = "https://..." }

[values]
stator_od_mm = { v = 84.963, src = "catalog", page = 19 }
kb_vrms_per_krpm = { v = 41.2, src = "catalog", page = 20 }
```

Copy the numbers exactly as the datasheet prints them. Leave a value out rather than guess: the selector
reports it as missing instead of passing the part.

## Requirements

One TOML file per need, kept with the project (e.g. `unknown-machine/requirements/motor.toml`): the category,
an operating point and a list of checks.

```toml
category = "frameless-motors"

[operating]
speed_rpm = 3000
bus_vdc = 325

[[check]]
field = "bus_vdc_needed"   # derived from the card and the operating point
max = "bus_vdc"            # a string limit refers to an [operating] value
why = "Back-EMF at the duty speed must stay under the drive's DC bus"
```

Check keys: `min`, `max`, `equals`, `in`, plus `prefer = true` for soft checks and `why` for the report.

## Derived values

Worked out from a card and the operating point, so cards only hold what the vendor publishes:

| Field | How |
|---|---|
| `bus_vdc_needed` | Back-EMF constant × speed × √2 × 1.15 (peak line-line voltage plus 15% for IR drop and control headroom); or, without a back-EMF constant, the rated bus scaled by speed |
| `current_at_peak_torque_arms` | Required peak torque ÷ torque constant |

Add a new derived value in `derived()` in `partsel.py` when a new kind of part needs one.

## Demo video

[`demo/partsel-demo.mp4`](demo/partsel-demo.mp4) (65 s) walks through choosing the unknown-machine motor:
the requirements, a part card, `--brief`, `--detail`, two `--set` what-ifs and the hand checks. It is
rendered by `python3 tools/partsel/demo/make_video.py` (needs Pillow and ffmpeg). The script runs every command
it shows, so re-rendering after a change shows the tools' current output.
