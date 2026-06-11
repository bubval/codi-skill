# Diagram Type Reference

All diagram types use the same parser grammar from [grammar.md](./grammar.md).
Each type defines a vocabulary, validation rules, layout behavior, and rendering
conventions.

## Sequence

Declaration:

```yaml
Login[sequence]:
  - Browser[actor]
  - API[service]
```

Purpose: ordered interactions over time.

Lifeline node types:

- `actor`
- `participant`
- `lifeline`
- `service`
- `server`
- `database`
- `component`
- `object`
- `system`

Message grammar:

```yaml
- Browser --> API: "request"
- API <-- Browser: "response"
- sync Browser -> API: "synchronous call"
- async API --> Worker: "queue job"
- reply Browser <-- API: "200 OK"
- create API --> Session: "new session"
- destroy API --> Session: "expire"
- found --> API: "external event"
- lost API -->: "dropped event"
- self API --> API: "retry"
```

Lifecycle and notes:

```yaml
- activate API
- deactivate API
- destroy Session
- note over API: "Token validation"
- note left of Browser: "Starts flow"
- note right of Worker: "Async branch"
```

Fragments:

```yaml
- alt valid credentials
- else invalid credentials
- opt remember device
- loop each retry
- par background work
- ref shared authorization flow
```

Validation focuses on lifeline vocabulary, message endpoints, message sorts,
fragment directives, notes, and lifecycle consistency. Layout places lifelines
horizontally and events/messages vertically in source order.

Examples:

- [sequence-auth-login.codi](./examples/sequence-auth-login.codi) and [SVG](./examples/sequence-auth-login.svg)
- [sequence-lifecycle-fragments.codi](./examples/sequence-lifecycle-fragments.codi) and [SVG](./examples/sequence-lifecycle-fragments.svg)
- [sequence-notes-replies.codi](./examples/sequence-notes-replies.codi) and [SVG](./examples/sequence-notes-replies.svg)

## Unstructured

Declaration:

```yaml
ServiceMap[unstructured]:
  - API[service]
  - Queue[queue]
  - API --> Queue: "publishes"
```

Purpose: permissive freeform diagrams, concept maps, ownership maps, dependency
webs, and quick sketches.

Node vocabulary is intentionally open. Unknown node types are accepted. Common
rendering properties:

```yaml
- API[service]:
    label: "Public API"
    shape: rect
    icon: server
    width: 220
    height: 90
    fill: "#f5f7ff"
    stroke: "#4f46e5"
    text: "#111827"
    style: dashed
```

Diagram and nested layout properties:

```yaml
- algorithm: organic
- direction: LR
- rank_gap: 160
- node_gap: 60
```

Edge properties:

```yaml
- API --> Queue:
    label: "events"
    style: dashed
    stroke: "#6b7280"
    stroke_width: 2
```

Validation warns about unsupported or malformed renderer-relevant options, such
as invalid `algorithm`, invalid `direction`, negative numeric values, and old
grouping props. Layout uses organic/force-style behavior unless direction and
nesting make a structured layout more appropriate.

Examples:

- [unstructured-service-map.codi](./examples/unstructured-service-map.codi) and [SVG](./examples/unstructured-service-map.svg)
- [unstructured-incident-map.codi](./examples/unstructured-incident-map.codi) and [SVG](./examples/unstructured-incident-map.svg)
- [unstructured-dependency-web.codi](./examples/unstructured-dependency-web.codi) and [SVG](./examples/unstructured-dependency-web.svg)

## Flowchart

Declaration:

```yaml
ReleaseGate[flowchart]:
  - Draft[process]
  - Review[decision]
  - Draft --> Review: "submit"
```

Purpose: generic directed process flows.

Flowchart accepts arbitrary node type annotations so authors can use readable
domain-specific node kinds:

```yaml
- Start[terminal]
- Validate[process]
- Approved[decision]
- Publish[process]
```

Layout properties:

```yaml
- direction: LR
- rank_gap: 180
- node_gap: 48
```

Nested flowchart nodes:

```yaml
- Fulfillment[group]:
    direction: TB
    children:
      - ReserveInventory[process]
      - PackOrder[process]
      - ReserveInventory --> PackOrder: "reserved"
```

Validation checks direction values, duplicate node names, duplicate edges,
numeric layout props, and layout-only nodes. Layout is directed and
container-aware.

Examples:

- [flowchart-release-gate.codi](./examples/flowchart-release-gate.codi) and [SVG](./examples/flowchart-release-gate.svg)
- [flowchart-error-handling.codi](./examples/flowchart-error-handling.codi) and [SVG](./examples/flowchart-error-handling.svg)
- [flowchart-nested-process.codi](./examples/flowchart-nested-process.codi) and [SVG](./examples/flowchart-nested-process.svg)

