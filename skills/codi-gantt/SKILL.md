---
name: codi-gantt
description: Author, edit, validate, render, and troubleshoot CoDi `gantt` diagrams. Use for Project plans, timelines, milestones, resources, dependencies, lanes, groups, deadlines, and critical path views. Assumes the `codi-cli` skill is installed for shared CLI commands, validation, rendering, and common .codi grammar.
---

# CoDi Gantt

## Requirement

This skill assumes the `codi-cli` skill is installed. Use `codi-cli` for shared `.codi` grammar, `codi help`, `codi validate`, `codi render`, scan, diff, and diagnostic workflow.

## Use This Diagram Type For

- You need schedule, dates, durations, resources, milestones, dependencies, and progress.
- You need a timeline/table render rather than a node-link graph.

## Avoid This Diagram Type When

- You need a generic process without calendar semantics; use flowchart or activity.

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
- `references/examples/01-gantt-product-launch.codi`
- `references/examples/02-gantt-resource-plan.codi`
- `references/examples/03-gantt-critical-path.codi`
