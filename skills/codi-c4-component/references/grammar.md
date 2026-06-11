# CoDi C4 Component Grammar

## Declaration

```yaml
DiagramName[c4-component]:
  - NodeName[type]
  - NodeName --> OtherNode: "relationship label"
```

## Shared CoDi Grammar

All CoDi diagrams are YAML. A file contains exactly one top-level mapping key with a bracketed diagram type. The top-level value is a YAML list. Node types use bracket annotations. Edges use `-->`, `<--`, or `<-->`.

## Type-Specific Notes

- Mark the scoped container and nest components in a `container-boundary`.
- Keep supporting systems and containers outside the scoped boundary unless they are the scoped container.

## Nesting

Use `children:` for nested structures when this diagram type supports containers, boundaries, packages, regions, lanes, groups, or swimlanes. Direct nested YAML sequences are accepted for some class-like/member patterns when examples show that form.

## Labels and Properties

A scalar string after a node colon becomes a node description. A scalar string after an edge colon becomes an edge label. Mapping values become structured properties and should be preferred for detailed diagrams.