## Activity

Declaration:

```yaml
Approval[activity]:
  - Start[initial]
  - Review[action]
  - Approved[decision]
  - Start --> Review
```

Purpose: UML-style activity flows, object flows, control flow, partitions, and
regions.

Canonical node families:

- action nodes: actions, calls, accept/send signal variants
- object nodes: object nodes, pins, data stores, central buffers
- control nodes: initial, final, flow-final, decision, merge, fork, join
- containers: activity partitions/swimlanes, interruptible regions, expansion regions

Common grammar:

```yaml
- Intake[swimlane]:
    children:
      - ReceiveForm[action]
      - ValidateForm[action]
- Start[initial]
- Done[activity-final]
- Form[object]
- Start --> ReceiveForm:
    type: control-flow
- ReceiveForm --> Form:
    type: object-flow
```

Implicit endpoint names such as `initial`, `final`, and common aliases are
recognized by the validator. Activity flows can use `type: control-flow` or
`type: object-flow`.

Validation checks node vocabulary, endpoint references, invalid object/control
flow combinations, partition membership, pins, regions, and common UML activity
constraints. Layout renders action/control/object nodes and swimlane-style
grouping.

Examples:

- [activity-approval-workflow.codi](./examples/activity-approval-workflow.codi) and [SVG](./examples/activity-approval-workflow.svg)
- [activity-object-flow.codi](./examples/activity-object-flow.codi) and [SVG](./examples/activity-object-flow.svg)
- [activity-swimlane-handoff.codi](./examples/activity-swimlane-handoff.codi) and [SVG](./examples/activity-swimlane-handoff.svg)

## State Machine

Declaration:

```yaml
OrderState[state-machine]:
  - Created[state]
  - Paid[state]
  - Created --> Paid:
      trigger: "paymentCaptured"
```

Purpose: UML-style state machines.

Node types include:

- `state`
- `composite-state`
- `region`
- pseudostates such as initial, final, choice, junction, fork, join, entry-point,
  exit-point, terminate, shallow/deep history variants

Transition properties:

```yaml
- Created --> Paid:
    trigger: "paymentCaptured"
    guard: "amount > 0"
    action: "recordPayment"
```

State behavior:

```yaml
- Paid[state]:
    entry-action: "sendReceipt"
    do-activity: "waitForFulfillment"
    exit-action: "closeInvoice"
    internal-transitions:
      - event: "refundRequested"
        action: "openRefundCase"
    deferred:
      - "shipmentUpdated"
```

Composite states and regions:

```yaml
- Processing[composite-state]:
    regions:
      Payment:
        - Authorizing[state]
        - Captured[state]
      Fulfillment:
        - Picking[state]
        - Shipped[state]
```

Validation checks state vocabulary, transition endpoints, transition properties,
diagram props, composite/region structure, history kinds, and scoped names.
Layout uses directed state graph layout and supports nested/composite rendering.

Examples:

- [state-machine-order.codi](./examples/state-machine-order.codi) and [SVG](./examples/state-machine-order.svg)
- [state-machine-composite.codi](./examples/state-machine-composite.codi) and [SVG](./examples/state-machine-composite.svg)
- [state-machine-regions.codi](./examples/state-machine-regions.codi) and [SVG](./examples/state-machine-regions.svg)

## Class

Declaration:

```yaml
Domain[class]:
  - Order[class]
  - PaymentPort[interface]
  - Order --> PaymentPort:
      type: dependency
```

Purpose: UML class diagrams and scanner-generated code structure.

Node types:

- `class`
- `interface`
- `enum`
- `package`
- related class-like aliases handled by the renderer and validator

Members:

```yaml
- Order[class]:
    members:
      - "-id: OrderId"
      - "+total(): Money"
```

or:

```yaml
- Order[class]:
    - "-id: OrderId"
    - "+total(): Money"
```

Common relationship types:

- `association`
- `dependency`
- `inherits`
- `inheritance`
- `extends`
- `implements`
- `realization`
- `composition`
- `aggregation`

Association details:

```yaml
- Customer --> Order:
    type: association
    sourceRole: "buyer"
    targetRole: "orders"
    sourceMultiplicity: "1"
    targetMultiplicity: "0..*"
    navigable: true
```

Class-specific properties include stereotypes, templates, modifiers, association
classes, and scanner evidence. Validation checks member syntax, identifiers,
relationship semantics, multiplicity, roles, inheritance/implementation misuse,
and common generated-model smells. Layout renders class boxes with compartments.

Examples:

