# CoDi C4 Component Properties

## Diagram Properties

| Name | Type | Meaning |
|---|---|---|
| `direction` | TB | LR | RL | BT | Preferred graph direction. |
| `rank_gap` | non-negative number | Space between graph ranks. |
| `node_gap` | non-negative number | Space between sibling nodes. |

## Node Properties

| Name | Type | Meaning |
|---|---|---|
| `description` | string | Short description rendered or used by validators. |
| `label` | string | Display label override. |
| `links` | list/object | External links attached to the node. |
| `refs` | list | Source references or related `.codi` files. |
| `children` | list | Components nested inside a container boundary. |
| `technology` | string | Component technology. |
| `tech` | string | Technology alias. |
| `external` | boolean/annotation | Marks element external. |
| `scope` | boolean/annotation | Marks scoped container. |

## Edge Properties

| Name | Type | Meaning |
|---|---|---|
| `label` | string | Human-readable relationship label. |
| `type` | enum | Relationship type. |
| `technology` | string | Technology used by the relationship. |
| `tech` | string | Short alias for `technology`. |
| `protocol` | string | Protocol used by the relationship. |
| `transport` | string | Transport used by the relationship. |
| `links` | list/object | External links attached to the relationship. |

## Property Rules

- Unknown properties may fail validation on strict diagram types.
- Use quoted strings for labels or descriptions containing punctuation, colons, dates, or symbols.
- Prefer explicit booleans (`true`/`false`) for boolean fields.
- Prefer stable ids where the diagram type supports id-like properties.
