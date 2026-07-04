# CoDi Activity Authoring Guide

## Purpose

UML-style activity diagrams with actions, object flows, control nodes, swimlanes, forks, joins, and regions.

## Choose This Type When

- You need UML activity semantics rather than a generic flowchart.
- You need swimlanes/partitions, object nodes, pins, forks, joins, or guarded decisions.
- You need validation for object-flow versus control-flow mistakes.

## Prefer Another Type When

- You only need a simple process sketch; use flowchart.
- You need state over time; use state-machine.

## Minimal Shape

```yaml
Approval[activity]:
  - start[initial-node]
  - Review[action]
  - done[activity-final-node]
  - start --> Review
  - Review --> done
```

## Production Pattern

- Declare important nodes before edges.
- Use stable names because CoDi identity is name-based.
- Add labels on relationships where the validator or reader benefits from intent.
- Prefer structured properties over overloaded labels when a property exists.
- Keep layout under `layout:` and colors under `style:`; semantic properties stay top-level.
- Keep examples valid by running `codi validate`.
- Use `codi help render` before assuming installed render flags.

## Common Mistakes

- Referencing an undeclared edge endpoint.
- Mixing a diagram type's vocabulary with a lower-level or unrelated diagram type.
- Using the removed `children:` keyword. Children are plain nested list items.
- Using dropped aliases such as `color`, `border`, `tech`, or the bare `style: dashed` scalar.
- Using a render target as source syntax. Render size belongs on the CLI, not in `.codi`.
- Relying on stale command flags instead of `codi help <command>`.
