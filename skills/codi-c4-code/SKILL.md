---
name: codi-c4-code
description: Author, edit, validate, render, and troubleshoot CoDi `c4-code` diagrams. Use for C4 code-level diagrams showing classes, interfaces, functions, modules, and packages inside one component. Assumes the `codi-cli` skill is installed for shared CLI commands, validation, rendering, and common .codi grammar.
---

# CoDi C4 Code

## Requirement

This skill assumes the `codi-cli` skill is installed. Use `codi-cli` for shared `.codi` grammar, `codi help`, `codi validate`, `codi render`, scan, diff, and diagnostic workflow.

## Use This Diagram Type For

- You need code-level architecture inside one component.
- You want C4 context plus class-like structure and structural relationship validation.

## Avoid This Diagram Type When

- You only need pure UML/domain classes; use codi-class.
- You need component-level architecture; use codi-c4-component.

## Authoring Workflow

1. Read `references/authoring.md` for diagram selection and common patterns.
2. Read `references/vocabulary.md` and `references/properties.md` before writing detailed nodes or edges.
3. Use examples from `references/examples/` as source templates.
4. Validate with `codi validate <file>`.
5. Render with `codi render <file> --format svg -o <file.svg>` when the CLI is available.

## References

- Structure and grammar: `references/grammar.md`
- Node and edge vocabulary: `references/vocabulary.md`
- Valid properties: `references/properties.md`
- Validation rules and common repairs: `references/validation.md`
- Layout and rendering behavior: `references/layout-rendering.md`
- Examples:
- `references/examples/01-c4-code-payment-module.codi`
- `references/examples/02-c4-code-event-handler.codi`
- `references/examples/03-c4-code-repository-layer.codi`
