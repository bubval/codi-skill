---
name: codi-sequence
description: Author, edit, validate, render, and troubleshoot CoDi `sequence` diagrams. Use for Ordered interactions over time between actors, services, systems, databases, and objects. Assumes the `codi-cli` skill is installed for shared CLI commands, validation, rendering, and common .codi grammar.
---

# CoDi Sequence

## Requirement

This skill assumes the `codi-cli` skill is installed. Use `codi-cli` for shared `.codi` grammar, `codi help`, `codi validate`, `codi render`, scan, diff, and diagnostic workflow.

## Use This Diagram Type For

- Explaining request/response flows, login flows, async work, callbacks, retries, or lifecycle behavior.
- Source order matters and messages should appear vertically in time order.
- You need sequence-specific constructs such as activation, replies, notes, and fragments.

## Avoid This Diagram Type When

- The goal is static system topology; use C4 or unstructured instead.
- The goal is a generic process with decisions and parallel branches; use activity or flowchart.

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
- `references/examples/01-sequence-auth-login.codi`
- `references/examples/02-sequence-lifecycle-fragments.codi`
- `references/examples/03-sequence-notes-replies.codi`
