---
name: codi-flowchart
description: Author, edit, validate, render, and troubleshoot CoDi `flowchart` diagrams. Use for Generic directed process flows with decisions, stages, nested groups, and readable domain-specific node kinds. Assumes the `codi-cli` skill is installed for shared CLI commands, validation, rendering, and common .codi grammar.
---

# CoDi Flowchart

## Requirement

This skill assumes the `codi-cli` skill is installed. Use `codi-cli` for shared `.codi` grammar, `codi help`, `codi validate`, `codi render`, scan, diff, and diagnostic workflow.

## Use This Diagram Type For

- You need a directed process or decision flow.
- The node vocabulary should remain flexible but the graph should be structured.
- You need nested process groups with directed layout.

## Avoid This Diagram Type When

- You need UML activity semantics such as object flows, pins, partitions, forks, and joins.
- You need a timeline; use Gantt.

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
- `references/examples/01-process-flow.codi`
- `references/examples/02-nested-groups-and-styling.codi`
