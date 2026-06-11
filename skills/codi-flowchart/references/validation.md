# CoDi Flowchart Validation

## Main Rules

- Duplicate node names and duplicate edges are flagged.
- Direction must be one of `LR`, `RL`, `TB`, or `BT`.
- Numeric layout props must be non-negative.
- `layout_only` nodes should have children.

## Repair Loop

1. Run `codi validate <file>`.
2. Read each diagnostic code, node, edge, and path.
3. Fix the source rather than suppressing diagnostics.
4. Rerun validation.
5. Render only after error and critical diagnostics are gone.

## Strict Mode

Use `codi validate <file> --strict` when producing best-practice examples or documentation diagrams. Strict mode may promote supported convention warnings.

## Common Repairs

- Add missing node declarations for edge endpoints.
- Rename duplicate nodes or intentionally nest them where the type supports scope.
- Replace invalid node/edge types with vocabulary entries from `vocabulary.md`.
- Replace unsupported properties with entries from `properties.md`.
- Add relationship labels where the diagram type expects them.
