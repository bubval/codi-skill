# Diagram Type Reference

All diagram types use the same parser grammar from [grammar.md](./grammar.md):
one top-level `Name[diagram-type]` key, a list body, property items for
`layout:`/`style:`, implicit children, and top-level semantic properties.
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

Full fragment vocabulary: `alt`, `else`, `opt`, `loop`, `par`, `break`,
`critical`, `neg`, `assert`, `strict`, `seq`, `ignore`, `consider`, and `ref`.

Lifelines, notes, and fragments accept a `style:` map:

```yaml
- WebApp[participant]:
    style:
      fill: "#eff6ff"
      stroke: "#3b82f6"
```

Sequence layout is time-based: there are no `layout:` keys for this type.
Validation focuses on lifeline vocabulary, message endpoints, message sorts,
fragment directives, notes, and lifecycle consistency. Layout places lifelines
horizontally and events/messages vertically in source order.

Examples:

- [sequence/01-basic-messages-lifecycle.codi](./examples/sequence/01-basic-messages-lifecycle.codi)
- [sequence/02-fragments-notes-refs.codi](./examples/sequence/02-fragments-notes-refs.codi)
- [sequence/03-parallel-and-boundary.codi](./examples/sequence/03-parallel-and-boundary.codi)

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

Node vocabulary is intentionally open. Unknown node types are accepted, and
unknown *semantic* properties are allowed — but layout and style properties
must use the `layout:` and `style:` maps like every other type:

```yaml
- API[service]:
    label: "Public API"
    owner: "platform"          # open semantic key — allowed top-level
    layout:
      width: 220
      height: 90
    style:
      shape: rect
      fill: "#f5f7ff"
      stroke: "#4f46e5"
      text: "#111827"
      line: dashed
```

`shape` lives under `style:` for this type — the `[type]` annotation carries
meaning; the shape override is visual only.

Diagram layout (the `algorithm` key is unique to unstructured):

```yaml
- layout:
    algorithm: organic
    direction: LR
    rank_gap: 160
    node_gap: 60
```

Edge styling:

```yaml
- API --> Queue:
    label: "events"
    style:
      line: dashed
      stroke: "#6b7280"
      stroke_width: 2
```

Validation warns about unsupported or malformed renderer-relevant options, such
as invalid `algorithm`, invalid `direction`, negative numeric values, and old
grouping props. Layout uses organic/force-style behavior unless direction and
nesting make a structured layout more appropriate.

Examples:

- [unstructured/01-freeform-groups.codi](./examples/unstructured/01-freeform-groups.codi)
- [unstructured/02-styling-and-edge-styles.codi](./examples/unstructured/02-styling-and-edge-styles.codi)
- [unstructured/03-layout-affinity.codi](./examples/unstructured/03-layout-affinity.codi)

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

Diagram layout:

```yaml
- layout:
    direction: LR
    rank_gap: 180
    node_gap: 48
```

Nested flowchart groups use a list body with property items:

```yaml
- Fulfillment[group]:
    - layout:
        direction: TB
    - style:
        fill: "#eff6ff"
    - ReserveInventory[process]
    - PackOrder[process]
    - ReserveInventory --> PackOrder: "reserved"
```

Container-layout keys (`direction`, `rank_gap`, `node_gap`) are only meaningful
on the diagram and on containers; on a leaf node they warn. `width`/`height`
under `layout:` are valid on any node.

Validation checks direction values, duplicate node names, duplicate edges,
numeric layout props, and layout-only nodes. Layout is directed and
container-aware.

Examples:

- [flowchart/01-process-flow.codi](./examples/flowchart/01-process-flow.codi)
- [flowchart/02-nested-groups-and-styling.codi](./examples/flowchart/02-nested-groups-and-styling.codi)

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

Common grammar. Lane membership is expressed by nesting only — there is no
`lane:` property:

```yaml
- Intake[swimlane]:
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
`type: object-flow`. Edge `guard` and `weight` are top-level semantic keys.

Diagram spacing goes under `layout:` and includes the activity-specific
`lane_gap` and `edge_gap` keys:

```yaml
- layout:
    rank_gap: 120
    node_gap: 44
    lane_gap: 32
