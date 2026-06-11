# CoDi C4 Container Authoring Guide

## Purpose

C4 container diagrams showing deployable/runtime containers inside one software system.

## Choose This Type When

- You need services, apps, databases, queues, or deployable units inside a scoped system.
- You need neighboring users/systems around those containers.

## Prefer Another Type When

- You only need system context; use codi-c4-context.
- You need internals of one container; use codi-c4-component.

## Minimal Shape

```yaml
Example[c4-container]:
  - FirstNode[container]
```

## Production Pattern

- Declare important nodes before edges.
- Use stable names because CoDi identity is name-based.
- Add labels on relationships where the validator or reader benefits from intent.
- Prefer structured properties over overloaded labels when a property exists.
- Keep examples valid by running `codi validate`.
- Use `codi help render` before assuming installed render flags.

## Common Mistakes

- Referencing an undeclared edge endpoint.
- Mixing a diagram type's vocabulary with a lower-level or unrelated diagram type.
- Using a render target as source syntax. Render size belongs on the CLI, not in `.codi`.
- Relying on stale command flags instead of `codi help <command>`.
