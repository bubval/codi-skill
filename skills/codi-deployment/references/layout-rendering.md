# CoDi Deployment Layout and Rendering

## Layout Behavior

- Clouds, regions, networks, clusters, and namespaces render as nested containers/swimlanes.
- Placement edges are styled differently from traffic edges; public unencrypted traffic is highlighted.

## Render Commands

```bash
codi render diagram.codi --format svg -o diagram.svg
codi render diagram.codi --theme dark --format svg -o diagram-dark.svg
codi render diagram.codi --ratio 16:9 --width 1280 --format svg -o diagram-wide.svg
```

## Guidance

- Prefer SVG for documentation and review.
- Use PNG only when explicitly requested or required.
- Use `--ratio`, `--width`, `--height`, or `--size` as CLI flags; do not put render targets in `.codi` source.
- Use an explicit `direction` under `layout:` when layout direction matters more than target aspect ratio.
