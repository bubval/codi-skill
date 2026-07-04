# CoDi Activity Validation

## Main Rules

- Initial nodes must not have incoming flow.
- Final nodes must not have outgoing flow.
- Decision nodes should have at least two guarded outgoing flows.
- Fork/join arity is validated.
- Object flows must connect actions/object nodes/pins/parameters/expansion nodes.
- Pins should be nested under actions.

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
- Replace unsupported properties with entries from `properties.md`; move layout keys under `layout:` and color keys under `style:`.
- Replace the removed `children:` keyword with plain nested list items.
- Add relationship labels where the diagram type expects them.
