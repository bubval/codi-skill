# CoDi Threat Model Vocabulary

## Diagram Type

Use top-level annotation:

```yaml
Name[threat-model]:
```

## Valid Node Types

- `trust-boundary`
- `process`
- `data-store`
- `external-entity`

## Valid Edge Types

- `data-flow`

## Vocabulary Guidance

Use the vocabulary above exactly unless this document says the type is open/permissive. When the validator is strict for this type, unknown node or edge types can fail validation.
