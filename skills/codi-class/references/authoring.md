# CoDi Class Authoring Guide

## Purpose

UML class, interface, enum, and package diagrams, including scanner-generated code structure.

## Choose This Type When

- You need static object/code structure with classes, interfaces, enums, packages, members, and relationships.
- You need association details such as roles, multiplicity, navigability, composition, or aggregation.
- You want to visualize scanner-generated model relationships.

## Prefer Another Type When

- You need C4 code-level architecture inside a component; use codi-c4-code.
- You need call order; use sequence.

## Minimal Shape

```yaml
Domain[class]:
  - Order[class]:
      - "+ id: UUID"
  - PaymentPort[interface]:
      - "+ charge(order: Order): void"
  - Order --> PaymentPort:
      type: dependency
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
