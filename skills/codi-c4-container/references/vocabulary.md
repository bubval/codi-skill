# CoDi C4 Container Vocabulary

## Diagram Type

Use top-level annotation:

```yaml
Name[c4-container]:
```

## Valid Node Types

- `container`
- `database`
- `data-store`
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

Use the vocabulary above exactly unless this document says the type is open/permissive. When the validator is strict for this type, unknown node or edge types can fail validation.
