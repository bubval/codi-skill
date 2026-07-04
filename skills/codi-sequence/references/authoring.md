# CoDi Sequence Authoring Guide

## Purpose

Ordered interactions over time between actors, services, systems, databases, and objects.

## Choose This Type When

- Explaining request/response flows, login flows, async work, callbacks, retries, or lifecycle behavior.
- Source order matters and messages should appear vertically in time order.
- You need sequence-specific constructs such as activation, replies, notes, and fragments.

## Prefer Another Type When

- The goal is static system topology; use C4 or unstructured instead.
- The goal is a generic process with decisions and parallel branches; use activity or flowchart.

## Minimal Shape

```yaml
Login[sequence]:
  - Browser[actor]
  - API[service]
  - sync Browser -> API: "POST /login"
  - reply Browser <-- API: "200 OK"
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
