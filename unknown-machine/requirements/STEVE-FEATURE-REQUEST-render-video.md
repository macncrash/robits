# Feature request: render an animated design to video through the MCP

**Goal:** an agent should be able to make the same video I recorded by hand for
Unknown machine – planetary joint actuator, rev 49: the `teardown` exploded-view
animation playing while the camera orbits the assembly, saved as an MP4. Today I
have to screen-record the app and drag the view myself.

Reference recording: `rev49-unknown.mov` (21.6 s, 1920×1128 @ 60 fps, H.264). It
captures the STEVE window (the viewport, the Inspector panel and the animation
timeline) while the 15.5 s `teardown` animation plays and I orbit the
orthographic camera by hand from iso round to bottom and back views.

## What the MCP can do today

`inspect_model(document_id, animation=, t=, view=)` returns **one still image** at
one moment of an animation, from one of four fixed views
(`isometric`, `top`, `front`, `right`). There's no camera control, no video and no
way to capture the app UI.

## What the MCP can't do yet

1. **Video output.** I'm asking for a `render_video` tool (or a mode of
   `inspect_model`) that plays an animation over time and returns MP4 or WebM.
   STEVE's sister server Gravity already has `render_video`, which could serve as
   the pattern.
2. **Free camera.** Only four preset views exist. Needed:
   - azimuth, elevation and roll
   - a look-at target (a point or an instance)
   - zoom or fit-to-extent
   - orthographic or perspective (my recording is orthographic)
3. **Camera motion over time.** Camera keyframes or a turntable/orbit preset
   (e.g. `{"orbit": {"deg": 360, "elevation": 25}}`, or
   `[(t, az, el, zoom), …]` with easing). This replaces my hand-orbiting, which
   swept through iso, front, bottom and back.
4. **Timing that doesn't follow the animation.** The output length is set
   separately from the animation's: the 15.5 s teardown sat inside a 21.6 s clip.
   That needs playback speed (the UI's ¼×–2×), holds at the start and end, a loop
   count, and a time window `t_start`/`t_end`.
5. **Framing that follows the explode.** An exploded design is much wider than
   the assembled one. In my recording, parts left the frame. I'm asking for a fit
   option over the whole animation (`fit: "animation_extent"`) or a fit that
   tracks each frame.
6. **Capture region and app UI.** A choice between the bare viewport
   (`"viewport"`) and the viewport plus the Inspector and timeline (`"app"`), as
   in my recording. Also toggles for the grid, view cube, axis triad, the
   selection highlight and the timeline scrubber.
7. **Output settings:** width and height (or an aspect ratio), fps, format
   (mp4/webm/gif), quality or bitrate, background colour, and shading (edges on
   or off, materials). An optional poster frame would help.
8. **Delivery and long jobs.** Rendering will run longer than one call, so the
   tool should follow `generate_model`'s pattern: `still_working` plus progress,
   where calling again joins the same job. The file should come back the way
   `download=[…]` already works (a one-time curl URL) and be attached to the
   revision.

## Sketch of the call

```python
render_video(
  document_id, revision=49,
  animation="teardown", speed=1.0, hold_start_s=1, hold_end_s=5,
  camera={"projection": "orthographic", "fit": "animation_extent",
          "keys": [(0, {"az": 45, "el": 30}), (8, {"az": 160, "el": 10}),
                   (14, {"az": 250, "el": -40}), (21.6, {"az": 405, "el": 30})],
          "easing": "ease"},
  capture="app",            # or "viewport"
  size=(1920, 1128), fps=60, format="mp4",
  overlays={"grid": True, "view_cube": True, "triad": True},
  download=True,
)
```

## Nice to have

A "record my camera" option, where the UI saves the path I orbit by hand as
camera keyframes in the design (like `design.animation`, maybe
`design.camera_path(...)`). An agent could then re-render that exact path at any
later revision.
