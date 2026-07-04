# CoDi State Machine Authoring Guide

## Purpose

UML-style state machines with states, transitions, composite states, regions, history, and pseudostates.

## Choose This Type When

- You need lifecycle/state behavior rather than process steps.
- Events, guards, actions, entry/do/exit behavior, and composite states matter.
- You need validation of pseudostate and transition rules.

## Prefer Another Type When

- You need ordered interactions between participants; use sequence.
- You need business process flow; use activity or flowchart.

## Minimal Shape

```yaml
OrderState[state-machine]:
  - initial --> Created
  - Created[state]
  - Created --> final:
      trigger: "archived"
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
