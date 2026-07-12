# CoDi Gantt Authoring Guide

## Purpose

Project plans, timelines, milestones, resources, dependencies, lanes, groups, deadlines, and critical path views.

## Choose This Type When

- You need schedule, dates, durations, resources, milestones, dependencies, and progress.
- You need a timeline/table render rather than a node-link graph.

## Prefer Another Type When

- You need a generic process without calendar semantics; use flowchart or activity.

## Minimal Shape

```yaml
LaunchPlan[gantt]:
  - Design[task]:
      start: 2026-06-10
      duration: 5d
  - Launch[milestone]:
      date: 2026-07-01
      depends_on:
        - Design
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
