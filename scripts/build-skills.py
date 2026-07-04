#!/usr/bin/env python3
"""Build the public CoDi multi-skill package.

This script is for repository maintainers. It generates the selectable
`skills/<name>` folders consumed by `npx skills add`.
"""

from __future__ import annotations

import shutil
import textwrap
from dataclasses import dataclass, field
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent
DOCS = WORKSPACE / "codi-docs"
DIAGRAM_DOCS = DOCS / "diagrams"
# Examples are grouped per diagram type: examples/<diagram-type>/NN-name.codi
EXAMPLES = DIAGRAM_DOCS / "examples"


@dataclass(frozen=True)
class DiagramSkill:
    name: str
    title: str
    diagram_type: str
    purpose: str
    choose_when: list[str]
    avoid_when: list[str]
    node_types: list[str]
    edge_types: list[str]
    diagram_props: list[tuple[str, str, str]]
    node_props: list[tuple[str, str, str]]
    edge_props: list[tuple[str, str, str]]
    grammar_notes: list[str]
    validation_notes: list[str]
    layout_notes: list[str]
    examples: list[str]
    layout_props: list[tuple[str, str, str]] = field(default_factory=list)
    style_extra: list[tuple[str, str, str]] = field(default_factory=list)
    edge_props_title: str = "Edge Properties"


COMMON_NODE_PROPS = [
    ("description", "string", "Short description rendered or used by validators."),
    ("label", "string", "Display label override."),
    ("links", "list/object", "External links attached to the node."),
    ("refs", "list", "Source references or related `.codi` files."),
]

# Shared style vocabulary: identical for every diagram type, always nested
# under `style:`. Canonical names only — the old aliases (`color`, `border`,
# `border_color`, `border_width`, `text_color`, `muted_text_color`) and the
# bare `style: dashed` scalar are gone.
STYLE_PROPS = [
    ("fill", "color string", "Fill color."),
    ("stroke", "color string", "Stroke/border color."),
    ("stroke_width", "number", "Stroke width."),
    ("text", "color string", "Text color."),
    ("muted_text", "color string", "Secondary text color."),
    ("opacity", "0..1", "Opacity."),
    ("line", "solid | dashed | dashed-border", "Line treatment (replaces the old `style:` scalar)."),
    ("dash", "list[number]", "Custom dash pattern, for example `[8, 5]`."),
]

EDGE_STYLE_KEYS = "`stroke`, `stroke_width`, `opacity`, `line`, and `dash`"

# Container-layout keys arrange a node's CHILDREN. They are valid on the
# diagram root and on container nodes; on a leaf node they warn.
CONTAINER_LAYOUT_PROPS = [
    ("direction", "TB | LR | RL | BT", "Graph direction for child arrangement."),
    ("rank_gap", "non-negative number", "Space between graph ranks."),
    ("node_gap", "non-negative number", "Space between sibling nodes."),
]

# Self-layout keys size the node itself and are valid on ANY node.
SELF_LAYOUT_PROPS = [
    ("width", "positive number", "Node width in layout units (valid on any node)."),
    ("height", "positive number", "Node height in layout units (valid on any node)."),
]

C4_RELATIONSHIPS = [
    "uses",
    "depends-on",
    "calls",
    "reads-from",
    "writes-to",
    "sends-to",
    "publishes-to",
    "subscribes-to",
]

STRUCTURAL_RELATIONSHIPS = [
    "association",
    "dependency",
    "inherits",
    "inheritance",
    "extends",
    "implements",
    "realization",
    "composition",
    "aggregation",
]

C4_EDGE_PROPS = [
    ("label", "string", "Human-readable relationship label."),
    ("type", "enum", "Relationship type."),
    ("technology", "string", "Technology used by the relationship."),
    ("protocol", "string", "Protocol used by the relationship."),
    ("transport", "string", "Transport used by the relationship."),
    ("links", "list/object", "External links attached to the relationship."),
]

# Minimal VALID declaration snippet per type. Each of these passes
# `codi validate` — keep them green when editing.
DECLARATIONS = {
    "sequence": """Login[sequence]:
  - Browser[actor]
  - API[service]
  - sync Browser -> API: "POST /login"
  - reply Browser <-- API: "200 OK\"""",
    "unstructured": """ServiceMap[unstructured]:
  - API[service]
  - Queue[queue]
  - API --> Queue: "publishes\"""",
    "flowchart": """ReleaseGate[flowchart]:
  - Draft[process]
  - Review[decision]
  - Draft --> Review: "submit\"""",
    "activity": """Approval[activity]:
  - start[initial-node]
  - Review[action]
  - done[activity-final-node]
  - start --> Review
  - Review --> done""",
    "state-machine": """OrderState[state-machine]:
  - initial --> Created
  - Created[state]
  - Created --> final:
      trigger: "archived\"""",
    "class": """Domain[class]:
  - Order[class]:
      - "+ id: UUID"
  - PaymentPort[interface]:
      - "+ charge(order: Order): void"
  - Order --> PaymentPort:
      type: dependency""",
    "c4-context": """Platform[c4-context]:
  - Customer[person]: "Uses the platform"
  - PlatformSystem[software-system]:
      scope: true
      description: "System in scope"
  - Payments[external-software-system]: "Payment provider"
  - Customer --> PlatformSystem: "Places orders"
  - PlatformSystem --> Payments: "Charges cards\"""",
    "c4-container": """Checkout[c4-container]:
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
      protocol: "HTTPS\"""",
    "c4-component": """PaymentAPI[c4-component]:
  - API[container, scope]: "Payment API"
  - APIBoundary[container-boundary]:
      - Controller[component]:
          description: "Handles payment requests"
          technology: "Axum"
      - Service[component]:
          description: "Coordinates payment workflow"
          technology: "Rust"
  - Controller --> Service:
      label: "Delegates command"
      protocol: "in-process\"""",
    "c4-code": """PaymentModule[c4-code]:
  - PaymentComponent[component, scope]: "Payments component"
  - PaymentService[class]:
      - "+ authorize(request: PaymentRequest): PaymentResult"
  - PaymentPort[interface]:
      - "+ authorize(request: PaymentRequest): PaymentResult"
  - PaymentService --> PaymentPort:
      type: implements
      label: "implements port\"""",
    "threat-model": """UploadModel[threat-model]:
  - User[external-entity]: "Uploads content"
  - AppTier[trust-boundary]:
      - UploadAPI[process]: "Accepts upload requests"
  - User --> UploadAPI:
      label: "HTTPS upload"
      protocol: HTTPS
      encrypted: true""",
    "gantt": """LaunchPlan[gantt]:
  - Design[task]:
      start: 2026-06-10
      duration: 5d
  - Launch[milestone]:
      date: 2026-07-01
      depends_on:
        - Design""",
    "deployment": """Production[deployment]:
  - AppCluster[cluster]:
      - platform: kubernetes
      - WebNamespace[namespace]:
          - Web[deployment]:
              image: "registry/web:1.0.0"
  - Internet[external-system]: "Public traffic"
  - Internet --> Web:
      type: routes-to
      protocol: HTTPS
      encrypted: true""",
}


