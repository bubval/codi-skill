# CoDi Unstructured Authoring Guide

## Purpose

Permissive freeform diagrams, concept maps, dependency webs, ownership maps, and quick sketches.

## Choose This Type When

- You need readable topology but not a strict semantic model.
- Node types are domain-specific or experimental.
- You want rich visual styling and nested groups without strict validation.

## Prefer Another Type When

- You need C4, UML, STRIDE, or Gantt-specific validation.
- A strict diagram type exists for the domain and should catch mistakes.

## Minimal Shape

```yaml
ServiceMap[unstructured]:
  - API[service]
  - Queue[queue]
  - API --> Queue: "publishes"
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
