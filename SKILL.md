---
name: codi
description: Create, edit, validate, render, scan, and explain CoDi .codi architecture diagram files. Use when working with .codi files or when the user asks for C4, sequence, class, flowchart, activity, state-machine, threat-model, Gantt, unstructured, or source-scanned diagrams in CoDi.
---

# CoDi

## Core Workflow

CoDi source is YAML with one top-level `DiagramName[diagram-type]` key and a list body. Use this skill to author `.codi` files, edit existing diagrams, run validation, render SVG/PNG output, and troubleshoot diagnostics.

Follow this loop:

1. Pick the diagram type from `references/diagram-types.md`.
2. Read only the relevant reference files for the task.
3. Write or edit the `.codi` source.
4. Run `codi validate <file>`.
5. Fix any error or critical diagnostics.
6. Render documentation output with `codi render <file> --format svg -o <file.svg>`.

Prefer SVG for documentation, review, and regression artifacts. Use PNG only when the user asks for raster output or needs compatibility with a tool that cannot embed SVG.

## Reference Routing

- Syntax, YAML shape, bracket annotations, arrows, and nesting: `references/grammar.md`
- Diagram type selection, node vocabulary, edge vocabulary, and type-specific examples: `references/diagram-types.md`
- Diagnostics, strict mode, common failures, and repair strategy: `references/validation.md`
- CLI commands for validate, render, scan, expand, diff, and test: `references/cli.md`
- Output size, aspect ratio, themes, scene detail, SVG, PNG, and focus rendering: `references/rendering-and-scaling.md`
- Concrete source examples: `references/examples/*.codi`

Load examples by diagram type instead of reading the full examples directory. Good defaults:

- C4 context: `references/examples/c4-context-retail-platform.codi`
- C4 container: `references/examples/c4-container-saas-analytics.codi`
- C4 component: `references/examples/c4-component-payment-service.codi`
- C4 code: `references/examples/c4-code-payment-module.codi`
- Sequence: `references/examples/sequence-auth-login.codi`
- Class: `references/examples/class-domain-model.codi`
- Flowchart: `references/examples/flowchart-release-gate.codi`
- Activity: `references/examples/activity-approval-workflow.codi`
- State machine: `references/examples/state-machine-order.codi`
- Threat model: `references/examples/threat-model-file-upload.codi`
- Gantt: `references/examples/gantt-product-launch.codi`
- Unstructured: `references/examples/unstructured-service-map.codi`

## CLI Availability

Before promising rendered output, verify that the `codi` CLI is available:

```bash
scripts/codi-doctor.sh
```

If the CLI is missing, still author or edit `.codi` source from the bundled references, but tell the user validation/rendering could not be run locally.

For the standard validate-and-render loop, use:

```bash
scripts/codi-validate-render.sh diagram.codi diagram.svg
```

## Authoring Rules

- Use exactly one top-level diagram per `.codi` file.
- Always annotate the top-level diagram with a diagram type, such as `System[c4-context]:`.
- Prefer declared nodes before edges that reference them.
- Use `-->`, `<--`, or `<-->` for generic edges.
- Quote labels that contain punctuation, spaces, colons, dates, or symbols.
- Use `children:` for nested nodes unless matching an example that uses a direct nested sequence.
- Keep names stable when editing existing diagrams because CoDi identity is name-based.
- When validation fails, fix the source and rerun validation before rendering.

## Diagram Type Defaults

- Use `c4-context` for system context and external actors/systems.
- Use `c4-container` for deployable/runtime containers inside one system.
- Use `c4-component` for components inside one container.
- Use `c4-code` for code-level structure inside a component.
- Use `sequence` for ordered interactions over time.
- Use `class` for UML class/interface/enum/package models.
- Use `flowchart` for generic directed process flows.
- Use `activity` for UML activity flows, swimlanes, object flows, forks, joins, and decisions.
- Use `state-machine` for states, transitions, composite states, regions, and pseudostates.
- Use `threat-model` for STRIDE-compatible data-flow diagrams with trust boundaries.
- Use `gantt` for schedules, milestones, dependencies, resources, and timelines.
- Use `unstructured` for permissive sketches, dependency webs, ownership maps, and concept maps.
