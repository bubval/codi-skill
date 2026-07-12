# CoDi Gantt Properties

Properties belong to one of three buckets: **layout** (nested under `layout:`), **style** (nested under `style:`), and **semantic** (bare top-level keys). `layout:` and `style:` must be written in YAML block form; inline `{ }` maps are not supported. There are no property aliases — one canonical snake_case name per concept.

## Layout Properties (`layout:` map)

This type is time-based: it has **no** `layout:` keys. Do not add `direction`, `rank_gap`, or `node_gap` to this diagram type.

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
| `timeline` | object | Timeline configuration: scale, today. |
| `calendar` | object | Calendar configuration: timezone, work_week, holidays. |
| `markers` | list | Timeline markers with date/label/name/color. |
| `dependencies` | object | Dependency display configuration. |
| `critical_path` | boolean/enum | Critical path display mode. |

### Node Properties

| Name | Type | Meaning |
|---|---|---|
| `start` | date/datetime | Task/group/lane start. |
| `end` | date/datetime | Task/group/lane end. |
| `duration` | duration | Task duration. |
| `date` | date/datetime | Milestone date. |
| `progress` | 0..1, 0..100, or percent | Task progress. |
| `resource` | string | Assigned resource. |
| `depends_on` | list | Dependencies of this task/milestone (see Dependency Properties). |
| `baseline_start` | date/datetime | Baseline start. |
| `baseline_end` | date/datetime | Baseline end. |
| `actual_start` | date/datetime | Actual start. |
| `actual_end` | date/datetime | Actual end. |
| `deadline` | date/datetime | Deadline marker. |
| `critical` | boolean | Marks critical work. |
| `capacity` | number | Resource capacity. |

### Dependency Properties (`depends_on:` entries)

| Name | Type | Meaning |
|---|---|---|
| `task` | node-ref | Predecessor task/milestone name (required in the mapping form). |
| `type` | finish-start \| start-start \| finish-finish \| start-finish | Dependency type; defaults to finish-start. |
| `lag` | duration | Dependency lag. |
| `lead` | duration | Dependency lead. |

## Property Rules

- Canonical names only: `color`, `border`, `border_color`, `border_width`, `text_color`, `tech`, and the bare `style:` scalar are gone. Use `fill`, `stroke`, `stroke_width`, `text`, `technology`, and `line:` inside `style:`.
- Unknown properties may fail validation on strict diagram types.
- Use quoted strings for labels or descriptions containing punctuation, colons, dates, or symbols.
- Prefer explicit booleans (`true`/`false`) for boolean fields.
- Prefer stable ids where the diagram type supports id-like properties.
