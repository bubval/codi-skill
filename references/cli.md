# CoDi CLI Reference

Use the `codi` CLI when it is available on `PATH`. If it is not available, author or edit `.codi` source from the references and report that validation/rendering could not be run.

## Help

Use the installed CLI help as the source of truth for command syntax:

```bash
codi help
codi help render
codi help validate
codi help scan
codi help version save
codi help branch switch
codi <command> --help
```

When generated instructions conflict with `codi help`, trust `codi help`
because it reflects the installed binary.

## Validate

Parse and validate source:

```bash
codi validate diagram.codi
codi validate diagram.codi --strict
codi validate diagram.codi --format json
cat diagram.codi | codi validate - --source-name editor.codi --format json
```

Validation exits with status `1` when any diagnostic has `error` or `critical` severity. Text diagnostics print to stderr. JSON diagnostics print to stdout.

Use `--type-path <file.py>` for custom diagram types or validation overrides.

## Render

Render `.codi` to SVG or PNG:

```bash
codi render diagram.codi
codi render diagram.codi --format svg -o diagram.svg
codi render diagram.codi --format png --raster-scale 2 -o diagram.png
codi render diagram.codi --theme dark --detail overview --format svg -o overview.svg
codi render diagram.codi --size 1600x900 --format svg -o exact.svg
codi render diagram.codi --ratio 16:9 --width 1280 --format svg -o wide.svg
codi render diagram.codi --node PaymentService --format svg -o payment-service.svg
codi render custom.codi --type-path ./custom_type.py --format svg -o custom.svg
```

Render validates before producing output. SVG is the preferred documentation artifact because it is deterministic, inspectable, and diffable.

## Scan

Scan source code and generate `.codi`:

```bash
codi scan ./src
codi scan ./src --name MyProject -o deps.codi
codi scan ./src --mode class --name MyProject -o classes.codi
codi scan https://github.com/org/repo --source-kind github -o repo.codi
codi scan ./src --mode class -o classes.codi --render-svg classes.svg
codi scan ./src --mode class --render-png classes.png --ratio 16:9 --width 1600
```

Modes:

- `dependency`: module dependency diagrams
- `class`: class diagrams with inferred relationships

Useful class scan options:

- `--relationship-inference strict|conservative|rich`
- `--include-generated`
- `--max-relationships-per-class <n>`
- `--max-total-relationships <n>`

## Expand

Inspect canonical output:

```bash
codi expand diagram.codi
codi expand diagram.codi --pretty
codi expand diagram.codi --format codi
codi expand custom.codi --type-path ./custom_type.py --pretty
```

Expansion prints to stdout and fails when expansion diagnostics include errors.

## Diff

Compare two diagrams structurally:

```bash
codi diff old.codi new.codi
codi diff old.codi new.codi --format json
codi diff old.codi new.codi --render diff.svg
codi diff old.codi new.codi --render diff.svg --theme dark
codi diff old.codi new.codi --type-path ./custom_type.py
```

`codi diff` exits `1` when changes are found and `0` when no changes are found.

## Test

Run embedded snapshot tests where present:

```bash
codi test diagram.codi
codi test fixtures/diagrams
codi test fixtures/diagrams --test render
codi test fixtures/diagrams --update-snapshots
```

The current test runner is partial. Snapshot tests can render SVG and compare or update snapshots. Some documented test forms are parsed but skipped.
