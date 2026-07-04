# CoDi Class Vocabulary

## Diagram Type

Use top-level annotation:

```yaml
Name[class]:
```

## Valid Node Types

- `class`
- `interface`
- `enum`
- `package`

## Valid Edge Types

- `association`
- `dependency`
- `inherits`
- `inheritance`
- `extends`
- `implements`
- `realization`
- `composition`
- `aggregation`

## Vocabulary Guidance

Use the vocabulary above exactly unless this document says the type is open/permissive. When the validator is strict for this type, unknown node or edge types can fail validation. Type names are dash-case; property keys are snake_case.
