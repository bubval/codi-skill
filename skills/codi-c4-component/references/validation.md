# CoDi C4 Component Validation

## Main Rules

- Components should sit inside the scoped container boundary.
- Crossing relationships to containers or systems should declare protocol, technology, tech, or transport.

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
