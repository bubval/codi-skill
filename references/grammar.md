# Diagram Grammar

CoDi diagram source is YAML plus a small semantic layer. The parser does not
define a separate text grammar for indentation, strings, comments, maps, or
lists. YAML owns those rules. CoDi interprets the YAML tree into a `Diagram`
with a name, diagram type, diagram properties, nodes, edges, source references,
links, members, and nested children.

## Document Shape

A diagram file must parse as one YAML mapping with exactly one top-level key.

```yaml
DiagramName[diagram-type]:
  - Item
  - AnotherItem
```

Rules:

- The top-level YAML value must be a mapping.
- The mapping must contain exactly one key.
- The top-level key must be a string.
- The top-level key must have a bracket annotation.
- The top-level value must be a YAML sequence.

Valid:

```yaml
Login[sequence]:
  - Browser[actor]
  - API[service]
  - Browser --> API: "POST /login"
```

Invalid:

```yaml
Login:
  - Browser[actor]
```

The invalid example has no top-level `[type]` annotation.

Invalid:

```yaml
One[sequence]:
  - A[actor]
Two[sequence]:
  - B[actor]
```

The parser expects exactly one top-level diagram per file.

## Bracket Annotations

Bracket annotations are parsed with this shape:

```text
Name[type]
Name[type, annotation, annotation]
```

The first segment inside the brackets is always the type. Remaining segments are
annotations.

Examples:

```yaml
Checkout[c4-component]:
  - WebApp[container, scope]: "Checkout web application"
  - Payments[external-software-system, external]: "Payment provider"
```

Parsed node fields:

| Source | Name | Node type | Annotations |
|---|---|---|---|
| `WebApp[container, scope]` | `WebApp` | `container` | `scope` |
| `Payments[external-software-system, external]` | `Payments` | `external-software-system` | `external` |

Annotations are type-specific: `scope` marks the C4 element in scope for its
level (a `software-system` in c4-container, a `container` in c4-component),
and `external` marks external elements.

Invalid bracket annotations:

```text
[system]
Customer[]
Customer[system,]
Customer[, external]
```

The name, type, and each comma-separated segment must be non-empty after
trimming whitespace.

Node and edge **type names** are dash-case (`trust-boundary`, `composite-state`,
`external-software-system`). Property **keys** are snake_case (`flow_id`,
`entry_action`, `source_role`). Do not mix the two conventions.

## Diagram Types

The diagram type is the bracket annotation on the top-level key:

```yaml
Platform[c4-context]:
  - Customer[person]
```

The parser accepts the string, but the CLI only has default validators for the
built-in types listed in [diagram-types.md](./diagram-types.md). Unknown diagram
types require `--type-path <file.py>` for custom expansion, validation, and
layout.

## Property Buckets

Every property on a diagram, node, or edge belongs to exactly one of three
buckets:

| Bucket | How written | Contents |
|---|---|---|
| **layout** | `layout:` sub-map | `direction`, `rank_gap`, `node_gap`, `lane_gap`, `edge_gap`, `algorithm`, `width`, `height` |
| **style** | `style:` sub-map | `fill`, `stroke`, `stroke_width`, `text`, `muted_text`, `opacity`, `dash`, `line`, `shape` |
| **semantic** | bare top-level keys | everything domain-specific: `technology`, `protocol`, `guard`, `start`, `members`, `threats`, … |

Only `layout` and `style` are nested. Semantic properties stay top-level.

```yaml
- QueryApi[container]:
    technology: "Go service"        # semantic — top-level
    layout:
      width: 220                    # layout — nested
    style:
      fill: "#e8f5e9"               # style — nested
      stroke: "#4caf50"
```

### Layout keys

`layout:` is valid on the diagram root and on nodes. Its keys split into two
classes:

- **container-layout** — `direction`, `rank_gap`, `node_gap`, `lane_gap`,
  `edge_gap`, `algorithm`. These arrange a node's *children*. On a leaf node
  they trigger a warning because there is nothing to arrange.
- **self-layout** — `width`, `height`. These size the node itself and are valid
  on any node, leaf included.

Not every type reads every key: `lane_gap`/`edge_gap` are activity-only,
`algorithm` is unstructured-only. `gantt` and `sequence` are time-based and
have **no** `layout:` keys at all. Edges never take `layout:`.

### Style keys

`style:` is valid on any node and any edge (not on the diagram root — use the
`theme:` directive for global appearance). Canonical key names only:

| Key | Meaning |
|---|---|
| `fill` | Fill color |
| `stroke` | Stroke/border color |
| `stroke_width` | Stroke width |
| `text` | Text color |
| `muted_text` | Secondary text color |
| `opacity` | Opacity 0..1 |
| `line` | Line treatment: `solid`, `dashed`, or `dashed-border` |
| `dash` | Custom dash pattern, e.g. `[8, 5]` |
| `shape` | Renderer shape override where supported (e.g. unstructured) |

There are **no aliases**. `color`, `border`, `border_color`, `border_width`,
`text_color`, and the old bare `style: dashed` scalar are not accepted.
`style:` is exclusively a map; the dashed shorthand is now the `line` key
inside it.