```

Validation checks node vocabulary, endpoint references, invalid object/control
flow combinations, partition membership, pins, regions, and common UML activity
constraints. Layout renders action/control/object nodes and swimlane-style
grouping.

Examples:

- [activity/01-control-flow.codi](./examples/activity/01-control-flow.codi)
- [activity/02-actions-pins-object-flow.codi](./examples/activity/02-actions-pins-object-flow.codi)
- [activity/03-lanes-regions.codi](./examples/activity/03-lanes-regions.codi)

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

State behavior (snake_case keys):

```yaml
- Paid[state]:
    entry_action: "sendReceipt"
    do_activity: "waitForFulfillment"
    exit_action: "closeInvoice"
    internal_transitions:
      - event: "refundRequested"
        action: "openRefundCase"
    deferred:
      - "shipmentUpdated"
```

Composite states nest children implicitly; orthogonal regions keep the explicit
`regions:` key:

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

A composite state that needs layout or style alongside children uses the list
body:

```yaml
- Active[composite-state]:
    - layout:
        direction: LR
    - style:
        fill: "#f0fdf4"
    - entry_action: "attach media surface"
    - Playing[state]
    - Paused[state]
    - Playing --> Paused:
        trigger: pause
```

Validation checks state vocabulary, transition endpoints, transition properties,
diagram props, composite/region structure, history kinds, and scoped names.
Layout uses directed state graph layout and supports nested/composite rendering.

Examples:

- [state-machine/01-basic-lifecycle.codi](./examples/state-machine/01-basic-lifecycle.codi)
- [state-machine/02-pseudostates-composite.codi](./examples/state-machine/02-pseudostates-composite.codi)
- [state-machine/03-regions-internal-transitions.codi](./examples/state-machine/03-regions-internal-transitions.codi)

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

or the string-list shorthand:

```yaml
- Order[class]:
    - "-id: OrderId"
    - "+total(): Money"
```

Packages are containers; their children are plain list items:

```yaml
- Domain[package]:
    - style:
        fill: "#f8fafc"
    - Order[class]:
        - "+ id: UUID"
    - OrderLine[class]
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

Association details (snake_case keys):

```yaml
- Customer --> Order:
    type: association
    source_role: "buyer"
    target_role: "orders"
    source_multiplicity: "1"
    target_multiplicity: "0..*"
    navigability: target
```

Stereotypes can come from the bracket annotation (`Repository[interface,
repository]`) or the `stereotype:` property; when both are present the property
wins. Template parameters use `template_parameters:` with `name` (and optional
`constraint`/`default`) entries. Validation checks member syntax, identifiers,
relationship semantics, multiplicity, roles, inheritance/implementation misuse,
and common generated-model smells. Layout renders class boxes with compartments.

Examples:

- [class/01-members-interfaces-enums.codi](./examples/class/01-members-interfaces-enums.codi)
- [class/02-relationships-multiplicity.codi](./examples/class/02-relationships-multiplicity.codi)
- [class/03-stereotypes-templates-association.codi](./examples/class/03-stereotypes-templates-association.codi)

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

Mark external systems with the `external-software-system` type or the
`external` annotation (`[system, external]`).

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

- [c4-context/01-saas-context.codi](./examples/c4-context/01-saas-context.codi)
- [c4-context/02-boundaries-and-metadata.codi](./examples/c4-context/02-boundaries-and-metadata.codi)

## C4 Container

Declaration:

