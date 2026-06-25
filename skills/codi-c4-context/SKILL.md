---
name: codi-c4-context
description: Author, edit, validate, render, and troubleshoot CoDi `c4-context` diagrams. Use for C4 system context diagrams showing one software system in scope, its users, and external systems. Assumes the `codi-cli` skill is installed for shared CLI commands, validation, rendering, and common .codi grammar.
---

# CoDi C4 Context

## Requirement

This skill assumes the `codi-cli` skill is installed. Use `codi-cli` for shared `.codi` grammar, `codi help`, `codi validate`, `codi render`, scan, diff, and diagnostic workflow.

## Use This Diagram Type For

- You need a high-level system context for humans and neighboring systems.
- You want to communicate boundaries and external dependencies before container/component detail.
- You need C4 validation for context-level vocabulary.

## Avoid This Diagram Type When

- You need deployable/runtime internals; use codi-c4-container.
- You need code/class internals; use codi-c4-code or codi-class.

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
- `references/examples/01-saas-context.codi`
- `references/examples/02-boundaries-and-metadata.codi`