### Block form only

`layout:` and `style:` maps must be written in YAML block form. Inline flow
maps are not supported and the language server warns on them:

```yaml
- layout:                     # block form — the only supported form
    direction: TB

- layout: { direction: TB }   # flow form — NOT supported
```

## Node Bodies

A node's value can be a scalar, a mapping, or a list.

### Bare Node Item

```yaml
- Browser[actor]
```

Creates a node with:

- `name`: `Browser`
- `node_type`: `actor`
- `annotations`: `[]`
- no description
- no custom properties

### Node With Description

```yaml
- Browser[actor]: "Runs the user session"
```

A scalar string value becomes `description`.

### Mapping Body — properties only

The mapping body is the canonical form for **leaf** nodes: properties, no
children.

```yaml
- API[container]:
    description: "Public API"
    technology: "Rust"
    style:
      fill: "#dbeafe"
    links:
      docs: "https://example.test/api"
```

Reserved node property keys:

| Key | Meaning |
|---|---|
| `description` | Node description string |
| `label` | Display label override |
| `layout` | Layout sub-map (see Property Buckets) |
| `style` | Style sub-map (see Property Buckets) |
| `regions` | State-machine orthogonal regions map |
| `members` | Class-like member strings |
| `refs` | Node references, usually scanner or source references |
| `links` | External links attached to the node |

Other properties are preserved as node props and interpreted by validators,
layout, or rendering according to diagram type.

### List Body — property items plus children

The list body is the canonical form for **containers** (and it is exactly how
the diagram root works). Children are plain list items; there is no `children:`
keyword. Properties are written as single-key list items, one key per item:

```yaml
- Analytics[system-boundary]:
    - label: "SaaS Analytics Platform"     # property item
    - layout:                              # property item (block map)
        direction: TB
    - style:
        fill: "#f8fafc"
    - Dashboard[container]:                # child node (leaf: mapping body)
        technology: "React SPA"
    - Api[container]                       # child node
    - Dashboard --> Api: "calls"           # child edge
```

Each list item is classified in this order:

1. **Property item** — a single-key mapping whose key is a reserved or
   type-semantic property (`layout`, `style`, `label`, `description`,
   `members`, `regions`, `provider`, …) → applied to the owning node.
2. **Edge item** — matches arrow syntax → edge.
3. **Node item** — matches `Name[type]` → child node.
4. **Member string** — a plain string, in a class-like type → member line.

This is required by YAML itself: a mapping key and a sequence item cannot
coexist at the same indentation level, so a node with both properties and
children must use the list body with property items.

The `children:` keyword from older CoDi versions is **removed**: not accepted,
not emitted, not documented. Children are simply the node/edge items in the
body list.

### Members (class-like nodes)

Member strings never look like `Name[type]` or arrow items, so a plain string
list under a `class`, `interface`, or `enum` is a member list:

```yaml
- User[class]:
    - "+id: UUID"
    - "+email: String"
```

The explicit `members:` key also works, and is the right choice when the node
carries other properties in a mapping body:

```yaml
- User[class]:
    members:
      - "+id: UUID"
      - "+changeEmail(email: String): void"
    style:
      stroke: "#64748b"
```

Member strings and `Name[type]` children can coexist in one list body — string
items become members, bracketed items become nested types.

### Edge Item

```yaml
- Browser --> API: "POST /login"
```

Creates an edge from `Browser` to `API` with label `POST /login`.

### Edge With Properties

```yaml
- Browser --> API:
    label: "POST /login"
    protocol: "HTTPS"
    type: "calls"
    style:
      stroke: "#94a3b8"
      line: dashed
```

Reserved edge property keys:

| Key | Meaning |
|---|---|
| `label` | Edge label string |
| `style` | Style sub-map (stroke, stroke_width, dash, line, opacity) |
| `links` | External links attached to the edge |

Other properties (`type`, `protocol`, `guard`, `trigger`, `port`, …) are
semantic and stay top-level. Edges never take `layout:`.

### Untyped Mapping Item

If a mapping key is not a bracket node, arrow edge, sequence directive, or
reserved key, the parser creates an untyped node.

```yaml
- ManualStep: "No bracket type"
```

This may be accepted by permissive types such as `flowchart` and
`unstructured`, but typed validators usually reject it.

## Arrow Grammar

CoDi recognizes three generic arrows:

| Source | Parsed endpoints | Direction |
|---|---|---|
| `A --> B` | from `A`, to `B` | forward |
| `A <-- B` | from `B`, to `A` | reverse |
| `A <--> B` | from `A`, to `B` | bidirectional |

The `<--` form swaps the endpoints and records reverse direction. Renderers can
use that direction, for example to draw a sequence reply.

Edge labels can be scalar values:

```yaml
- A --> B: "message"
```

or mapping properties:

```yaml
- A --> B:
    label: "message"
    encrypted: true
```

