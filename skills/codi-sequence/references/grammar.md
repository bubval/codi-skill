# CoDi Sequence Grammar

## Declaration

```yaml
DiagramName[sequence]:
  - NodeName[type]
  - NodeName --> OtherNode: "relationship label"
```

## Shared CoDi Grammar

All CoDi diagrams are YAML. A file contains exactly one top-level mapping key with a bracketed diagram type. The top-level value is a YAML list. Node types use bracket annotations. Edges use `-->`, `<--`, or `<-->`.

## Type-Specific Notes

- Declare lifelines before messages where possible.
- Generic arrows are supported: `A --> B`, `A <-- B`, and `A <--> B`.
- Sequence directives include `sync`, `call`, `async`, `reply`, `create`, `destroy`, `found`, `lost`, and `self`.
- Lifecycle directives include `activate X`, `deactivate X`, and `destroy X`.
- Notes use `note over X`, `note left of X`, or `note right of X`.
- Fragments use `alt`, `else`, `opt`, `loop`, `par`, and `ref` list items.

## Nesting

Use `children:` for nested structures when this diagram type supports containers, boundaries, packages, regions, lanes, groups, or swimlanes. Direct nested YAML sequences are accepted for some class-like/member patterns when examples show that form.

## Labels and Properties

A scalar string after a node colon becomes a node description. A scalar string after an edge colon becomes an edge label. Mapping values become structured properties and should be preferred for detailed diagrams.
