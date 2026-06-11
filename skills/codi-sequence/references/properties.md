# CoDi Sequence Properties

## Diagram Properties

No diagram-specific properties are required. Shared render targets are CLI flags, not source properties.

## Node Properties

| Name | Type | Meaning |
|---|---|---|
| `description` | string | Short description rendered or used by validators. |
| `label` | string | Display label override. |
| `links` | list/object | External links attached to the node. |
| `refs` | list | Source references or related `.codi` files. |

## Edge Properties

| Name | Type | Meaning |
|---|---|---|
| `label` | string | Message text. |
| `type` | enum | Message sort, commonly inferred from directive syntax. |

## Property Rules

- Unknown properties may fail validation on strict diagram types.
- Use quoted strings for labels or descriptions containing punctuation, colons, dates, or symbols.
- Prefer explicit booleans (`true`/`false`) for boolean fields.
- Prefer stable ids where the diagram type supports id-like properties.
