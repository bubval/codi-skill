# CoDi C4 Component Vocabulary

## Diagram Type

Use top-level annotation:

```yaml
Name[c4-component]:
```

## Valid Node Types

- `component`
- `person`
- `system`
- `software-system`
- `external-software-system`
- `container`
- `database`
- `data-store`
- `boundary`
- `container-boundary`

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