- [class-domain-model.codi](./examples/class-domain-model.codi) and [SVG](./examples/class-domain-model.svg)
- [class-association-details.codi](./examples/class-association-details.codi) and [SVG](./examples/class-association-details.svg)
- [class-interface-contracts.codi](./examples/class-interface-contracts.codi) and [SVG](./examples/class-interface-contracts.svg)

## C4 Context

Declaration:

```yaml
Platform[c4-context]:
  - Customer[person]: "Uses the platform"
  - Platform[software-system, scope]: "System in scope"
  - Payments[external-software-system]: "Payment provider"
  - Customer --> Platform: "Places orders"
```

Purpose: one software system in context with people and external systems.

Node types:

- `person`
- `system`
- `software-system`
- `external-software-system`
- `boundary`
- `system-boundary`
- `enterprise-boundary`

Mark the system in scope:

```yaml
- Platform[software-system, scope]: "Retail checkout platform"
```

or:

```yaml
- Platform[software-system]:
    description: "Retail checkout platform"
    scope: true
```

Relationship types:

- `uses`
- `depends-on`
- `calls`
- `reads-from`
- `writes-to`
- `sends-to`
- `publishes-to`
- `subscribes-to`

Validation rejects lower-level elements such as containers, components, classes,
and databases. It checks descriptions, labels, duplicates, endpoint references,
scope, reachability, and boundary contents. Layout is C4 boundary-aware.

Examples:

- [c4-context-retail-platform.codi](./examples/c4-context-retail-platform.codi) and [SVG](./examples/c4-context-retail-platform.svg)
- [c4-context-healthcare-portal.codi](./examples/c4-context-healthcare-portal.codi) and [SVG](./examples/c4-context-healthcare-portal.svg)
- [c4-context-iot-fleet.codi](./examples/c4-context-iot-fleet.codi) and [SVG](./examples/c4-context-iot-fleet.svg)

## C4 Container

Declaration:

```yaml
Checkout[c4-container]:
  - CheckoutSystem[system-boundary, scope]:
      children:
        - WebApp[container]:
            description: "Customer UI"
            technology: "React"
        - API[container]:
            description: "Backend API"
            technology: "Rust"
  - WebApp --> API:
      label: "Calls"
      protocol: "HTTPS"
```

Purpose: containers inside one software system plus people and external systems
that interact with them.

Primary node types:

- `container`
- `database`
- `data-store`

Supporting node types:

- `person`
- `system`
- `software-system`
- `external-software-system`

Boundary types:

- `boundary`
- `system-boundary`
- `enterprise-boundary`

Containers should sit inside the scoped system boundary. Container-to-container
relationships should declare protocol, technology, tech, or transport.

Examples:

- [c4-container-retail-checkout.codi](./examples/c4-container-retail-checkout.codi) and [SVG](./examples/c4-container-retail-checkout.svg)
- [c4-container-saas-analytics.codi](./examples/c4-container-saas-analytics.codi) and [SVG](./examples/c4-container-saas-analytics.svg)
- [c4-container-open-banking.codi](./examples/c4-container-open-banking.codi) and [SVG](./examples/c4-container-open-banking.svg)

## C4 Component

Declaration:

```yaml
PaymentAPI[c4-component]:
  - API[container, scope]: "Payment API"
  - APIBoundary[container-boundary]:
      children:
        - PaymentController[component]:
            description: "Handles payment requests"
            technology: "Axum"
        - PaymentService[component]:
            description: "Coordinates payment workflow"
            technology: "Rust"
  - PaymentController --> PaymentService:
      label: "Delegates command"
      protocol: "in-process"
```

Purpose: components inside one container plus neighboring containers, systems,
people, and stores.

Primary node type:

- `component`

Supporting node types:

- `person`
- `system`
- `software-system`
- `external-software-system`
- `container`
- `database`
- `data-store`

Boundary types:

- `boundary`
- `container-boundary`

Components should sit inside the scoped container boundary. Supporting elements
should usually sit outside that boundary unless they are the scoped container.
Relationships crossing to containers or systems should declare protocol,
technology, tech, or transport.

Examples:

- [c4-component-payment-service.codi](./examples/c4-component-payment-service.codi) and [SVG](./examples/c4-component-payment-service.svg)
- [c4-component-notification-service.codi](./examples/c4-component-notification-service.codi) and [SVG](./examples/c4-component-notification-service.svg)
- [c4-component-ingestion-service.codi](./examples/c4-component-ingestion-service.codi) and [SVG](./examples/c4-component-ingestion-service.svg)

## C4 Code

Declaration:

```yaml
PaymentModule[c4-code]:
  - PaymentComponent[component, scope]: "Scoped component"
  - PaymentPackage[package]:
      children:
        - PaymentService[class]:
            members:
              - "+authorize(command: AuthorizePayment): Result"
        - PaymentPort[interface]:
            members:
              - "+authorize(request: PaymentRequest): PaymentResult"
  - PaymentService --> PaymentPort:
      type: implements
      label: "implements"
```