```yaml
Checkout[c4-container]:
  - CheckoutSystem[software-system]:
      scope: true
      description: "Checkout system"
  - CheckoutBoundary[system-boundary]:
      - WebApp[container]:
          description: "Customer UI"
          technology: "React"
      - API[container]:
          description: "Backend API"
          technology: "Rust"
  - WebApp --> API:
      label: "Sends checkout commands"
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

Containers should sit inside the scoped system boundary. The technology key is
`technology` — the old `tech` alias is gone. Container-to-container
relationships should declare `protocol`, `technology`, or `transport`.

Examples:

- [c4-container/01-system-containers.codi](./examples/c4-container/01-system-containers.codi)
- [c4-container/02-boundary-and-technology.codi](./examples/c4-container/02-boundary-and-technology.codi)

## C4 Component

Declaration:

```yaml
PaymentAPI[c4-component]:
  - API[container, scope]: "Payment API"
  - APIBoundary[container-boundary]:
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
Relationships crossing to containers or systems should declare `protocol`,
`technology`, or `transport`.

Examples:

- [c4-component/01-service-components.codi](./examples/c4-component/01-service-components.codi)
- [c4-component/02-container-boundary.codi](./examples/c4-component/02-container-boundary.codi)

## C4 Code

Declaration:

```yaml
PaymentModule[c4-code]:
  - PaymentComponent[component, scope]: "Scoped component"
  - PaymentPackage[package]:
      - PaymentService[class]:
          members:
            - "+authorize(command: AuthorizePayment): Result"
      - PaymentPort[interface]:
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

Class-like nodes take members via the string-list shorthand or the explicit
`members:` key, exactly like the `class` type. Relationship types include C4
relationships plus structural class/code relationships such as `inherits`,
`implements`, `composition`, and `aggregation`. Structural relationships are
type-checked: for example, `implements` must target an interface or trait.

Examples:

- [c4-code/01-modules-functions-tables.codi](./examples/c4-code/01-modules-functions-tables.codi)
- [c4-code/02-members-and-boundaries.codi](./examples/c4-code/02-members-and-boundaries.codi)

## Threat Model

Declaration:

```yaml
UploadThreatModel[threat-model]:
  - User[external-entity]: "Uploads content"
  - Internet[trust-boundary]:
      - UploadAPI[process]:
          description: "Accepts upload requests"
          technology: "Rust"
      - FileStore[data-store]:
          description: "Stores uploaded files"
          encrypted: true
  - User --> UploadAPI:
      label: "HTTPS upload"
      encrypted: true
      data_classification: pii
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

Edge properties (snake_case keys; type names stay dash-case):

- `label`
- `encrypted`
- `authenticated`
- `protocol`
- `data_classification`
- `flow_id`
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
    residual_risk: "Token replay within 5-minute window"
```

Threats can target elements by `element` or flows by `flow_id`. Supported
STRIDE categories:

- `spoofing`
- `tampering`
- `repudiation`
- `information-disclosure`
- `denial-of-service`
- `elevation-of-privilege`

Validation checks threat vocabulary, severity/status, duplicate names, endpoint
references, flow IDs, boundary crossings, sensitive classifications, encryption,
reachability, and authored threat references. Diagram `layout:` gaps
(`rank_gap`, `node_gap`) are honored.

Examples:

- [threat-model/01-boundaries-and-data-flows.codi](./examples/threat-model/01-boundaries-and-data-flows.codi)
- [threat-model/02-nested-boundaries-and-controls.codi](./examples/threat-model/02-nested-boundaries-and-controls.codi)
- [threat-model/03-auth-webhook-and-queue.codi](./examples/threat-model/03-auth-webhook-and-queue.codi)

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
      depends_on:
        - Design
```

Purpose: project plans, resource lanes, milestones, dependencies, and timelines.

Node types:

- `task`
- `milestone`
- `group`
- `lane`
- `resource`

Common aliases are normalized by the validator, such as `phase` for group-like
structure.

Common task properties (snake_case):

- `start`
- `end`
- `duration`
- `progress`
- `resource` or `resources`
- `depends_on`
- `baseline_start`
- `baseline_end`
- `deadline`
- `critical`

Timeline and calendar directives (these stay their own directives — gantt has
no `layout:` keys; the timeline is computed from dates):

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

Dependencies are declared with `depends_on` on the dependent task or milestone.
Gantt does **not** use arrow edges. The simple form lists predecessor names;
the typed form is a mapping with `task` and optional `type`, `lag`, `lead`:

