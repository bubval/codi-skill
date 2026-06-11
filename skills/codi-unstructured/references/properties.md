# CoDi Unstructured Properties

## Diagram Properties

| Name | Type | Meaning |
|---|---|---|
| `algorithm` | organic | force | force-directed | fdg | Layout algorithm. |
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
| `shape` | string | Renderer shape override where supported. |
| `width` | positive number | Node width in layout units. |
| `height` | positive number | Node height in layout units. |
| `fill` | color string | Node fill color. |
| `stroke` | color string | Node stroke color. |
| `border` | color string | Border color alias. |
| `text` | color string | Text color. |
| `border_width` | number | Border width. |
| `stroke_width` | number | Stroke width. |
| `algorithm` | organic | force | Nested layout algorithm. |
| `direction` | TB | LR | RL | BT | Nested layout direction. |
| `children` | list | Nested child nodes and edges. |
| `icon` | string | Renderer icon name. |
| `style` | string | Visual style such as dashed. |
| `opacity` | number | Node opacity. |

## Edge Properties

| Name | Type | Meaning |
|---|---|---|
| `label` | string | Relationship label. |
| `style` | string | Edge style such as dashed. |
| `stroke` | color string | Edge color. |
| `stroke_width` | number | Edge width. |
| `dash` | list[number] | Custom dash pattern. |
| `opacity` | number | Edge opacity. |
| `links` | list/object | External links attached to the edge. |

## Property Rules

- Unknown properties may fail validation on strict diagram types.
- Use quoted strings for labels or descriptions containing punctuation, colons, dates, or symbols.
- Prefer explicit booleans (`true`/`false`) for boolean fields.
- Prefer stable ids where the diagram type supports id-like properties.
