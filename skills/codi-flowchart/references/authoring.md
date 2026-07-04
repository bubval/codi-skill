# CoDi Flowchart Authoring Guide

## Purpose

Generic directed process flows with decisions, stages, nested groups, and readable domain-specific node kinds.

## Choose This Type When

- You need a directed process or decision flow.
- The node vocabulary should remain flexible but the graph should be structured.
- You need nested process groups with directed layout.

## Prefer Another Type When

- You need UML activity semantics such as object flows, pins, partitions, forks, and joins.
- You need a timeline; use Gantt.

## Minimal Shape

```yaml
ReleaseGate[flowchart]:
  - Draft[process]
  - Review[decision]
  - Draft --> Review: "submit"
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