```yaml
- Build[task]:
    start: 2026-06-17
    duration: 10d
    depends_on:
      - Design
- Test[task]:
    duration: 4d
    depends_on:
      - task: Build
        type: start-start
        lag: 2d
```

Dependency types:

- `finish-start` (default)
- `start-start`
- `finish-finish`
- `start-finish`

Validation checks schedules, invalid date/duration values, resources,
dependency endpoints, dependency cycles, calendar settings, markers, critical
path options, and dependency timing. Rendering uses a Gantt-specific table and
timeline payload rather than generic node boxes.

Examples:

- [gantt/01-basic-tasks.codi](./examples/gantt/01-basic-tasks.codi)
- [gantt/02-groups-milestones-resources.codi](./examples/gantt/02-groups-milestones-resources.codi)
- [gantt/03-calendars-dependencies-critical-path.codi](./examples/gantt/03-calendars-dependencies-critical-path.codi)

## Deployment

Declaration. Containers nest children as list items; a container that also
carries properties writes them as property items:

```yaml
KubernetesPalette[deployment]:
  - PlatformCluster[cluster]:
      - provider: k8s
      - platform: kubernetes
      - AppNamespace[namespace]:
          - WebDeployment[deployment]:
              - image: "registry.example.com/web:2026.06"
              - WebPod[pod]:
                  - WebContainer[container]
          - AppSecret[secret]
  - WebDeployment --> AppSecret:
      type: uses-secret
```

Purpose: infrastructure and runtime deployment topology — clouds, regions,
networks, clusters, namespaces, workloads, data stores, routing, and the
relationships between them.

Node vocabulary (scopes, networks, compute, workloads, routing, data, and more):

- scopes: `cloud`, `region`, `zone`, `availability-zone`, `edge-location`
- networking: `network`, `vpc`, `subnet`, `security-group`, `firewall`,
  `private-link`, `vpn`
- compute: `cluster`, `namespace`, `node-pool`, `node`, `function`
- workloads: `workload`, `deployment`, `statefulset`, `daemonset`, `job`,
  `cronjob`, `pod`, `container`
- routing: `service`, `ingress`, `gateway`, `load-balancer`, `api-gateway`,
  `dns`, `cdn`
- config/secrets/storage: `config-map`, `secret`, `volume`, `persistent-volume`,
  `persistent-volume-claim`, `bucket`, `object-store`
- data: `database`, `cache`, `queue`, `topic`, `registry`
- other: `identity-provider`, `external-system`

Relationship types:

- placement: `hosts`, `runs`, `deploys-to`, `contains`, `scheduled-on`
- traffic: `routes-to`, `calls`, `connects-to`, `exposes`, `forwards-to`
- data: `reads-from`, `writes-to`, `publishes-to`, `subscribes-to`
- mounts/config: `mounts`, `uses-secret`, `uses-config`, `pulls-image-from`
- security: `allows`, `denies`, `terminates-tls`, `authenticates-with`

Common node properties: `provider` (`aws|azure|gcp|k8s|generic`), `platform`
(`kubernetes|vm|serverless|managed`), `environment`, `region`, `zone`,
`replicas`, `image`, `version`, `public`, `encrypted`, `managed`. Edge
properties include `type`, `protocol` (`HTTPS|HTTP|TCP|UDP|gRPC|AMQP|Kafka`),
`port`, `encrypted`, `internal`, and `direction`. Node sizing uses `width`
under `layout:`.

Validation checks node/edge vocabulary, endpoint references, namespace nesting
for Kubernetes workloads and namespace-scoped resources, cluster placement and
platform, workload `image`/`version`, database encryption, and provider-specific
property placement. Layout nests clouds, networks, clusters, and namespaces as
containers and distinguishes placement edges from traffic edges.

Examples:

- [deployment/01-kubernetes-platform.codi](./examples/deployment/01-kubernetes-platform.codi)
- [deployment/02-cloud-neutral-provider.codi](./examples/deployment/02-cloud-neutral-provider.codi)
- [deployment/03-node-types-and-relationships.codi](./examples/deployment/03-node-types-and-relationships.codi)
