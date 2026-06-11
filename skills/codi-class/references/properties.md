# CoDi Class Properties

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
| `members` | list[string] | Class/interface/enum members. |
| `children` | list | Nested package contents. |
| `stereotype` | string | UML stereotype. |
| `stereotypes` | list[string] | Multiple UML stereotypes. |
| `templateParameters` | list | Generic/template parameters. |
| `language` | string | Source language hint. |

## Edge Properties

| Name | Type | Meaning |
|---|---|---|
| `type` | enum | Relationship type. |
| `label` | string | Relationship label. |
| `sourceRole` | string | Association source role. |
| `targetRole` | string | Association target role. |
| `sourceMultiplicity` | string | Source multiplicity. |
| `targetMultiplicity` | string | Target multiplicity. |
| `navigable` | boolean | Whether association is navigable. |
| `links` | list/object | External links attached to the relationship. |

## Property Rules

- Unknown properties may fail validation on strict diagram types.
- Use quoted strings for labels or descriptions containing punctuation, colons, dates, or symbols.
- Prefer explicit booleans (`true`/`false`) for boolean fields.
- Prefer stable ids where the diagram type supports id-like properties.
