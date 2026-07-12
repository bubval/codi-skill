# CoDi Flowchart Grammar

## Declaration

A minimal valid `flowchart` diagram:

```yaml
ReleaseGate[flowchart]:
  - Draft[process]
  - Review[decision]
  - Draft --> Review: "submit"
```

## Shared CoDi Grammar

All CoDi diagrams are YAML. A file contains exactly one top-level mapping key with a bracketed diagram type. The top-level value is a YAML list. Node types use bracket annotations. Edges use `-->`, `<--`, or `<-->`.

Every property belongs to one of three buckets: `layout:` (nested map), `style:` (nested map), or semantic keys (bare top-level). Property keys are snake_case; node/edge type names are dash-case. `layout:` and `style:` maps are written in YAML block form only — inline `{ }` maps are not supported.

## Type-Specific Notes

- Use readable domain-specific node types, for example `Review[decision]` or `Deploy[process]`.
- Groups nest children as plain list items; group layout and style are property items (`- layout:` block, `- style:` block) in the same list.
- Use labels on decision outgoing edges for branch meaning.

## Nesting: The Uniform Body Rule

There is no `children:` keyword. Every body — the diagram body and any container body — is a YAML list, and each item is one of:

1. A **property item**: a single-key mapping such as `- layout:` (block map), `- style:` (block map), or `- label: "x"`, applied to the owning node.
2. An **edge**: arrow syntax.
3. A **child node**: `Name[type]`.
4. A **member string** (class-like types only).

A leaf node with only properties uses a plain mapping body instead:

```yaml
- Leaf[type]:
    description: "properties only"
    style:
      fill: "#eef2ff"
```

A container with properties AND children uses the list body with property items:

```yaml
- Parent[type]:
    - layout:
        direction: TB
    - style:
        fill: "#f8fafc"
    - ChildA[type]
    - ChildB[type]
    - ChildA --> ChildB
```

## Labels and Properties

A scalar string after a node colon becomes a node description. A scalar string after an edge colon becomes an edge label. Mapping values become structured properties and should be preferred for detailed diagrams.
