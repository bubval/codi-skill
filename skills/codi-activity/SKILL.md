---
name: codi-activity
description: Author, edit, validate, render, and troubleshoot CoDi `activity` diagrams. Use for UML-style activity diagrams with actions, object flows, control nodes, swimlanes, forks, joins, and regions. Assumes the `codi-cli` skill is installed for shared CLI commands, validation, rendering, and common .codi grammar.
---

# CoDi Activity

## Requirement

This skill assumes the `codi-cli` skill is installed. Use `codi-cli` for shared `.codi` grammar, `codi help`, `codi validate`, `codi render`, scan, diff, and diagnostic workflow.

## Use This Diagram Type For

- You need UML activity semantics rather than a generic flowchart.
- You need swimlanes/partitions, object nodes, pins, forks, joins, or guarded decisions.
- You need validation for object-flow versus control-flow mistakes.

## Avoid This Diagram Type When

- You only need a simple process sketch; use flowchart.
- You need state over time; use state-machine.

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
- `references/examples/01-activity-approval-workflow.codi`
- `references/examples/02-activity-object-flow.codi`
- `references/examples/03-activity-swimlane-handoff.codi`
