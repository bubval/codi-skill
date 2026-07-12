# CoDi Threat Model Authoring Guide

## Purpose

STRIDE-compatible data-flow diagrams with trust boundaries, data stores, processes, external entities, and authored threats.

## Choose This Type When

- You need a security data-flow diagram.
- You need trust boundary crossing checks, encryption checks, and authored STRIDE threats.
- You need threat status, severity, mitigations, and data classification.

## Prefer Another Type When

- You need general architecture without security-specific semantics; use C4 or unstructured.

## Minimal Shape

```yaml
UploadModel[threat-model]:
  - User[external-entity]: "Uploads content"
  - AppTier[trust-boundary]:
      - UploadAPI[process]: "Accepts upload requests"
  - User --> UploadAPI:
      label: "HTTPS upload"
      protocol: HTTPS
      encrypted: true
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
