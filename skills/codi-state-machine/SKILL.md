---
name: codi-state-machine
description: Author, edit, validate, render, and troubleshoot CoDi `state-machine` diagrams. Use for UML-style state machines with states, transitions, composite states, regions, history, and pseudostates. Assumes the `codi-cli` skill is installed for shared CLI commands, validation, rendering, and common .codi grammar.
---

# CoDi State Machine

## Requirement

This skill assumes the `codi-cli` skill is installed. Use `codi-cli` for shared `.codi` grammar, `codi help`, `codi validate`, `codi render`, scan, diff, and diagnostic workflow.

## Use This Diagram Type For

- You need lifecycle/state behavior rather than process steps.
- Events, guards, actions, entry/do/exit behavior, and composite states matter.
- You need validation of pseudostate and transition rules.

## Avoid This Diagram Type When

- You need ordered interactions between participants; use sequence.
- You need business process flow; use activity or flowchart.

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
- `references/examples/01-state-machine-order.codi`
- `references/examples/02-state-machine-composite.codi`
- `references/examples/03-state-machine-regions.codi`
