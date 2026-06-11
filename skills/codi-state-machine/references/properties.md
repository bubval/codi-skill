# CoDi State Machine Properties

## Diagram Properties

| Name | Type | Meaning |
|---|---|---|
| `direction` | TB | LR | RL | BT | Preferred graph direction. |
| `rank_gap` | non-negative number | Space between graph ranks. |
| `node_gap` | non-negative number | Space between sibling nodes. |

## Node Properties

| Name | Type | Meaning |
|---|---|---|
| `label` | string | Display label. |
| `width` | positive number | Rendered width. |
| `height` | positive number | Rendered height. |
| `entry-action` | string | Entry behavior. |
| `do-activity` | string | Ongoing state activity. |
| `exit-action` | string | Exit behavior. |
| `internal-transitions` | list | Internal transition objects with trigger/guard/action. |
| `deferred` | list[string] | Deferred events. |
| `regions` | mapping | Composite state regions. |
| `children` | list | Nested state children where supported. |
| `type` | shallow | deep | History pseudostate kind. |
| `direction` | TB | LR | RL | BT | Preferred graph direction. |
| `rank_gap` | non-negative number | Space between graph ranks. |
| `node_gap` | non-negative number | Space between sibling nodes. |

## Edge Properties

| Name | Type | Meaning |
|---|---|---|
| `trigger` | string | Event that triggers the transition. |
| `guard` | string | Guard condition. |
| `action` | string | Transition action. |
| `label` | string | Rendered transition label. |
| `event` | string | Alias/semantic event field. |
| `completion` | boolean | Completion transition flag. |
| `type` | transition | Explicit edge type. |

## Property Rules

- Unknown properties may fail validation on strict diagram types.
- Use quoted strings for labels or descriptions containing punctuation, colons, dates, or symbols.
- Prefer explicit booleans (`true`/`false`) for boolean fields.
- Prefer stable ids where the diagram type supports id-like properties.
