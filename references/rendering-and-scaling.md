# Layout and Rendering

Layout turns a validated diagram graph into positioned nodes. Rendering turns
the positioned graph into a scene and then SVG or PNG.

## Layout Result

The shared layout result maps node names to positioned boxes:

```text
name -> { x, y, width, height }
```

Coordinates are center-based in layout code. Render scene code converts those
positions into visual geometry, edge routes, labels, ports, and text blocks.

## Layout Dispatch

The core dispatcher uses `diagram.diagram_type`:

| Diagram type | Layout behavior |
|---|---|
| `sequence` | Formulaic lifelines and ordered message rows |
| `c4-context` | C4 boundary-aware graph layout |
| `c4-container` | C4 boundary-aware graph layout |
| `c4-component` | C4 boundary-aware graph layout |
| `c4-code` | Class/code element layout |
| `class` | UML class layout |
| `flowchart` | Directed graph layout with nested containers |
| `gantt` | Timeline/table layout |
| `activity` | Activity node and swimlane layout |
| `state-machine` | State graph layout, including nested/composite states |
| `threat-model` | Trust-boundary/data-flow layout |
| `unstructured` | Organic or force-style layout |

Unknown internal types fall back to force-directed layout, but the CLI requires
custom type support before rendering unknown user-facing diagram types.

## Direction and Spacing

Several types support layout properties under the diagram-level `layout:`
directive (block form only):

```yaml
- layout:
    direction: LR
    rank_gap: 180
    node_gap: 64
```

Accepted direction vocabulary is generally:

- `LR`: left to right
- `RL`: right to left
- `TB`: top to bottom
- `BT`: bottom to top

Supported spacing keys depend on type. `flowchart`, `unstructured`, C4,
activity, threat-model, deployment, and state-machine diagrams support
diagram-level spacing options; container nodes take their own `layout:` map for
nested spacing. `gantt` and `sequence` are time-based and have no `layout:`
keys.

## Render Targets

The CLI can target exact dimensions or an aspect ratio:

```bash
codi render diagram.codi --format svg --size 1600x900 -o diagram.svg
codi render diagram.codi --format png --width 1200 --height 900 -o diagram.png
codi render diagram.codi --format svg --ratio 16:9 --width 1280 -o diagram.svg
codi render diagram.codi --format svg --ratio 4:3 --height 900 -o diagram.svg
```

Rules:

- `--ratio` accepts forms like `16:9`, `4/3`, or `1.777`.
- `--size <WxH>` sets exact output dimensions and cannot combine with
  `--width`, `--height`, or `--ratio`.
- `--width` with `--height` sets exact output dimensions.
- `--width` with `--ratio` computes height; `--height` with `--ratio` computes
  width.
- `--ratio` alone shapes the export canvas while preserving natural output size.
- Exact target dimensions affect the SVG root `width` and `height`.
- For C4, flowchart, and state-machine diagrams, a wide/tall target can provide
  a direction hint when the source has no explicit `direction`.

Render targets are command-line export settings, not `.codi` syntax. Do not add
`aspect_ratio`, `canvas`, or similar sizing keys to source files unless the user
is defining ordinary diagram properties for a custom type.

Common targets:

| Use case | Target |
|---|---|
| Slide/video | `--ratio 16:9 --width 1920` |
| Docs image | `--ratio 16:9 --width 1280` |
| Square thumbnail | `--ratio 1:1 --width 1024` |
| Portrait preview | `--ratio 9:16 --height 1600` |
| Wide dashboard panel | `--ratio 32:9 --width 1920` |
| Exact export | `--size 1600x900` |

Target option constraints:

- `--size` must use `WIDTHxHEIGHT`, such as `1600x900`.
- `--size` cannot combine with `--width`, `--height`, or `--ratio`.
- `--width` alone requires `--height` or `--ratio`.
- `--height` alone requires `--width` or `--ratio`.
- `--width` with `--height` sets exact dimensions.
- `--width` with `--ratio` computes height.
- `--height` with `--ratio` computes width.
- `--ratio` accepts `16:9`, `16/9`, or decimal forms such as `1.777`.
- `--raster-scale` is rejected for exact PNG targets.

## Scene Detail

`--detail` controls how much scene information is rendered:

```bash
codi render diagram.codi --detail full
codi render diagram.codi --detail interactive
codi render diagram.codi --detail overview
```

Use `full` for documentation unless testing a specific overview or interactive
surface.

## Themes

Themes are selected during render:

```bash
codi render diagram.codi --theme light --format svg -o diagram.svg
codi render diagram.codi --theme dark --format svg -o diagram-dark.svg
codi render diagram.codi --theme ./theme.yml --format svg -o themed.svg
```

The renderer applies theme colors to node fills, strokes, text, edge labels,
markers, boundaries, and diff accents.

## SVG Rendering

SVG is generated from the render scene. The SVG renderer handles:

- root viewport and background
- node shapes
- class compartments
- sequence lifelines and activations
- edge lines, markers, and labels
- C4 type labels
- activity and state-machine glyphs
- Gantt table/timeline payloads
- diff badges and metadata where used

Use SVG for docs and regression review because it is deterministic and
text-diffable.

## PNG Rendering

PNG output rasterizes SVG:

```bash
codi render diagram.codi --format png -o diagram.png
codi render diagram.codi --format png --raster-scale 2 -o diagram@2x.png
codi render diagram.codi --format png --max-raster-dimension 4096 -o diagram.png
```

PNG is best for screenshots, release artifacts, and documents that cannot embed
SVG. `--raster-scale` applies only to non-exact PNG output; exact PNG output
from `--size`, `--width --height`, or ratio-computed dimensions already defines
the final pixel size. `--max-raster-dimension 0` disables the PNG dimension cap.

## Focus Rendering

`--node <name>` renders a focused source node:

```bash
codi render source.codi --node PaymentService --format svg -o payment-service.svg
```

Class packages use package focus rendering. Other supported nodes render as
single-node or local-focus scenes depending on type and available context.
