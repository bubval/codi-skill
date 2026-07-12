# CoDi State Machine Vocabulary

## Diagram Type

Use top-level annotation:

```yaml
Name[state-machine]:
```

## Valid Node Types

- `state`
- `composite-state`
- `region`
- `initial`
- `final`
- `choice`
- `junction`
- `fork`
- `join`
- `entry-point`
- `exit-point`
- `terminate`
- `history`

## Valid Edge Types

- `transition`

## Vocabulary Guidance

Use the vocabulary above exactly unless this document says the type is open/permissive. When the validator is strict for this type, unknown node or edge types can fail validation. Type names are dash-case; property keys are snake_case.
