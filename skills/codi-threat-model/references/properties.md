# CoDi Threat Model Properties

Properties belong to one of three buckets: **layout** (nested under `layout:`), **style** (nested under `style:`), and **semantic** (bare top-level keys). `layout:` and `style:` must be written in YAML block form; inline `{ }` maps are not supported. There are no property aliases — one canonical snake_case name per concept.

## Layout Properties (`layout:` map)

| Name | Type | Meaning |
|---|---|---|
| `direction` | TB \| LR \| RL \| BT | Graph direction for child arrangement. |
| `rank_gap` | non-negative number | Space between graph ranks. |
| `node_gap` | non-negative number | Space between sibling nodes. |

Container-layout keys (direction, gaps, algorithm) apply to the diagram root and to container nodes, where they arrange children; on a leaf node they warn. `width`/`height` size the node itself and are valid on any node. Edges never take `layout:`.

## Style Properties (`style:` map)

| Name | Type | Meaning |
|---|---|---|
| `fill` | color string | Fill color. |
| `stroke` | color string | Stroke/border color. |
| `stroke_width` | number | Stroke width. |
| `text` | color string | Text color. |
| `muted_text` | color string | Secondary text color. |
| `opacity` | 0..1 | Opacity. |
| `line` | solid \| dashed \| dashed-border | Line treatment (replaces the old `style:` scalar). |
| `dash` | list[number] | Custom dash pattern, for example `[8, 5]`. |

Edges accept `style:` too, with `stroke`, `stroke_width`, `opacity`, `line`, and `dash`. The diagram root takes no `style:`; use the `theme:` directive for global appearance.

## Semantic Properties

Semantic properties stay top-level next to `layout:`/`style:`.

### Diagram Directives

| Name | Type | Meaning |
|---|---|---|
| `threats` | list | Top-level authored threats targeting elements or flows. |

### Node Properties

| Name | Type | Meaning |
|---|---|---|
| `description` | string | Short description rendered or used by validators. |
| `label` | string | Display label override. |
| `links` | list/object | External links attached to the node. |
| `refs` | list | Source references or related `.codi` files. |
| `threats` | list | Threats scoped to this element. |
| `trust_level` | string | Trust level for external entities. |
| `technology` | string | Technology for processes. |
| `privilege_level` | normal \| elevated | Privilege level for processes. |
| `controls` | list[string] | Security controls. |
| `encrypted` | boolean | Encryption status for data stores. |
| `data_classification` | public \| internal \| confidential \| restricted \| pii \| phi \| pci \| secret | Data sensitivity. |

### Edge Properties

| Name | Type | Meaning |
|---|---|---|
| `label` | string | Data flow label. |
| `type` | data-flow | Explicit data flow type. |
| `encrypted` | boolean | Whether the flow is encrypted. |
| `authenticated` | boolean | Whether the flow is authenticated. |
| `protocol` | string | Protocol used by the data flow. |
| `data` | string | Data carried by the flow. |
| `data_classification` | enum | Sensitivity of data in transit. |
| `flow_id` | string | Stable id for targeting threats (the `id` alias is gone). |
| `threats` | list | Threats scoped to this flow. |
| `bidirectional` | boolean | Whether the flow is bidirectional. |

## Property Rules

- Canonical names only: `color`, `border`, `border_color`, `border_width`, `text_color`, `tech`, and the bare `style:` scalar are gone. Use `fill`, `stroke`, `stroke_width`, `text`, `technology`, and `line:` inside `style:`.
- Unknown properties may fail validation on strict diagram types.
- Use quoted strings for labels or descriptions containing punctuation, colons, dates, or symbols.
- Prefer explicit booleans (`true`/`false`) for boolean fields.
- Prefer stable ids where the diagram type supports id-like properties.
