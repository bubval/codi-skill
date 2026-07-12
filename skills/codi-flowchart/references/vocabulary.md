# CoDi Flowchart Vocabulary

## Diagram Type

Use top-level annotation:

```yaml
Name[flowchart]:
```

## Valid Node Types

- `open vocabulary; common: start, terminal, process, decision, group, note, category, examples, container`

## Valid Edge Types

- `generic directed edges via `-->`, `<--`, `<-->``

## Vocabulary Guidance

Use the vocabulary above exactly unless this document says the type is open/permissive. When the validator is strict for this type, unknown node or edge types can fail validation. Type names are dash-case; property keys are snake_case.