Purpose: code-level structure inside one component.

Primary node types:

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

Supporting node types:

- `component`
- `container`
- `database`
- `data-store`

Boundary types:

- `boundary`
- `component-boundary`
- `package`

Relationship types include C4 relationships plus structural class/code
relationships such as `inherits`, `implements`, `composition`, and
`aggregation`. Structural relationships are type-checked: for example,
`implements` must target an interface or trait.

Examples:

- [c4-code-payment-module.codi](./examples/c4-code-payment-module.codi) and [SVG](./examples/c4-code-payment-module.svg)
- [c4-code-repository-layer.codi](./examples/c4-code-repository-layer.codi) and [SVG](./examples/c4-code-repository-layer.svg)
- [c4-code-event-handler.codi](./examples/c4-code-event-handler.codi) and [SVG](./examples/c4-code-event-handler.svg)

## Threat Model

Declaration:

```yaml
UploadThreatModel[threat-model]:
  - User[external-entity]: "Uploads content"
  - Internet[trust-boundary]:
      children:
        - UploadAPI[process]:
            description: "Accepts upload requests"
            technology: "Rust"
        - FileStore[data-store]:
            description: "Stores uploaded files"
            encrypted: true
  - User --> UploadAPI:
      label: "HTTPS upload"
      encrypted: true
      data-classification: pii
```

Purpose: STRIDE-compatible data-flow diagrams with trust boundaries and authored
threat annotations.

Node types:

- `trust-boundary`
- `process`
- `data-store`
- `external-entity`

Edge type:

- default `data-flow`

Edge properties:

- `label`
- `encrypted`
- `protocol`
- `data-classification`
- `flow-id` or `id`
- `threats`
- `bidirectional`

Threat annotations:

```yaml
threats:
  - category: spoofing
    severity: high
    status: mitigated
    element: UploadAPI
    mitigation: "OIDC token validation"
```

Supported STRIDE categories:

- `spoofing`
- `tampering`
- `repudiation`
- `information-disclosure`
- `denial-of-service`
- `elevation-of-privilege`

Validation checks threat vocabulary, severity/status, duplicate names, endpoint
references, flow IDs, boundary crossings, sensitive classifications, encryption,
reachability, and authored threat references.

Examples:

- [threat-model-file-upload.codi](./examples/threat-model-file-upload.codi) and [SVG](./examples/threat-model-file-upload.svg)
- [threat-model-oidc-flow.codi](./examples/threat-model-oidc-flow.codi) and [SVG](./examples/threat-model-oidc-flow.svg)
- [threat-model-ci-cd.codi](./examples/threat-model-ci-cd.codi) and [SVG](./examples/threat-model-ci-cd.svg)

## Gantt

Declaration:

```yaml
LaunchPlan[gantt]:
  - timeline:
      scale: week
  - Design[task]:
      start: 2026-06-10
      duration: 5d
  - Launch[milestone]:
      date: 2026-07-01
  - Design --> Launch:
      type: finish-start
```

Purpose: project plans, resource lanes, milestones, dependencies, and timelines.

Node types:

- `task`
- `milestone`
- `group`
- `lane`
- `resource`

Common aliases are normalized by the validator, such as `phase` for group-like
structure and dependency aliases for finish/start relationships.

Common task properties:

- `start`
- `end` or `finish`
- `duration`
- `progress`
- `resource` or `resources`
- `baseline-start`
- `baseline-end`
- `deadline`
- `critical`

Timeline and calendar directives:

```yaml
- timeline:
    scale: month
    today: 2026-06-10
- calendar:
    timezone: Europe/Sofia
    work_week: [mon, tue, wed, thu, fri]
    holidays:
      - 2026-06-24
```

Dependencies:

```yaml
- Design --> Build:
    type: finish-start
    lag: 2d
- Build --> Test:
    type: start-start
```

Dependency types:

- `finish-start`
- `start-start`
- `finish-finish`
- `start-finish`
- `soft-link`

Validation checks schedules, invalid date/duration values, resources,
dependency endpoints, dependency cycles, calendar settings, markers, critical
path options, and dependency timing. Rendering uses a Gantt-specific table and
timeline payload rather than generic node boxes.

Examples:

- [gantt-product-launch.codi](./examples/gantt-product-launch.codi) and [SVG](./examples/gantt-product-launch.svg)
- [gantt-resource-plan.codi](./examples/gantt-resource-plan.codi) and [SVG](./examples/gantt-resource-plan.svg)
- [gantt-critical-path.codi](./examples/gantt-critical-path.codi) and [SVG](./examples/gantt-critical-path.svg)
