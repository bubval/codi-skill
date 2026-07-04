# CoDi Gantt Vocabulary

## Diagram Type

Use top-level annotation:

```yaml
Name[gantt]:
```

## Valid Node Types

- `task`
- `milestone`
- `group`
- `lane`
- `resource`

## Valid Edge Types

- `finish-start`
- `start-start`
- `finish-finish`
- `start-finish`

## Vocabulary Guidance

Use the vocabulary above exactly unless this document says the type is open/permissive. When the validator is strict for this type, unknown node or edge types can fail validation. Type names are dash-case; property keys are snake_case.
