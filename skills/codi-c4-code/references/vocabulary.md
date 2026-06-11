# CoDi C4 Code Vocabulary

## Diagram Type

Use top-level annotation:

```yaml
Name[c4-code]:
```

## Valid Node Types

- `class`
- `interface`
- `enum`
- `trait`
- `struct`
- `object`
- `function`
- `module`
- `record`
- `database-table`
- `component`
- `container`
- `database`
- `data-store`
- `boundary`
- `component-boundary`
- `package`

## Valid Edge Types

- `uses`
- `depends-on`
- `calls`
- `reads-from`
- `writes-to`
- `sends-to`
- `publishes-to`
- `subscribes-to`
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

Use the vocabulary above exactly unless this document says the type is open/permissive. When the validator is strict for this type, unknown node or edge types can fail validation.
