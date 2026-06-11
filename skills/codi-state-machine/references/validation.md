# CoDi State Machine Validation

## Main Rules

- Reserved pseudostate names must match their type.
- Initial pseudostates must not have incoming transitions.
- Transitions from initial pseudostates must not set trigger or guard.
- Final and terminate pseudostates must not have outgoing transitions.
- Choice pseudostates require guarded outgoing transitions.
- Fork/join arity is validated.
- Node names must be unique within a scope, or references must be qualified.

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
