# CoDi Activity Vocabulary

## Diagram Type

Use top-level annotation:

```yaml
Name[activity]:
```

## Valid Node Types

- `action`
- `call-action`
- `call-operation-action`
- `call-behavior-action`
- `accept-event-action`
- `send-signal-action`
- `object`
- `object-node`
- `input-pin`
- `output-pin`
- `value-pin`
- `data-store`
- `central-buffer`
- `initial`
- `initial-node`
- `final`
- `activity-final`
- `activity-final-node`
- `flow-final`
- `flow-final-node`
- `decision`
- `decision-node`
- `merge`
- `merge-node`
- `fork`
- `fork-node`
- `join`
- `join-node`
- `swimlane`
- `partition`
- `activity-partition`
- `interruptible-region`
- `expansion-region`
- `expansion-node`

## Valid Edge Types

- `control-flow`
- `object-flow`
- `interrupting-edge`

## Vocabulary Guidance

Use the vocabulary above exactly unless this document says the type is open/permissive. When the validator is strict for this type, unknown node or edge types can fail validation. Type names are dash-case; property keys are snake_case.
