# robits

Mechanical "what would this be if it were real?" projects. Each one starts from a concept image, usually
AI-generated, of a machine that doesn't exist. We work out a plausible design intent and model it in 3D
with its internal parts, so it can be taken apart, checked and studied.

Each project lives in its own folder with everything needed to open, view or rebuild it.

## Projects

| Project | What it turned out to be | Folder |
|---|---|---|
| Unknown machine | Robot-joint actuator: BLDC motor + 5:1 planetary gearbox, hollow shaft, encoder, bolted pedestal mount | [`unknown-machine/`](unknown-machine/) |
| Robot arm | Six-axis arm with claw gripper, built from six sizes of the joint actuator; joints, poses and a pick-and-place animation | [`robot-arm/`](robot-arm/) |

## Tools

| Tool | What it does |
|---|---|
| [`tools/partsel/`](tools/partsel/) | Part selector: checks the bought-part cards in [`parts/`](parts/) against a project's requirements and explains every pass and fail, with sources. [65 s demo video](tools/partsel/demo/partsel-demo.mp4) |

## Folder layout

Every project folder follows the same layout:

```
<project>/
  README.md     what it is, how the design was inferred, parts list, caveats
  images/       the reference image and renders of the model
  source/       parametric CAD source (CadQuery / Python), one file per component
  analysis/     stress / strain studies and hand calculations, where done
  requirements/ what bought parts must meet, checked with tools/partsel
  exports/      neutral CAD files: STEP (assembly and per component), STL meshes, DXF where there are flat parts
```

The STEP files open in almost any CAD tool (Fusion, SolidWorks, Onshape, FreeCAD, KiCad, …). STL files are
for viewing and 3D printing.

## Adding a project

1. Create a folder named after the project (lowercase, hyphens).
2. Use the layout above and write a `README.md` covering the reference, the design intent and the caveats.
3. Add a row to the table above.

## License

[MIT](LICENSE). Free to use, copy, modify and share. The designs are speculative concept models and come
**without warranty of any kind**. They are not engineered, tested or certified for any real-world load or use.
