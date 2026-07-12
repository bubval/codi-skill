# CoDi C4 Context Authoring Guide

## Purpose

C4 system context diagrams showing one software system in scope, its users, and external systems.

## Choose This Type When

- You need a high-level system context for humans and neighboring systems.
- You want to communicate boundaries and external dependencies before container/component detail.
- You need C4 validation for context-level vocabulary.

## Prefer Another Type When

- You need deployable/runtime internals; use codi-c4-container.
- You need code/class internals; use codi-c4-code or codi-class.

## Minimal Shape

```yaml
Platform[c4-context]:
  - Customer[person]: "Uses the platform"
  - PlatformSystem[software-system]:
      scope: true
      description: "System in scope"
  - Payments[external-software-system]: "Payment provider"
  - Customer --> PlatformSystem: "Places orders"
  - PlatformSystem --> Payments: "Charges cards"
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
