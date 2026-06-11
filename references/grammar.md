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
Checkout[c4-container]:
  - WebApp[container, scope]
  - Payments[external-software-system, external]
```

Parsed node fields:

| Source | Name | Node type | Annotations |
|---|---|---|---|
| `WebApp[container, scope]` | `WebApp` | `container` | `scope` |
| `Payments[external-software-system, external]` | `Payments` | `external-software-system` | `external` |

Invalid bracket annotations:

```text
[system]
Customer[]
Customer[system,]
Customer[, external]
```

The name, type, and each comma-separated segment must be non-empty after
trimming whitespace.

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

## List Items

Every diagram body item is a YAML list item.

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

### Node With Properties

```yaml
- API[container]:
    description: "Public API"
    technology: "Rust"
    links:
      docs: "https://example.test/api"
```

Special node properties:

| Key | Meaning |
|---|---|
| `description` | Node description string |
| `children` | Nested node/edge list |
| `regions` | State-machine regions map |
| `members` | Class-like member strings |
| `refs` | Node references, usually scanner or source references |
| `links` | External links attached to the node |

Other properties are preserved as node props and interpreted by validators,
layout, or rendering according to diagram type.

### Node With Direct Nested Sequence

```yaml
- Core[package]:
    - User[class]
    - Order[class]
```

A sequence value is interpreted as either:

- members, if the items look like member strings, or
- nested children, if the items look like nodes or edges.

For `class`, `interface`, and `enum` nodes, a plain string sequence is a member
list.

```yaml
- User[class]:
    - "+id: UUID"
    - "+email: String"
```

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
```

Special edge properties:

| Key | Meaning |
|---|---|
| `label` | Edge label string |
| `links` | External links attached to the edge |

Other properties are preserved as edge props and interpreted by the diagram type.

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
stored as the guard.

## Nested Children

Container nodes can hold nested child nodes through `children`:

```yaml
- CheckoutSystem[system-boundary]:
    children:
      - WebApp[container]: "Customer UI"
      - API[container]: "Backend API"
      - WebApp --> API: "HTTPS"
```

The parser recursively parses the nested list. Edges are collected into the
diagram edge list, while child nodes are attached to the parent node.

## State-Machine Regions

State machines have special `regions` support:

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
normalization code can resolve scoped names.

## Members

Class-like nodes can use `members`:

```yaml
- User[class]:
    members:
      - "+id: UUID"
      - "+changeEmail(email: String): void"
```

or direct member list syntax:

```yaml
- User[class]:
    - "+id: UUID"
    - "+changeEmail(email: String): void"
```

The parser stores members as strings. The class validator interprets field and
method details.

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
- `direction`
- `rank_gap`
- `node_gap`
- `edge_gap`
- `lane_gap`
- `threats`

Gantt-only reserved keys:

- `timeline`
- `calendar`
- `dependencies`
- `defaults`
- `markers`
- `sort`
- `critical_path`
- `columns`

Unstructured-only reserved key:

- `algorithm`

Reserved keys that are diagram directives are copied into diagram props. Other
reserved keys are skipped by the generic node parser and consumed later by
validators or type-specific logic.

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
