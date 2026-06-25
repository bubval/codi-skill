# CoDi CLI Reference

Use the `codi` CLI when it is available. Before any command, confirm it is reachable with `command -v codi` (this also matches a shell alias or function, not just a binary on `PATH`).

If `codi` is not found, the CLI is unavailable. Do not fabricate output: never hand-write or otherwise fake an SVG, PNG, validation report, diff, or expanded result in place of the CLI — there is no fallback renderer or validator. Refuse the action and tell the user that `codi` could not be located and must be on `PATH` or exposed as an alias/function. You may still author or edit `.codi` source from the references, but state plainly that it was not validated or rendered.

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

Scan a source directory or GitHub repository and generate a `class` diagram with
inferred relationships:

```bash
codi scan ./src
codi scan ./src --name MyProject -o classes.codi
codi scan https://github.com/org/repo --source-kind github -o repo.codi
codi scan ./src -o classes.codi --render-svg classes.svg
codi scan ./src --render-png classes.png --ratio 16:9 --width 1600
```

`codi scan` always produces a class diagram. Output goes to stdout unless `-o` is
given. The generated diagram is named `Dependencies` by default; override with
`--name`.

Source selection:

- `--source-kind auto|local|github` (default `auto`)

Relationship and member detail:

- `--relationship-inference strict|conservative|rich` (default `conservative`)
- `--external-type-resolution off|imports|installed` (default `installed`)
- `--include-generated` include generated source and declaration files
- `--include-member-metadata` include source-language member metadata
- `--include-relationship-evidence` include source relationship evidence
- `--max-members-per-class <n>` (default `1024`)
- `--max-relationships-per-class <n>` (default `512`)
- `--max-total-relationships <n>` (default `10000`)

Rendering the scan output (used with `--render-svg`/`--render-png`):

- `--theme <name|path>`, `--size WIDTHxHEIGHT`, `--ratio`, `--width`, `--height`
- `--raster-scale <n>`, `--max-raster-dimension <n>`

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

## Version

Each `.codi` file has its own local version history (independent of git). Save,
inspect, diff, and restore versions:

```bash
codi version save diagram.codi -m "initial layout"
codi version save diagram.codi --branch experiment
codi version list diagram.codi
codi version list diagram.codi --all --format json
codi version show diagram.codi --version HEAD
codi version status diagram.codi
codi version diff diagram.codi --from v1 --to HEAD
codi version diff diagram.codi --from v1 --to HEAD --render diff.svg --theme dark
codi version restore diagram.codi --version v1 --yes
codi version checkout diagram.codi --version <hash> --yes
```

A version can be referenced by id, label, hash prefix, or `HEAD`.

## Branch

Manage per-file version branches:

```bash
codi branch list diagram.codi
codi branch current diagram.codi
codi branch create diagram.codi experiment --from HEAD
codi branch switch diagram.codi experiment
codi branch switch diagram.codi main --restore --yes
```

`--restore` writes the branch head back into the working file; `--yes` skips the
overwrite confirmation.

## Test

Run embedded snapshot tests where present:

```bash
codi test diagram.codi
codi test fixtures/diagrams
codi test fixtures/diagrams --test render
codi test fixtures/diagrams --update-snapshots
```

The current test runner is partial. Snapshot tests can render SVG and compare or update snapshots. Some documented test forms are parsed but skipped.