One exception: `gantt` does not use arrow edges at all. Gantt dependencies are
declared with the `depends_on:` property on the dependent task or milestone
(see [diagram-types.md](./diagram-types.md)).

## Sequence Message Grammar

Sequence diagrams support prefixed message forms in addition to generic arrows.

```yaml
- sync Browser -> API: "request"
- call Browser --> API: "request"
- async API --> Worker: "enqueue"
- reply API <-- Worker: "accepted"
- return Browser <-- API: "200 OK"
- create API --> Session: "create"
- destroy API --> Session: "expire"
- delete API --> Session: "remove"
- found --> API: "external event"
- lost API -->: "dropped event"
- self API --> API: "retry"
```

Accepted message sort words:

- `sync`, `call`, `synchronous`, `synchronous-call`
- `async`, `signal`, `asynchronous`, `asynchronous-call`
- `reply`, `return`, `response`
- `create`, `creation`
- `destroy`, `delete`, `deletion`
- `found`
- `lost`
- `self`, `self-call`

The authored shorthand words are normalized into `sequence_message_sort`
properties on the parsed edge.

## Sequence Directives

Sequence directives are parsed as special `sequence-event` nodes. They preserve
ordering by storing sequence order metadata during parse.

Lifecycle directives:

```yaml
- activate API
- deactivate API
- destroy Session
```

Notes:

```yaml
- note over API: "Validates token"
- note left of Browser: "User starts here"
- note right of Worker: "Async processing"
```

Fragments:

```yaml
- alt valid credentials
- else invalid credentials
- opt remember device
- loop each item
- par parallel branch
- break failure
- critical payment section
- neg forbidden path
- assert invariant
- strict ordered calls
- seq weak sequencing
- ignore noisy messages
- consider selected messages
- ref shared flow
```

The fragment operator is stored as the sequence target; any remaining text is
stored as the guard. Fragments nest their messages implicitly as indented list
items.

## Nested Children

Container nodes hold nested children as plain list items in their body:

```yaml
- CheckoutSystem[system-boundary]:
    - WebApp[container]: "Customer UI"
    - API[container]: "Backend API"
    - WebApp --> API: "HTTPS"
```

The parser recursively parses the nested list. Edges are collected into the
diagram edge list, while child nodes are attached to the parent node. A node is
a container when its type is a declared container type for the diagram
(boundaries, packages, swimlanes, groups, composite states, trust boundaries,
clusters, …) or when it has children.

## State-Machine Regions

State machines keep the explicit `regions` key — it is semantic (orthogonal
regions), not generic nesting:

```yaml
- Processing[composite-state]:
    regions:
      Payment:
        - Authorizing[state]
        - Captured[state]
        - Authorizing --> Captured:
            trigger: "capture"
      Fulfillment:
        - Picking[state]
        - Shipped[state]
```

Each region becomes a child node of type `region`. Edges declared inside nested
state-machine scopes receive internal `__scope` metadata so the layout and
normalization code can resolve scoped names. Plain (non-region) composite-state
children nest implicitly like any other container.

## Links

Links can be declared as a mapping:

```yaml
links:
  source: "src/auth.rs:42"
  docs: "https://example.test/auth"
```

or as a list:

```yaml
links:
  - kind: source
    value: "src/auth.rs:42"
  - kind: ticket
    value: "AUTH-401"
    label: "Login hardening"
```

Both forms produce link records with `kind`, `value`, and optional `label`.

## Sources

Top-level `sources` items are parsed into source references:

```yaml
Backlog[gantt]:
  - sources:
      - name: tasks
        file: backlog.xlsx
        sheet: Sprint 3
  - BuildAPI[task]:
      start: 2026-06-10
      duration: 5d
```

Each source reference has:

- `name`
- `file`
- optional `sheet`

## Diagram Directives and Reserved Keys

Certain mapping keys are treated as diagram directives or reserved words, not as
nodes.

Common reserved keys:

- `test`
- `sources`
- `theme`
- `overlay`
- `layout`
- `threats` (threat-model)

`layout` replaces the flat `direction`/`rank_gap`/`node_gap`/`edge_gap`/
`lane_gap` directives from older CoDi versions:

```yaml
Pipeline[flowchart]:
  - layout:
      direction: LR
      rank_gap: 160
```

Gantt-only reserved keys (semantic configuration, not `layout:`):

- `timeline`
- `calendar`
- `dependencies`
- `defaults`
- `markers`
- `sort`
- `critical_path`
- `columns`

Reserved keys that are diagram directives are copied into diagram props. Other
reserved keys are skipped by the generic node parser and consumed later by
validators or type-specific logic. Unknown property items on built-in types
produce warnings.

## YAML Notes

Use quotes for values that contain YAML-sensitive characters:

```yaml
- API --> Worker: "event: order.created"
```

Prefer list form for all diagram declarations. It preserves order and permits
repeated edges between the same pair of nodes.

```yaml
- API --> Worker: "create"
- API --> Worker: "cancel"
```

Do not depend on YAML map duplicate keys. Duplicate mapping keys are not a safe
way to model repeated edges.
