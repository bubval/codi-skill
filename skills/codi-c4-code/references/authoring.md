# CoDi C4 Code Authoring Guide

## Purpose

C4 code-level diagrams showing classes, interfaces, functions, modules, and packages inside one component.

## Choose This Type When

- You need code-level architecture inside one component.
- You want C4 context plus class-like structure and structural relationship validation.

## Prefer Another Type When

- You only need pure UML/domain classes; use codi-class.
- You need component-level architecture; use codi-c4-component.

## Minimal Shape

```yaml
PaymentModule[c4-code]:
  - PaymentComponent[component, scope]: "Payments component"
  - PaymentService[class]:
      - "+ authorize(request: PaymentRequest): PaymentResult"
  - PaymentPort[interface]:
      - "+ authorize(request: PaymentRequest): PaymentResult"
  - PaymentService --> PaymentPort:
      type: implements
      label: "implements port"
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
