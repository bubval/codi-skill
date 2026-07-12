# CoDi C4 Code Validation

## Main Rules

- Structural relationships are type-checked.
- `implements` must target an interface or trait.
- Code elements should be inside the scoped component or package boundary.

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