DIAGRAMS = [
    DiagramSkill(
        name="codi-sequence",
        title="CoDi Sequence",
        diagram_type="sequence",
        purpose="Ordered interactions over time between actors, services, systems, databases, and objects.",
        choose_when=[
            "Explaining request/response flows, login flows, async work, callbacks, retries, or lifecycle behavior.",
            "Source order matters and messages should appear vertically in time order.",
            "You need sequence-specific constructs such as activation, replies, notes, and fragments.",
        ],
        avoid_when=[
            "The goal is static system topology; use C4 or unstructured instead.",
            "The goal is a generic process with decisions and parallel branches; use activity or flowchart.",
        ],
        node_types=[
            "actor",
            "participant",
            "lifeline",
            "service",
            "server",
            "database",
            "component",
            "object",
            "system",
        ],
        edge_types=[
            "message",
            "sync",
            "call",
            "async",
            "reply",
            "create",
            "destroy",
            "found",
            "lost",
            "self",
        ],
        diagram_props=[],
        layout_props=[],
        node_props=COMMON_NODE_PROPS,
        edge_props=[
            ("label", "string", "Message text."),
            ("type", "enum", "Message sort, commonly inferred from directive syntax."),
        ],
        grammar_notes=[
            "Declare lifelines before messages where possible.",
            "Generic arrows are supported: `A --> B`, `A <-- B`, and `A <--> B`.",
            "Sequence directives include `sync`, `call`, `async`, `reply`, `create`, `destroy`, `found`, `lost`, and `self`.",
            "Lifecycle directives include `activate X`, `deactivate X`, and `destroy X`.",
            "Notes use `note over X`, `note left of X`, or `note right of X`.",
            "Fragments use `alt`, `else`, `opt`, `loop`, `par`, `break`, `critical`, `neg`, `assert`, `strict`, `seq`, `ignore`, `consider`, and `ref` list items; fragment messages nest implicitly as indented list items.",
            "Lifelines, notes, and fragments accept a `style:` map (block form).",
        ],
        validation_notes=[
            "Every message endpoint must be a declared lifeline unless the directive explicitly models found/lost messages.",
            "Duplicate lifeline names are rejected.",
            "Replies should match a prior call where possible.",
            "Messages after a destroyed lifeline are invalid.",
        ],
        layout_notes=[
            "Sequence layout is time-based; there are no `layout:` keys for this type.",
            "Lifelines are laid out horizontally in declaration order.",
            "Messages, fragments, notes, activation, and destruction events are laid out vertically in source order.",
            "Render target aspect ratio pads the output but does not change event order.",
        ],
        examples=[
            "01-basic-messages-lifecycle.codi",
            "02-fragments-notes-refs.codi",
            "03-parallel-and-boundary.codi",
        ],
    ),
    DiagramSkill(
        name="codi-unstructured",
        title="CoDi Unstructured",
        diagram_type="unstructured",
        purpose="Permissive freeform diagrams, concept maps, dependency webs, ownership maps, and quick sketches.",
        choose_when=[
            "You need readable topology but not a strict semantic model.",
            "Node types are domain-specific or experimental.",
            "You want rich visual styling and nested groups without strict validation.",
        ],
        avoid_when=[
            "You need C4, UML, STRIDE, or Gantt-specific validation.",
            "A strict diagram type exists for the domain and should catch mistakes.",
        ],
        node_types=["open vocabulary; any node type annotation is accepted"],
        edge_types=["open vocabulary; generic arrows default to normal relationships"],
        diagram_props=[],
        layout_props=[
            ("algorithm", "organic | force | force-directed | fdg", "Layout algorithm (unique to unstructured)."),
            *CONTAINER_LAYOUT_PROPS,
            *SELF_LAYOUT_PROPS,
        ],
        style_extra=[
            ("shape", "string", "Renderer shape override such as `hexagon` or `cylinder`; the `[type]` annotation keeps carrying meaning."),
        ],
        node_props=[
            *COMMON_NODE_PROPS,
            ("icon", "string", "Renderer icon name."),
            ("members", "list[string]", "Member strings for class-like boxes."),
            ("layout_only", "boolean", "Marks a layout helper/affinity group."),
        ],
        edge_props=[
            ("label", "string", "Relationship label."),
            ("links", "list/object", "External links attached to the edge."),
        ],
        grammar_notes=[
            "Use any readable node type: `API[service]`, `Queue[queue]`, `Team[team]`.",
            "Groups nest children as plain list items; a group with properties writes them as property items (`- label: \"x\"`, `- style:` block) in the same list.",
            "Unknown semantic keys are allowed top-level (that is the point of the type), but layout and style keys must sit under `layout:`/`style:`.",
            "`shape` lives under `style:` — it is visual geometry, not semantics.",
        ],
        validation_notes=[
            "Unknown node types are accepted.",
            "Invalid layout options, negative dimensions, unsupported group props, and malformed renderer values warn or fail according to severity.",
        ],
        layout_notes=[
            "Defaults to organic/force-style layout.",
            "Structured direction and nesting can make layout more regular.",
            "Wide/tall render targets can tune spacing and spread.",
        ],
        examples=[
            "01-freeform-groups.codi",
            "02-styling-and-edge-styles.codi",
            "03-layout-affinity.codi",
        ],
    ),
    DiagramSkill(
        name="codi-flowchart",
        title="CoDi Flowchart",
        diagram_type="flowchart",
        purpose="Generic directed process flows with decisions, stages, nested groups, and readable domain-specific node kinds.",
        choose_when=[
            "You need a directed process or decision flow.",
            "The node vocabulary should remain flexible but the graph should be structured.",
            "You need nested process groups with directed layout.",
        ],
        avoid_when=[
            "You need UML activity semantics such as object flows, pins, partitions, forks, and joins.",
            "You need a timeline; use Gantt.",
        ],
        node_types=["open vocabulary; common: start, terminal, process, decision, group, note, category, examples, container"],
        edge_types=["generic directed edges via `-->`, `<--`, `<-->`"],
        diagram_props=[],
        layout_props=[*CONTAINER_LAYOUT_PROPS, *SELF_LAYOUT_PROPS],
        node_props=[
            *COMMON_NODE_PROPS,
            ("layout_only", "boolean", "Marks a layout helper/group."),
            ("show_title", "boolean", "Shows or hides a container title."),
        ],
        edge_props=[
            ("label", "string", "Branch or flow label."),
            ("type", "string", "Edge kind where meaningful."),
            ("links", "list/object", "External links attached to the edge."),
        ],
        grammar_notes=[
            "Use readable domain-specific node types, for example `Review[decision]` or `Deploy[process]`.",
            "Groups nest children as plain list items; group layout and style are property items (`- layout:` block, `- style:` block) in the same list.",
            "Use labels on decision outgoing edges for branch meaning.",
        ],
        validation_notes=[
            "Duplicate node names and duplicate edges are flagged.",
            "Direction must be one of `LR`, `RL`, `TB`, or `BT`.",
            "Numeric layout props must be non-negative.",
            "Container-layout keys on a leaf node warn: layout only affects child nodes.",
            "`layout_only` nodes should have children.",
        ],
        layout_notes=[
            "Uses directed graph layout and supports nested containers.",
            "Explicit `direction` wins over render target direction hints.",
        ],
        examples=[
            "01-process-flow.codi",
            "02-nested-groups-and-styling.codi",
        ],
    ),
    DiagramSkill(
        name="codi-activity",
        title="CoDi Activity",
        diagram_type="activity",
        purpose="UML-style activity diagrams with actions, object flows, control nodes, swimlanes, forks, joins, and regions.",
        choose_when=[
            "You need UML activity semantics rather than a generic flowchart.",
            "You need swimlanes/partitions, object nodes, pins, forks, joins, or guarded decisions.",
            "You need validation for object-flow versus control-flow mistakes.",
        ],
        avoid_when=[
            "You only need a simple process sketch; use flowchart.",
            "You need state over time; use state-machine.",
        ],
        node_types=[
            "action",
            "call-action",
            "call-operation-action",
            "call-behavior-action",
            "accept-event-action",
            "send-signal-action",
            "object",
            "object-node",
            "input-pin",
            "output-pin",
            "value-pin",
            "data-store",
            "central-buffer",
            "initial",
            "initial-node",
            "final",
            "activity-final",
            "activity-final-node",
            "flow-final",
            "flow-final-node",
            "decision",
            "decision-node",
            "merge",
            "merge-node",
            "fork",
            "fork-node",
            "join",
            "join-node",
            "swimlane",
            "partition",
            "activity-partition",
            "interruptible-region",
            "expansion-region",
            "expansion-node",
        ],
        edge_types=["control-flow", "object-flow", "interrupting-edge"],
        diagram_props=[],
        layout_props=[
            ("rank_gap", "non-negative number", "Space between graph ranks."),
            ("node_gap", "non-negative number", "Space between sibling nodes."),
            ("edge_gap", "non-negative number", "Space between parallel edges (activity-specific)."),
            ("lane_gap", "non-negative number", "Space between swimlanes (activity-specific)."),
            *SELF_LAYOUT_PROPS,
        ],
        node_props=[
            *COMMON_NODE_PROPS,
            ("operation", "string", "Required by call-operation-action."),
            ("behavior", "string", "Required by call-behavior-action."),
            ("signal", "string", "Required by accept-event-action and send-signal-action."),
        ],
        edge_props=[
            ("label", "string", "Flow label or guard text."),
            ("type", "control-flow | object-flow | interrupting-edge", "Activity edge type."),
            ("guard", "string", "Decision branch guard."),
            ("weight", "number", "Renderer/layout hint where supported."),
            ("links", "list/object", "External links attached to the edge."),
        ],
        grammar_notes=[
            "Use `initial` and `final` aliases for common endpoints.",
            "Swimlanes and regions are containers: their children are plain nested list items. Lane membership is expressed by nesting ONLY — there is no `lane:` property.",
            "A lane or action that needs both properties and children uses property items (`- operation: \"x\"`, `- style:` block) in its child list.",
            "Use `type: object-flow` for object/pin data movement.",
            "Use `type: control-flow` for control sequencing.",
        ],
        validation_notes=[
            "Initial nodes must not have incoming flow.",
            "Final nodes must not have outgoing flow.",
            "Decision nodes should have at least two guarded outgoing flows.",
            "Fork/join arity is validated.",
            "Object flows must connect actions/object nodes/pins/parameters/expansion nodes.",
            "Pins should be nested under actions.",
        ],
        layout_notes=[
            "Renders action/control/object glyphs and swimlane grouping.",
            "Source nesting controls partition membership.",
        ],
        examples=[
            "01-control-flow.codi",
            "02-actions-pins-object-flow.codi",
            "03-lanes-regions.codi",
        ],
    ),
    DiagramSkill(
        name="codi-state-machine",
        title="CoDi State Machine",
        diagram_type="state-machine",
        purpose="UML-style state machines with states, transitions, composite states, regions, history, and pseudostates.",
        choose_when=[
            "You need lifecycle/state behavior rather than process steps.",
            "Events, guards, actions, entry/do/exit behavior, and composite states matter.",
            "You need validation of pseudostate and transition rules.",
        ],
        avoid_when=[
            "You need ordered interactions between participants; use sequence.",
            "You need business process flow; use activity or flowchart.",
        ],
        node_types=[
            "state",
            "composite-state",
            "region",
            "initial",
            "final",
            "choice",
            "junction",
            "fork",
            "join",
            "entry-point",
            "exit-point",
            "terminate",
            "history",
        ],
        edge_types=["transition"],
        diagram_props=[],
        layout_props=[*CONTAINER_LAYOUT_PROPS, *SELF_LAYOUT_PROPS],
        node_props=[
            ("label", "string", "Display label."),
            ("entry_action", "string", "Entry behavior."),
            ("do_activity", "string", "Ongoing state activity."),
            ("exit_action", "string", "Exit behavior."),
            ("internal_transitions", "list", "Internal transition objects with trigger/guard/action."),
            ("deferred", "list[string]", "Deferred events."),
            ("regions", "mapping", "Composite state orthogonal regions."),
            ("type", "shallow | deep", "History pseudostate kind."),
        ],
        edge_props=[
            ("trigger", "string", "Event that triggers the transition."),
            ("guard", "string", "Guard condition."),
            ("action", "string", "Transition action."),
            ("label", "string", "Rendered transition label."),
            ("event", "string", "Alias/semantic event field."),
            ("completion", "boolean", "Completion transition flag."),
            ("type", "transition", "Explicit edge type."),
        ],
        grammar_notes=[
            "Use `initial[initial]` and `final[final]` for reserved pseudostates.",
            "Composite states nest plain children as list items; a composite with layout/style/actions plus children uses property items (`- layout:` block, `- entry_action: \"x\"`) in the same list.",
            "`regions:` stays an explicit property key for orthogonal regions — it is semantic, not generic nesting.",
            "State behavior keys are snake_case: `entry_action`, `do_activity`, `exit_action`, `internal_transitions`.",
            "Transition labels can be scalar labels or structured trigger/guard/action properties.",
        ],
        validation_notes=[
            "Reserved pseudostate names must match their type.",
            "Initial pseudostates must not have incoming transitions.",
            "Transitions from initial pseudostates must not set trigger or guard.",
            "Final and terminate pseudostates must not have outgoing transitions.",
            "Choice pseudostates require guarded outgoing transitions.",
            "Fork/join arity is validated.",
            "Node names must be unique within a scope, or references must be qualified.",
        ],
        layout_notes=[
            "Uses directed state graph layout.",
            "Composite states and regions render as nested structures.",
        ],
        examples=[
            "01-basic-lifecycle.codi",
            "02-pseudostates-composite.codi",
            "03-regions-internal-transitions.codi",
        ],
    ),
    DiagramSkill(
        name="codi-class",
        title="CoDi Class",
        diagram_type="class",
        purpose="UML class, interface, enum, and package diagrams, including scanner-generated code structure.",
        choose_when=[
            "You need static object/code structure with classes, interfaces, enums, packages, members, and relationships.",
            "You need association details such as roles, multiplicity, navigability, composition, or aggregation.",
            "You want to visualize scanner-generated model relationships.",
        ],
        avoid_when=[
            "You need C4 code-level architecture inside a component; use codi-c4-code.",
            "You need call order; use sequence.",
        ],
        node_types=["class", "interface", "enum", "package"],
        edge_types=STRUCTURAL_RELATIONSHIPS,
        diagram_props=[],
        layout_props=[*CONTAINER_LAYOUT_PROPS, *SELF_LAYOUT_PROPS],
        node_props=[
            *COMMON_NODE_PROPS,
            ("members", "list[string]", "Class/interface/enum members."),
            ("abstract", "boolean", "Marks an abstract class."),
            ("stereotype", "string", "UML stereotype; wins over a bracket-annotation stereotype."),
            ("stereotypes", "list[string]", "Multiple UML stereotypes."),
            ("template_parameters", "list", "Generic/template parameters: mappings with `name` and optional `constraint`/`default`."),
            ("language", "string", "Source language hint."),
        ],
        edge_props=[
            ("type", "enum", "Relationship type."),
            ("label", "string", "Relationship label."),
            ("source_role", "string", "Association source role."),
            ("target_role", "string", "Association target role."),
            ("source_multiplicity", "string", "Source multiplicity."),
            ("target_multiplicity", "string", "Target multiplicity."),
            ("navigability", "source | target | both | none", "Relationship navigability."),
            ("association_class", "node-ref", "Association class node reference."),
            ("constraint", "string", "Relationship constraint."),
            ("links", "list/object", "External links attached to the relationship."),
        ],
        grammar_notes=[
            "Members can be declared as `members:` or as a direct string list under a class/interface/enum.",
            "Package nodes nest classes, interfaces, enums, packages, and relationships as plain list items; package style is a `- style:` property item in the same list.",
            "Member strings and `Name[type]` children can coexist in one list body — property items are classified before the members heuristic.",
            "Member visibility commonly uses `+`, `-`, `#`, or `~`.",
            "Stereotypes come from the bracket annotation or the `stereotype:` property; the property wins on conflict.",
            "Edge endpoint keys are snake_case: `source_role`, `target_role`, `source_multiplicity`, `target_multiplicity`.",
        ],
        validation_notes=[
            "Member syntax, duplicate members, multiplicity, roles, inheritance, implementation, and generated-model smells are checked.",
            "`implements` should target an interface-like node.",
            "Large classes and large enums warn because they are hard to read.",
        ],
        layout_notes=[
            "Renders class boxes with compartments.",
            "Uses target-aware layout direction, spacing, compact packing, and candidate scoring when eligible.",
        ],
        examples=[
            "01-members-interfaces-enums.codi",
            "02-relationships-multiplicity.codi",
            "03-stereotypes-templates-association.codi",
        ],
    ),
    DiagramSkill(
        name="codi-c4-context",
        title="CoDi C4 Context",
        diagram_type="c4-context",
        purpose="C4 system context diagrams showing one software system in scope, its users, and external systems.",
        choose_when=[
            "You need a high-level system context for humans and neighboring systems.",
            "You want to communicate boundaries and external dependencies before container/component detail.",
            "You need C4 validation for context-level vocabulary.",
        ],
        avoid_when=[
            "You need deployable/runtime internals; use codi-c4-container.",
            "You need code/class internals; use codi-c4-code or codi-class.",
        ],
        node_types=["person", "system", "software-system", "external-software-system", "boundary", "system-boundary", "enterprise-boundary"],
        edge_types=C4_RELATIONSHIPS,
        diagram_props=[],
        layout_props=[*CONTAINER_LAYOUT_PROPS, *SELF_LAYOUT_PROPS],
        node_props=[
            *COMMON_NODE_PROPS,
            ("scope", "boolean/annotation", "Marks the software system in scope."),
        ],
        edge_props=C4_EDGE_PROPS,
        grammar_notes=[
            "Mark exactly one software system as in scope using `[software-system, scope]` or `scope: true`.",
            "Mark external systems with the `external-software-system` type or the `external` annotation (`[system, external]`).",
            "Boundaries may group software systems; boundary children are plain nested list items, with `- label:` as a property item when needed.",
        ],
        validation_notes=[
            "Lower-level elements such as containers, components, databases, and classes are rejected.",
            "Context relationships should have descriptive labels.",
            "Supporting elements should connect to the scoped system.",
            "Strict mode requires explicit scope.",
        ],
        layout_notes=[
            "Uses C4 boundary-aware graph layout.",
            "Wide/tall render targets can hint direction when no explicit `direction` is set.",
        ],
        examples=[
            "01-saas-context.codi",
            "02-boundaries-and-metadata.codi",
        ],
    ),
    DiagramSkill(
        name="codi-c4-container",
        title="CoDi C4 Container",
        diagram_type="c4-container",
        purpose="C4 container diagrams showing deployable/runtime containers inside one software system.",
        choose_when=[
            "You need services, apps, databases, queues, or deployable units inside a scoped system.",
            "You need neighboring users/systems around those containers.",
        ],
        avoid_when=[
            "You only need system context; use codi-c4-context.",
            "You need internals of one container; use codi-c4-component.",
        ],
        node_types=["container", "database", "data-store", "person", "system", "software-system", "external-software-system", "boundary", "system-boundary", "enterprise-boundary"],
        edge_types=C4_RELATIONSHIPS,
        diagram_props=[],
        layout_props=[*CONTAINER_LAYOUT_PROPS, *SELF_LAYOUT_PROPS],
        node_props=[
            *COMMON_NODE_PROPS,
            ("technology", "string", "Container technology (the `tech` alias is gone)."),
            ("scope", "boolean/annotation", "Marks scoped system boundary or system."),
        ],
        edge_props=C4_EDGE_PROPS,
        grammar_notes=[
            "Place containers inside a scoped `system-boundary` where possible; boundary children are plain nested list items.",
            "A boundary with a label, layout, or style plus children uses property items (`- label: \"x\"`, `- layout:` block, `- style:` block) in the same list.",
            "Use `database` or `data-store` for storage containers.",
        ],
        validation_notes=[
            "Containers should be inside the scoped system boundary.",
            "Container-to-container relationships should declare protocol, technology, or transport.",
            "Strict mode requires explicit scope.",
        ],
        layout_notes=["Uses C4 boundary-aware graph layout and target-aware direction hints."],
        examples=[
            "01-system-containers.codi",
            "02-boundary-and-technology.codi",
        ],
    ),
    DiagramSkill(
        name="codi-c4-component",
        title="CoDi C4 Component",
        diagram_type="c4-component",
        purpose="C4 component diagrams showing components inside one container and nearby containers/systems.",
        choose_when=[
            "You need controllers, services, adapters, modules, or other components inside one container.",
            "You need to show how components interact with neighboring containers and systems.",
        ],
        avoid_when=[
            "You need container-level deployment/runtime structure; use codi-c4-container.",
            "You need class/code internals; use codi-c4-code or codi-class.",
        ],
        node_types=["component", "person", "system", "software-system", "external-software-system", "container", "database", "data-store", "boundary", "container-boundary"],
        edge_types=C4_RELATIONSHIPS,
        diagram_props=[],
        layout_props=[*CONTAINER_LAYOUT_PROPS, *SELF_LAYOUT_PROPS],
        node_props=[
            *COMMON_NODE_PROPS,
            ("technology", "string", "Component technology (the `tech` alias is gone)."),
            ("scope", "boolean/annotation", "Marks scoped container."),
        ],
        edge_props=C4_EDGE_PROPS,
        grammar_notes=[
            "Mark the scoped container and nest components in a `container-boundary`; boundary children are plain nested list items with `- label:` as a property item.",
            "Keep supporting systems and containers outside the scoped boundary unless they are the scoped container.",
        ],
        validation_notes=[
            "Components should sit inside the scoped container boundary.",
            "Crossing relationships to containers or systems should declare protocol, technology, or transport.",
        ],
        layout_notes=["Uses C4 boundary-aware graph layout and target-aware direction hints."],
        examples=[
            "01-service-components.codi",
            "02-container-boundary.codi",
        ],
    ),
    DiagramSkill(
        name="codi-c4-code",
        title="CoDi C4 Code",
        diagram_type="c4-code",
        purpose="C4 code-level diagrams showing classes, interfaces, functions, modules, and packages inside one component.",
        choose_when=[
            "You need code-level architecture inside one component.",
            "You want C4 context plus class-like structure and structural relationship validation.",
        ],
        avoid_when=[
            "You only need pure UML/domain classes; use codi-class.",
            "You need component-level architecture; use codi-c4-component.",
        ],
        node_types=["class", "interface", "enum", "trait", "struct", "object", "function", "module", "record", "database-table", "component", "container", "database", "data-store", "boundary", "component-boundary", "package"],
        edge_types=[*C4_RELATIONSHIPS, *STRUCTURAL_RELATIONSHIPS],
        diagram_props=[],
        layout_props=[*CONTAINER_LAYOUT_PROPS, *SELF_LAYOUT_PROPS],
        node_props=[
            *COMMON_NODE_PROPS,
            ("members", "list[string]", "Members in class-like elements."),
            ("technology", "string", "Technology for supporting nodes."),
            ("scope", "boolean/annotation", "Marks scoped component."),
        ],
        edge_props=C4_EDGE_PROPS,
        grammar_notes=[
            "Use a scoped component and code/package boundaries to organize internals; package and boundary children are plain nested list items.",
            "Class-like members use the same string conventions as class diagrams: the string-list shorthand or explicit `members:`.",
            "Member strings and nested `Name[type]` children can coexist in one class body.",
        ],
        validation_notes=[
            "Structural relationships are type-checked.",
            "`implements` must target an interface or trait.",
            "Code elements should be inside the scoped component or package boundary.",
        ],
        layout_notes=["Uses class/code element layout with target-aware compact packing."],
        examples=[
            "01-modules-functions-tables.codi",
            "02-members-and-boundaries.codi",
        ],
    ),
    DiagramSkill(
        name="codi-threat-model",
        title="CoDi Threat Model",
        diagram_type="threat-model",
        purpose="STRIDE-compatible data-flow diagrams with trust boundaries, data stores, processes, external entities, and authored threats.",
        choose_when=[
            "You need a security data-flow diagram.",
            "You need trust boundary crossing checks, encryption checks, and authored STRIDE threats.",
            "You need threat status, severity, mitigations, and data classification.",
        ],
        avoid_when=[
            "You need general architecture without security-specific semantics; use C4 or unstructured.",
        ],
        node_types=["trust-boundary", "process", "data-store", "external-entity"],
        edge_types=["data-flow"],
        diagram_props=[
            ("threats", "list", "Top-level authored threats targeting elements or flows."),
        ],
        layout_props=CONTAINER_LAYOUT_PROPS,
        node_props=[
            *COMMON_NODE_PROPS,
            ("threats", "list", "Threats scoped to this element."),
            ("trust_level", "string", "Trust level for external entities."),
            ("technology", "string", "Technology for processes."),
            ("privilege_level", "normal | elevated", "Privilege level for processes."),
            ("controls", "list[string]", "Security controls."),
            ("encrypted", "boolean", "Encryption status for data stores."),
            ("data_classification", "public | internal | confidential | restricted | pii | phi | pci | secret", "Data sensitivity."),
        ],
        edge_props=[
            ("label", "string", "Data flow label."),
            ("type", "data-flow", "Explicit data flow type."),
            ("encrypted", "boolean", "Whether the flow is encrypted."),
            ("authenticated", "boolean", "Whether the flow is authenticated."),
            ("protocol", "string", "Protocol used by the data flow."),
            ("data", "string", "Data carried by the flow."),
            ("data_classification", "enum", "Sensitivity of data in transit."),
            ("flow_id", "string", "Stable id for targeting threats (the `id` alias is gone)."),
            ("threats", "list", "Threats scoped to this flow."),
            ("bidirectional", "boolean", "Whether the flow is bidirectional."),
        ],
        grammar_notes=[
            "Use trust boundaries as containers; boundary children are plain nested list items, with `- style:` as a property item when the boundary is styled.",
            "Use `threats:` on nodes, edges, or at the top level.",
            "Top-level threats can target elements or flows by element name, source/target, or `flow_id`.",
            "Property keys are snake_case: `flow_id`, `data_classification`, `residual_risk`. Node types stay dash-case: `trust-boundary`, `data-store`, `external-entity`.",
        ],
        validation_notes=[
            "Valid STRIDE categories: spoofing, tampering, repudiation, information-disclosure, denial-of-service, elevation-of-privilege.",
            "Valid severities: low, medium, high, critical.",
            "Valid statuses: open, mitigated, accepted.",
            "Cross-boundary flows should declare encryption and protocol/label.",
            "Sensitive data stores should declare `encrypted: true`.",
            "Elevated processes should declare controls.",
        ],
        layout_notes=[
            "Uses trust-boundary/data-flow layout and boundary-aware packing.",
            "Diagram `layout:` gaps (`rank_gap`, `node_gap`) are honored.",
        ],
        examples=[
            "01-boundaries-and-data-flows.codi",
            "02-nested-boundaries-and-controls.codi",
            "03-auth-webhook-and-queue.codi",
        ],
    ),
    DiagramSkill(
        name="codi-gantt",
        title="CoDi Gantt",
        diagram_type="gantt",
        purpose="Project plans, timelines, milestones, resources, dependencies, lanes, groups, deadlines, and critical path views.",
        choose_when=[
            "You need schedule, dates, durations, resources, milestones, dependencies, and progress.",
            "You need a timeline/table render rather than a node-link graph.",
        ],
        avoid_when=[
            "You need a generic process without calendar semantics; use flowchart or activity.",
        ],
        node_types=["task", "milestone", "group", "lane", "resource"],
        edge_types=["finish-start", "start-start", "finish-finish", "start-finish"],
        diagram_props=[
            ("timeline", "object", "Timeline configuration: scale, today."),
            ("calendar", "object", "Calendar configuration: timezone, work_week, holidays."),
            ("markers", "list", "Timeline markers with date/label/name/color."),
            ("dependencies", "object", "Dependency display configuration."),
            ("critical_path", "boolean/enum", "Critical path display mode."),
        ],
        layout_props=[],
        node_props=[
            ("start", "date/datetime", "Task/group/lane start."),
            ("end", "date/datetime", "Task/group/lane end."),
            ("duration", "duration", "Task duration."),
            ("date", "date/datetime", "Milestone date."),
            ("progress", "0..1, 0..100, or percent", "Task progress."),
            ("resource", "string", "Assigned resource."),
            ("depends_on", "list", "Dependencies of this task/milestone (see Dependency Properties)."),
            ("baseline_start", "date/datetime", "Baseline start."),
            ("baseline_end", "date/datetime", "Baseline end."),
            ("actual_start", "date/datetime", "Actual start."),
            ("actual_end", "date/datetime", "Actual end."),
            ("deadline", "date/datetime", "Deadline marker."),
            ("critical", "boolean", "Marks critical work."),
            ("capacity", "number", "Resource capacity."),
        ],
        edge_props=[
            ("task", "node-ref", "Predecessor task/milestone name (required in the mapping form)."),
            ("type", "finish-start | start-start | finish-finish | start-finish", "Dependency type; defaults to finish-start."),
            ("lag", "duration", "Dependency lag."),
            ("lead", "duration", "Dependency lead."),
        ],
        edge_props_title="Dependency Properties (`depends_on:` entries)",
        grammar_notes=[
            "Use `timeline:` for scale/today configuration.",
            "Use `calendar:` for timezone, work week, and holidays.",
            "Use tasks for date ranges, milestones for single dates, and groups/lanes for organization; group children are plain nested list items.",
            "Dependencies are declared with `depends_on:` on the dependent task or milestone — gantt does NOT use arrow edges.",
            "`depends_on` items are predecessor names, or mappings with `task` plus optional `type`/`lag`/`lead` for typed dependencies.",
            "Scheduling keys are snake_case: `baseline_start`, `actual_end`, `depends_on`.",
        ],
        validation_notes=[
            "Tasks need start and end/duration.",
            "Milestones need date and must have identical start/end semantics.",
            "`depends_on` entries must reference known tasks or milestones and cannot form cycles.",
            "Dates and durations are validated.",
            "Resources referenced by tasks should exist when modeled explicitly.",
        ],
        layout_notes=[
            "Gantt layout is time-based; there are no `layout:` keys for this type. `timeline:` and `calendar:` are semantic directives, not layout.",
            "Renders a Gantt-specific table and timeline payload rather than generic node boxes.",
        ],
        examples=[
            "01-basic-tasks.codi",
            "02-groups-milestones-resources.codi",
            "03-calendars-dependencies-critical-path.codi",
        ],
    ),
    DiagramSkill(
        name="codi-deployment",
        title="CoDi Deployment",
        diagram_type="deployment",
        purpose="infrastructure and runtime deployment topology across clouds, regions, networks, clusters, namespaces, workloads, data stores, routing, and the relationships between them.",
        choose_when=[
            "You need to show where software runs: cloud/region/zone, networks, clusters, namespaces, nodes, and workloads.",
            "You need Kubernetes-style placement (deployments, pods, containers, jobs, cronjobs) and namespace-scoped resources.",
            "You need traffic and placement relationships such as routes-to, connects-to, mounts, uses-secret, and scheduled-on.",
        ],
        avoid_when=[
            "You need logical system/container architecture rather than physical placement; use C4.",
            "You need security data-flow analysis with STRIDE threats; use threat-model.",
        ],
        node_types=[
            "cloud",
            "region",
            "zone",
            "availability-zone",
            "edge-location",
            "network",
            "vpc",
            "subnet",
            "security-group",
            "firewall",
            "private-link",
            "vpn",
            "cluster",
            "namespace",
            "node-pool",
            "node",
            "workload",
            "deployment",
            "statefulset",
            "daemonset",
            "job",
            "cronjob",
            "pod",
            "container",
            "service",
            "ingress",
            "gateway",
            "config-map",
            "secret",
            "volume",
            "persistent-volume",
            "persistent-volume-claim",
            "load-balancer",
            "api-gateway",
            "database",
            "cache",
            "queue",
            "topic",
            "bucket",
            "object-store",
            "function",
            "registry",
            "identity-provider",
            "dns",
            "cdn",
            "external-system",
        ],
        edge_types=[
            "hosts",
            "runs",
            "deploys-to",
            "contains",
            "scheduled-on",
            "routes-to",
            "calls",
            "connects-to",
            "exposes",
            "forwards-to",
            "reads-from",
            "writes-to",
            "publishes-to",
            "subscribes-to",
            "mounts",
            "uses-secret",
            "uses-config",
            "pulls-image-from",
            "allows",
            "denies",
            "terminates-tls",
            "authenticates-with",
        ],
        diagram_props=[],
        layout_props=[*CONTAINER_LAYOUT_PROPS, *SELF_LAYOUT_PROPS],
        node_props=[
            *COMMON_NODE_PROPS,
            ("badge", "string", "Optional compact node badge."),
            ("provider", "aws | azure | gcp | k8s | generic", "Provider hint."),
            ("platform", "kubernetes | vm | serverless | managed", "Runtime platform."),
            ("environment", "string", "Deployment environment such as prod or staging."),
            ("region", "string", "Cloud region."),
            ("zone", "string", "Cloud zone."),
            ("replicas", "number", "Replica count on workload nodes."),
            ("image", "string", "Container image on workload/container nodes."),
            ("version", "string", "Deployed version on workload/container nodes."),
            ("public", "boolean", "Publicly reachable resource."),
            ("encrypted", "boolean", "Encrypted resource (expected on databases)."),
            ("managed", "boolean", "Managed service marker."),
        ],
        edge_props=[
            ("type", "enum", "Deployment relationship type from the edge vocabulary."),
            ("label", "string", "Edge label."),
            ("protocol", "HTTPS | HTTP | TCP | UDP | gRPC | AMQP | Kafka", "Network protocol."),
            ("port", "number", "Network port."),
            ("encrypted", "boolean", "Encrypted traffic marker."),
            ("internal", "boolean", "Internal traffic marker."),
            ("direction", "enum", "Traffic direction."),
            ("links", "list/object", "External links attached to the relationship."),
        ],
        grammar_notes=[
            "Nest physical scope as list items: cloud/region/network/cluster/namespace/workload/pod containers hold their resources as nested children.",
            "A container that also carries properties (provider, platform, replicas, …) writes them as property items (`- provider: aws`) in the same child list.",
            "Use placement edges (`hosts`, `runs`, `deploys-to`, `contains`, `scheduled-on`) for where things run.",
            "Use traffic edges (`routes-to`, `calls`, `connects-to`, `exposes`, `forwards-to`) and data edges (`reads-from`, `writes-to`, `publishes-to`, `subscribes-to`) for runtime interaction.",
            "Mark Kubernetes clusters with `platform: kubernetes`; mark cloud provider with `provider:`.",
        ],
        validation_notes=[
            "Every edge endpoint must reference a declared node, and each node must declare a bracket node type.",
            "Unknown node or edge types fall back to generic rendering and are flagged as warnings.",
            "Kubernetes workloads (deployment, statefulset, daemonset, job, cronjob, pod) must be nested inside a namespace.",
            "Namespace-scoped resources (secret, config-map, persistent-volume-claim) must be nested inside a namespace.",
            "Kubernetes resources should sit inside a cluster whose `platform` is kubernetes.",
            "Workloads should declare `image` or `version`; databases should declare `encrypted: true`.",
            "Provider-specific properties should only appear on nodes of the matching provider.",
        ],
        layout_notes=[
            "Clouds, regions, networks, clusters, and namespaces render as nested containers/swimlanes.",
            "Placement edges are styled differently from traffic edges; public unencrypted traffic is highlighted.",
        ],
        examples=[
            "01-kubernetes-platform.codi",
            "02-cloud-neutral-provider.codi",
            "03-node-types-and-relationships.codi",
        ],
    ),
]


