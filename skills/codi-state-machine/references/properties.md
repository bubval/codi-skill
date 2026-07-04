# CoDi State Machine Properties

Properties belong to one of three buckets: **layout** (nested under `layout:`), **style** (nested under `style:`), and **semantic** (bare top-level keys). `layout:` and `style:` must be written in YAML block form; inline `{ }` maps are not supported. There are no property aliases — one canonical snake_case name per concept.

## Layout Properties (`layout:` map)

| Name | Type | Meaning |
|---|---|---|
| `direction` | TB \| LR \| RL \| BT | Graph direction for child arrangement. |
| `rank_gap` | non-negative number | Space between graph ranks. |
| `node_gap` | non-negative number | Space between sibling nodes. |
| `width` | positive number | Node width in layout units (valid on any node). |
| `height` | positive number | Node height in layout units (valid on any node). |

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

No diagram-specific directives. Shared render targets are CLI flags, not source properties.

### Node Properties

| Name | Type | Meaning |
|---|---|---|
| `label` | string | Display label. |
| `entry_action` | string | Entry behavior. |
| `do_activity` | string | Ongoing state activity. |
| `exit_action` | string | Exit behavior. |
| `internal_transitions` | list | Internal transition objects with trigger/guard/action. |
| `deferred` | list[string] | Deferred events. |
| `regions` | mapping | Composite state orthogonal regions. |
| `type` | shallow \| deep | History pseudostate kind. |

### Edge Properties

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

- Canonical names only: `color`, `border`, `border_color`, `border_width`, `text_color`, `tech`, and the bare `style:` scalar are gone. Use `fill`, `stroke`, `stroke_width`, `text`, `technology`, and `line:` inside `style:`.
- Unknown properties may fail validation on strict diagram types.
- Use quoted strings for labels or descriptions containing punctuation, colons, dates, or symbols.
- Prefer explicit booleans (`true`/`false`) for boolean fields.
- Prefer stable ids where the diagram type supports id-like properties.
