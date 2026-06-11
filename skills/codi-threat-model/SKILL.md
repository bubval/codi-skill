---
name: codi-threat-model
description: Author, edit, validate, render, and troubleshoot CoDi `threat-model` diagrams. Use for STRIDE-compatible data-flow diagrams with trust boundaries, data stores, processes, external entities, and authored threats. Assumes the `codi-cli` skill is installed for shared CLI commands, validation, rendering, and common .codi grammar.
---

# CoDi Threat Model

## Requirement

This skill assumes the `codi-cli` skill is installed. Use `codi-cli` for shared `.codi` grammar, `codi help`, `codi validate`, `codi render`, scan, diff, and diagnostic workflow.

## Use This Diagram Type For

- You need a security data-flow diagram.
- You need trust boundary crossing checks, encryption checks, and authored STRIDE threats.
- You need threat status, severity, mitigations, and data classification.

## Avoid This Diagram Type When

- You need general architecture without security-specific semantics; use C4 or unstructured.

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
- `references/examples/01-threat-model-file-upload.codi`
- `references/examples/02-threat-model-oidc-flow.codi`
- `references/examples/03-threat-model-ci-cd.codi`
