---
name: codi-c4-component
description: Author, edit, validate, render, and troubleshoot CoDi `c4-component` diagrams. Use for C4 component diagrams showing components inside one container and nearby containers/systems. Assumes the `codi-cli` skill is installed for shared CLI commands, validation, rendering, and common .codi grammar.
---

# CoDi C4 Component

## Requirement

This skill assumes the `codi-cli` skill is installed. Use `codi-cli` for shared `.codi` grammar, `codi help`, `codi validate`, `codi render`, scan, diff, and diagnostic workflow.

## Use This Diagram Type For

- You need controllers, services, adapters, modules, or other components inside one container.
- You need to show how components interact with neighboring containers and systems.

## Avoid This Diagram Type When

- You need container-level deployment/runtime structure; use codi-c4-container.
- You need class/code internals; use codi-c4-code or codi-class.

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
- `references/examples/01-c4-component-payment-service.codi`
- `references/examples/02-c4-component-notification-service.codi`
- `references/examples/03-c4-component-ingestion-service.codi`
