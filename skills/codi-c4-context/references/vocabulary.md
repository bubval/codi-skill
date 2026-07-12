# CoDi C4 Context Vocabulary

## Diagram Type

Use top-level annotation:

```yaml
Name[c4-context]:
```

## Valid Node Types

- `person`
- `system`
- `software-system`
- `external-software-system`
- `boundary`
- `system-boundary`
- `enterprise-boundary`

## Valid Edge Types

- `uses`
- `depends-on`
- `calls`
- `reads-from`
- `writes-to`
- `sends-to`
- `publishes-to`
- `subscribes-to`

## Vocabulary Guidance

Use the vocabulary above exactly unless this document says the type is open/permissive. When the validator is strict for this type, unknown node or edge types can fail validation. Type names are dash-case; property keys are snake_case.
