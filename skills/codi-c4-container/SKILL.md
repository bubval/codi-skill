---
name: codi-c4-container
description: Author, edit, validate, render, and troubleshoot CoDi `c4-container` diagrams. Use for C4 container diagrams showing deployable/runtime containers inside one software system. Assumes the `codi-cli` skill is installed for shared CLI commands, validation, rendering, and common .codi grammar.
---

# CoDi C4 Container

## Requirement

This skill assumes the `codi-cli` skill is installed. Use `codi-cli` for shared `.codi` grammar, `codi help`, `codi validate`, `codi render`, scan, diff, and diagnostic workflow.

## Use This Diagram Type For

- You need services, apps, databases, queues, or deployable units inside a scoped system.
- You need neighboring users/systems around those containers.

## Avoid This Diagram Type When

- You only need system context; use codi-c4-context.
- You need internals of one container; use codi-c4-component.

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
- `references/examples/01-c4-container-saas-analytics.codi`
- `references/examples/02-c4-container-retail-checkout.codi`
- `references/examples/03-c4-container-open-banking.codi`