def write(path: Path, contents: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    cleaned = textwrap.dedent(contents).strip()
    lines = [line[8:] if line.startswith("        ") else line for line in cleaned.splitlines()]
    path.write_text("\n".join(lines).strip() + "\n")


def bullets(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def embed(snippet: str) -> str:
    """Indent a multi-line snippet to the 8-space template base so write()
    strips it back uniformly, preserving the snippet's own indentation."""
    lines = snippet.splitlines()
    return "\n".join(
        [lines[0]] + [("        " + line) if line.strip() else line for line in lines[1:]]
    )


def table(rows: list[tuple[str, str, str]], headers=("Name", "Type", "Meaning")) -> str:
    lines = [
        f"| {headers[0]} | {headers[1]} | {headers[2]} |",
        "|---|---|---|",
    ]
    for name, value_type, meaning in rows:
        escaped_type = value_type.replace("|", "\\|")
        lines.append(f"| `{name}` | {escaped_type} | {meaning} |")
    return "\n".join(lines)


def copy_file(src: Path, dst: Path) -> None:
    if not src.exists():
        raise FileNotFoundError(src)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def openai_yaml(display_name: str, short_description: str, default_prompt: str) -> str:
    return f"""
    interface:
      display_name: "{display_name}"
      short_description: "{short_description}"
      default_prompt: "{default_prompt}"
    """


def build_cli_skill(skills_dir: Path) -> None:
    skill = skills_dir / "codi-cli"
    write(
        skill / "SKILL.md",
        """
        ---
        name: codi-cli
        description: Shared CoDi CLI and .codi language workflow. Use when working with CoDi files, installing CoDi diagram skills, checking codi availability, using codi help, validating, rendering, scanning, expanding, diffing, or troubleshooting .codi diagrams. Install this with any codi-* diagram skill.
        ---

        # CoDi CLI

        ## Core Workflow

        CoDi source is YAML with one top-level `DiagramName[diagram-type]` key and a list body. This shared skill covers the common language grammar, CLI commands, validation loop, rendering workflow, and troubleshooting process used by all CoDi diagram skills.

        Older versions of this package installed a single `codi` skill. This package now splits CoDi into `codi-cli` plus diagram-specific skills such as `codi-class`, `codi-sequence`, and `codi-threat-model`.

        ## Availability First

        Before running any CoDi command, confirm the `codi` CLI is reachable in the current shell:

        ```bash
        command -v codi
        # or
        type codi
        # or run the bundled check
        scripts/codi-doctor.sh
        ```

        `command -v codi` succeeds when `codi` is a binary on `PATH`, a shell alias, or a shell function. Note that aliases or functions defined only in an interactive profile may not be loaded in a non-interactive shell.

        If `codi` is not found, treat the CLI as unavailable and stop:

        - Do not invent results. Never hand-write, fake, or generate by other means an SVG, PNG, validation report, diff, or expanded output to stand in for the CLI. There is no fallback renderer or validator.
        - Refuse the validate/render/scan/diff/expand action and tell the user you cannot locate `codi`. It must be installed and available on `PATH`, or exposed as a shell alias or function, before any of these commands can run.
        - You may still author or edit `.codi` source from the references, but state clearly that it was not validated or rendered because the CLI is unavailable.

        ## Required Pairing

        Install this skill with any diagram-specific CoDi skill. Diagram skills assume this shared CLI skill is available.

        ## Command Truth

        Prefer the installed CLI's help before relying on memory:

        ```bash
        codi help
        codi help validate
        codi help render
        codi help scan
        codi help version save
        codi help branch switch
        ```

        If a command fails because of unknown flags, missing arguments, or version drift, run `codi help <command>` and adapt to the installed binary.

        ## Reference Routing

        - CLI commands: `references/cli.md`
        - Common YAML grammar: `references/grammar.md`
        - Validation and diagnostics: `references/validation.md`
        - Rendering, sizing, themes, and PNG/SVG behavior: `references/rendering-and-scaling.md`

        ## Validation Loop

        1. Write or edit `.codi` source using a diagram-specific skill.
        2. Run `codi validate <file>`.
        3. Fix error or critical diagnostics.
        4. Render documentation output with `codi render <file> --format svg -o <file.svg>`.

        Prefer SVG for docs and review. Use PNG only when requested or required by a target system.
        """,
    )
    write(
        skill / "agents" / "openai.yaml",
        openai_yaml(
            "CoDi CLI",
            "Shared CLI workflow for .codi diagrams",
            "Use $codi-cli to validate and render a .codi diagram.",
        ),
    )
    for filename in [
        "cli.md",
        "grammar.md",
        "validation.md",
        "rendering-and-scaling.md",
        "diagram-types.md",
    ]:
        copy_file(ROOT / "references" / filename, skill / "references" / filename)
    copy_file(ROOT / "scripts" / "codi-doctor.sh", skill / "scripts" / "codi-doctor.sh")
    copy_file(
        ROOT / "scripts" / "codi-validate-render.sh",
        skill / "scripts" / "codi-validate-render.sh",
    )


def layout_section(diagram: DiagramSkill) -> str:
    if not diagram.layout_props:
        return (
            "This type is time-based: it has **no** `layout:` keys. "
            "Do not add `direction`, `rank_gap`, or `node_gap` to this diagram type."
        )
    return (
        f"{table(diagram.layout_props)}\n\n"
        "Container-layout keys (direction, gaps, algorithm) apply to the diagram root and to "
        "container nodes, where they arrange children; on a leaf node they warn. "
        "`width`/`height` size the node itself and are valid on any node. "
        "Edges never take `layout:`."
    )


def style_section(diagram: DiagramSkill) -> str:
    rows = [*STYLE_PROPS, *diagram.style_extra]
    return (
        f"{table(rows)}\n\n"
        f"Edges accept `style:` too, with {EDGE_STYLE_KEYS}. "
        "The diagram root takes no `style:`; use the `theme:` directive for global appearance."
    )


def build_diagram_skill(skills_dir: Path, diagram: DiagramSkill) -> None:
    skill = skills_dir / diagram.name
    example_lines = "\n".join(
        f"- `references/examples/{example}`" for example in diagram.examples
    )
    write(
        skill / "SKILL.md",
        f"""
        ---
        name: {diagram.name}
        description: Author, edit, validate, render, and troubleshoot CoDi `{diagram.diagram_type}` diagrams. Use for {diagram.purpose} Assumes the `codi-cli` skill is installed for shared CLI commands, validation, rendering, and common .codi grammar.
        ---

        # {diagram.title}

        ## Requirement

        This skill assumes the `codi-cli` skill is installed. Use `codi-cli` for shared `.codi` grammar, `codi help`, `codi validate`, `codi render`, scan, diff, and diagnostic workflow.

        ## Use This Diagram Type For

        {bullets(diagram.choose_when)}

        ## Avoid This Diagram Type When

        {bullets(diagram.avoid_when)}

        ## Authoring Workflow

        1. Read `references/authoring.md` for diagram selection and common patterns.
        2. Read `references/vocabulary.md` and `references/properties.md` before writing detailed nodes or edges.
        3. Use examples from `references/examples/` as source templates.
        4. Validate with `codi validate <file>`.
        5. Render with `codi render <file> --format svg -o <file.svg>` when the CLI is available.

        ## References

        - Structure and grammar: `references/grammar.md`
        - Node and edge vocabulary: `references/vocabulary.md`
        - Valid properties: `references/properties.md`
        - Validation rules and common repairs: `references/validation.md`
        - Layout and rendering behavior: `references/layout-rendering.md`
        - Examples:
        {example_lines}
        """,
    )
    write(
        skill / "agents" / "openai.yaml",
        openai_yaml(
            diagram.title,
            f"Author CoDi {diagram.diagram_type} diagrams",
            f"Use ${diagram.name} to create a valid CoDi {diagram.diagram_type} diagram.",
        ),
    )
    write(
        skill / "references" / "authoring.md",
        f"""
        # {diagram.title} Authoring Guide

        ## Purpose

        {diagram.purpose}

        ## Choose This Type When

        {bullets(diagram.choose_when)}

        ## Prefer Another Type When

        {bullets(diagram.avoid_when)}

        ## Minimal Shape

        ```yaml
        {embed(DECLARATIONS[diagram.diagram_type])}
        ```

        ## Production Pattern

        - Declare important nodes before edges.
        - Use stable names because CoDi identity is name-based.
        - Add labels on relationships where the validator or reader benefits from intent.
        - Prefer structured properties over overloaded labels when a property exists.
        - Keep layout under `layout:` and colors under `style:`; semantic properties stay top-level.
        - Keep examples valid by running `codi validate`.
        - Use `codi help render` before assuming installed render flags.

        ## Common Mistakes

        - Referencing an undeclared edge endpoint.
        - Mixing a diagram type's vocabulary with a lower-level or unrelated diagram type.
        - Using the removed `children:` keyword. Children are plain nested list items.
        - Using dropped aliases such as `color`, `border`, `tech`, or the bare `style: dashed` scalar.
        - Using a render target as source syntax. Render size belongs on the CLI, not in `.codi`.
        - Relying on stale command flags instead of `codi help <command>`.
        """,
    )
    write(
        skill / "references" / "grammar.md",
        f"""
        # {diagram.title} Grammar

        ## Declaration

        A minimal valid `{diagram.diagram_type}` diagram:

        ```yaml
        {embed(DECLARATIONS[diagram.diagram_type])}
        ```

        ## Shared CoDi Grammar

        All CoDi diagrams are YAML. A file contains exactly one top-level mapping key with a bracketed diagram type. The top-level value is a YAML list. Node types use bracket annotations. Edges use `-->`, `<--`, or `<-->`.

        Every property belongs to one of three buckets: `layout:` (nested map), `style:` (nested map), or semantic keys (bare top-level). Property keys are snake_case; node/edge type names are dash-case. `layout:` and `style:` maps are written in YAML block form only — inline `{{ }}` maps are not supported.

        ## Type-Specific Notes

        {bullets(diagram.grammar_notes)}

        ## Nesting: The Uniform Body Rule

        There is no `children:` keyword. Every body — the diagram body and any container body — is a YAML list, and each item is one of:

        1. A **property item**: a single-key mapping such as `- layout:` (block map), `- style:` (block map), or `- label: "x"`, applied to the owning node.
        2. An **edge**: arrow syntax.
        3. A **child node**: `Name[type]`.
        4. A **member string** (class-like types only).

        A leaf node with only properties uses a plain mapping body instead:

        ```yaml
        - Leaf[type]:
            description: "properties only"
            style:
              fill: "#eef2ff"
        ```

        A container with properties AND children uses the list body with property items:

        ```yaml
        - Parent[type]:
            - layout:
                direction: TB
            - style:
                fill: "#f8fafc"
            - ChildA[type]
            - ChildB[type]
            - ChildA --> ChildB
        ```

        ## Labels and Properties

        A scalar string after a node colon becomes a node description. A scalar string after an edge colon becomes an edge label. Mapping values become structured properties and should be preferred for detailed diagrams.
        """,
    )
    write(
        skill / "references" / "vocabulary.md",
        f"""
        # {diagram.title} Vocabulary

        ## Diagram Type

        Use top-level annotation:

        ```yaml
        Name[{diagram.diagram_type}]:
        ```

        ## Valid Node Types

        {bullets([f'`{item}`' for item in diagram.node_types])}

        ## Valid Edge Types

        {bullets([f'`{item}`' for item in diagram.edge_types])}

        ## Vocabulary Guidance

        Use the vocabulary above exactly unless this document says the type is open/permissive. When the validator is strict for this type, unknown node or edge types can fail validation. Type names are dash-case; property keys are snake_case.
        """,
    )
    write(
        skill / "references" / "properties.md",
        f"""
        # {diagram.title} Properties

        Properties belong to one of three buckets: **layout** (nested under `layout:`), **style** (nested under `style:`), and **semantic** (bare top-level keys). `layout:` and `style:` must be written in YAML block form; inline `{{ }}` maps are not supported. There are no property aliases — one canonical snake_case name per concept.

        ## Layout Properties (`layout:` map)

        {layout_section(diagram)}

        ## Style Properties (`style:` map)

        {style_section(diagram)}

        ## Semantic Properties

        Semantic properties stay top-level next to `layout:`/`style:`.

        ### Diagram Directives

        {table(diagram.diagram_props) if diagram.diagram_props else "No diagram-specific directives. Shared render targets are CLI flags, not source properties."}

        ### Node Properties

        {table(diagram.node_props) if diagram.node_props else "No node-specific semantic properties are required."}

        ### {diagram.edge_props_title}

        {table(diagram.edge_props) if diagram.edge_props else "No edge-specific semantic properties are required."}

        ## Property Rules

        - Canonical names only: `color`, `border`, `border_color`, `border_width`, `text_color`, `tech`, and the bare `style:` scalar are gone. Use `fill`, `stroke`, `stroke_width`, `text`, `technology`, and `line:` inside `style:`.
        - Unknown properties may fail validation on strict diagram types.
        - Use quoted strings for labels or descriptions containing punctuation, colons, dates, or symbols.
        - Prefer explicit booleans (`true`/`false`) for boolean fields.
        - Prefer stable ids where the diagram type supports id-like properties.
        """,
    )
    write(
        skill / "references" / "validation.md",
        f"""
        # {diagram.title} Validation

        ## Main Rules

        {bullets(diagram.validation_notes)}

        ## Repair Loop

        1. Run `codi validate <file>`.
        2. Read each diagnostic code, node, edge, and path.
        3. Fix the source rather than suppressing diagnostics.
        4. Rerun validation.
        5. Render only after error and critical diagnostics are gone.

        ## Strict Mode

        Use `codi validate <file> --strict` when producing best-practice examples or documentation diagrams. Strict mode may promote supported convention warnings.

        ## Common Repairs

        - Add missing node declarations for edge endpoints.
        - Rename duplicate nodes or intentionally nest them where the type supports scope.
        - Replace invalid node/edge types with vocabulary entries from `vocabulary.md`.
        - Replace unsupported properties with entries from `properties.md`; move layout keys under `layout:` and color keys under `style:`.
        - Replace the removed `children:` keyword with plain nested list items.
        - Add relationship labels where the diagram type expects them.
        """,
    )
    write(
        skill / "references" / "layout-rendering.md",
        f"""
        # {diagram.title} Layout and Rendering

        ## Layout Behavior

        {bullets(diagram.layout_notes)}

        ## Render Commands

        ```bash
        codi render diagram.codi --format svg -o diagram.svg
        codi render diagram.codi --theme dark --format svg -o diagram-dark.svg
        codi render diagram.codi --ratio 16:9 --width 1280 --format svg -o diagram-wide.svg
        ```

        ## Guidance

        - Prefer SVG for documentation and review.
        - Use PNG only when explicitly requested or required.
        - Use `--ratio`, `--width`, `--height`, or `--size` as CLI flags; do not put render targets in `.codi` source.
        - Use an explicit `direction` under `layout:` when layout direction matters more than target aspect ratio.
        """,
    )
    for example in diagram.examples:
        copy_file(
            EXAMPLES / diagram.diagram_type / example,
            skill / "references" / "examples" / example,
        )


def build() -> None:
    skills_dir = ROOT / "skills"
    if skills_dir.exists():
        shutil.rmtree(skills_dir)
    skills_dir.mkdir()

    build_cli_skill(skills_dir)
    for diagram in DIAGRAMS:
        build_diagram_skill(skills_dir, diagram)


if __name__ == "__main__":
    build()
