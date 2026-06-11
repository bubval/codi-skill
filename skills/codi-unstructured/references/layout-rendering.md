# CoDi Unstructured Layout and Rendering

## Layout Behavior

- Defaults to organic/force-style layout.
- Structured direction and nesting can make layout more regular.
- Wide/tall render targets can tune spacing and spread.

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
- Use explicit source `direction` when layout direction matters more than target aspect ratio.
