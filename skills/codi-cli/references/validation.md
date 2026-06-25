# Validation and Diagnostics

Validation is separate from parsing. A diagram can parse successfully and still
fail validation because its vocabulary, endpoints, properties, or type-specific
rules are wrong.

## Commands

```bash
codi validate diagram.codi
codi validate diagram.codi --strict
codi validate diagram.codi --format json
cat diagram.codi | codi validate - --source-name editor.codi --format json
```

Render also validates before producing output:

```bash
codi render diagram.codi --format svg -o diagram.svg
```

## Diagnostic Shape

Core diagnostics include:

- `severity`: `critical`, `error`, `warning`, or `info`
- `code`: stable diagnostic code
- `message`: human-readable message
- optional `validator`
- optional `file`
- optional `line`
- optional `column`
- optional `path`
- optional `point`
- optional `node`
- optional `edge`
- optional `member`

`critical` and `error` diagnostics fail validation. `warning` and `info`
diagnostics report issues without failing the command unless a validator
promotes them in strict mode.

## Parse Diagnostics

The CLI reports parser and IO failures as diagnostics:

| Code | Meaning |
|---|---|
| `CODI-IO-001` | Source file or stdin could not be read |
| `CODI-PARSE-001` | YAML or semantic parse failed |
| `CODI-VALIDATOR-RUNTIME-001` | Python validator failed at runtime |

## Source Mapping

`codi validate` builds a source map from the original source text. Diagnostics
are enriched by matching:

- explicit diagnostic `path`
- node name
- edge endpoints
- class member

If a precise line/column cannot be found, the diagnostic still includes the
best available node, edge, path, or point.

## Built-In Validators

Default validators are embedded in the native CLI:

| Diagram type | Validator |
|---|---|
| `activity` | `activity.py` |
| `c4-context` | `c4_context.py` |
| `c4-container` | `c4_container.py` |
| `c4-component` | `c4_component.py` |
| `c4-code` | `c4_code.py` |
| `class` | `class_diagram_new.py` |
| `deployment` | `deployment.py` |
| `flowchart` | `flowchart.py` |
| `gantt` | `gantt.py` |
| `sequence` | `sequence.py` |
| `state-machine` | `state_machine.py` |
| `threat-model` | `threat_model.py` |
| `unstructured` | `unstructured.py` |

The validator catalog is the authority for what the CLI treats as a built-in
diagram type. A parser may accept any top-level type string, but the CLI needs a
default validator or `--type-path`.

## Strict Mode

`--strict` asks validators to enforce stronger conventions where supported.

Examples:

- C4 warnings such as missing relationship labels can be promoted.
- Threat models without authored threats may report additional information.
- Gantt and class validators may apply more opinionated checks.

Strict mode is not a separate grammar. It is a validation policy.

## Custom Diagram Types

Run a full custom diagram type:

```bash
codi validate custom.codi --type-path ./custom_type.py
codi render custom.codi --type-path ./custom_type.py --format svg -o custom.svg
```

For custom types, the CLI calls Python hooks for expansion, validation, and
layout. For built-in diagram types, `--type-path` can also provide a validation
override where supported by the CLI.

## Common Validation Failures

| Problem | Typical cause | Fix |
|---|---|---|
| Unknown diagram type | Top-level `[type]` is not built in | Use a built-in type or pass `--type-path` |
| Unknown node type | Node type not in the diagram vocabulary | Use the type vocabulary in [diagram-types.md](./diagram-types.md) |
| Unknown endpoint | Edge references a node name that was not declared | Add the node or fix spelling |
| Duplicate node name | Same name appears more than once in a scope | Rename or intentionally nest where supported |
| Missing scope | C4 zoom-level diagram has no scoped system/container/component | Mark one element with `scope: true` or `, scope` |
| Missing label | Relationship type expects a descriptive label | Add a scalar label or `label:` |
| Invalid property | Property is unsupported for that type or node | Move, rename, or remove the property |

## Validation Strategy for Docs

Documentation examples should satisfy:

```bash
codi validate docs-example.codi
codi render docs-example.codi --format svg -o docs-example.svg
```

Use `--strict` for examples that should demonstrate best practice. Do not
require strict mode for intentionally compact examples unless the warnings are
documented.
