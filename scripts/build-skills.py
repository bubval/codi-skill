#!/usr/bin/env python3
"""Build the public CoDi multi-skill package.

This script is for repository maintainers. It generates the selectable
`skills/<name>` folders consumed by `npx skills add`.
"""

from __future__ import annotations

import shutil
import textwrap
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent
DOCS = WORKSPACE / "codi-docs"
DIAGRAM_DOCS = DOCS / "language" / "diagrams"
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


COMMON_NODE_PROPS = [
    ("description", "string", "Short description rendered or used by validators."),
    ("label", "string", "Display label override."),
    ("links", "list/object", "External links attached to the node."),
    ("refs", "list", "Source references or related `.codi` files."),
]

RENDER_NODE_PROPS = [
    ("shape", "string", "Renderer shape override where supported."),
    ("width", "positive number", "Node width in layout units."),
    ("height", "positive number", "Node height in layout units."),
    ("fill", "color string", "Node fill color."),
    ("stroke", "color string", "Node stroke color."),
    ("border", "color string", "Border color alias."),
    ("text", "color string", "Text color."),
    ("border_width", "number", "Border width."),
    ("stroke_width", "number", "Stroke width."),
]

LAYOUT_PROPS = [
    ("direction", "TB | LR | RL | BT", "Preferred graph direction."),
    ("rank_gap", "non-negative number", "Space between graph ranks."),
    ("node_gap", "non-negative number", "Space between sibling nodes."),
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
    ("tech", "string", "Short alias for `technology`."),
    ("protocol", "string", "Protocol used by the relationship."),
    ("transport", "string", "Transport used by the relationship."),
    ("links", "list/object", "External links attached to the relationship."),
]


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
            "Fragments use `alt`, `else`, `opt`, `loop`, `par`, and `ref` list items.",
        ],
        validation_notes=[
            "Every message endpoint must be a declared lifeline unless the directive explicitly models found/lost messages.",
            "Duplicate lifeline names are rejected.",
            "Replies should match a prior call where possible.",
            "Messages after a destroyed lifeline are invalid.",
        ],
        layout_notes=[
            "Lifelines are laid out horizontally in declaration order.",
            "Messages, fragments, notes, activation, and destruction events are laid out vertically in source order.",
            "Render target aspect ratio pads the output but does not change event order.",
        ],
        examples=[
            "sequence-auth-login.codi",
            "sequence-lifecycle-fragments.codi",
            "sequence-notes-replies.codi",
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
        diagram_props=[
            ("algorithm", "organic | force | force-directed | fdg", "Layout algorithm."),
            *LAYOUT_PROPS,
        ],
        node_props=[
            *COMMON_NODE_PROPS,
            *RENDER_NODE_PROPS,
            ("algorithm", "organic | force", "Nested layout algorithm."),
            ("direction", "TB | LR | RL | BT", "Nested layout direction."),
            ("children", "list", "Nested child nodes and edges."),
            ("icon", "string", "Renderer icon name."),
            ("style", "string", "Visual style such as dashed."),
            ("opacity", "number", "Node opacity."),
        ],
        edge_props=[
            ("label", "string", "Relationship label."),
            ("style", "string", "Edge style such as dashed."),
            ("stroke", "color string", "Edge color."),
            ("stroke_width", "number", "Edge width."),
            ("dash", "list[number]", "Custom dash pattern."),
            ("opacity", "number", "Edge opacity."),
            ("links", "list/object", "External links attached to the edge."),
        ],
        grammar_notes=[
            "Use any readable node type: `API[service]`, `Queue[queue]`, `Team[team]`.",
            "Use `children:` to model groups.",
            "Avoid the old `group:` property; nested children are the supported grouping model.",
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
            "unstructured-service-map.codi",
            "unstructured-incident-map.codi",
            "unstructured-dependency-web.codi",
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
        diagram_props=LAYOUT_PROPS,
        node_props=[
            *COMMON_NODE_PROPS,
            *RENDER_NODE_PROPS,
            ("children", "list", "Nested child nodes and edges."),
            ("direction", "TB | LR | RL | BT", "Nested group direction."),
            ("rank_gap", "non-negative number", "Nested rank gap."),
            ("node_gap", "non-negative number", "Nested node gap."),
            ("layout_only", "boolean", "Marks a layout helper/group."),
        ],
        edge_props=[
            ("label", "string", "Branch or flow label."),
            ("style", "string", "Visual edge style."),
            ("stroke", "color string", "Edge color."),
            ("stroke_width", "number", "Edge width."),
            ("links", "list/object", "External links attached to the edge."),
        ],
        grammar_notes=[
            "Use readable domain-specific node types, for example `Review[decision]` or `Deploy[process]`.",
            "Use `children:` for nested process groups.",
            "Use labels on decision outgoing edges for branch meaning.",
        ],
        validation_notes=[
            "Duplicate node names and duplicate edges are flagged.",
            "Direction must be one of `LR`, `RL`, `TB`, or `BT`.",
            "Numeric layout props must be non-negative.",
            "`layout_only` nodes should have children.",
        ],
        layout_notes=[
            "Uses directed graph layout and supports nested containers.",
            "Explicit `direction` wins over render target direction hints.",
        ],
        examples=[
            "flowchart-release-gate.codi",
            "flowchart-error-handling.codi",
            "flowchart-nested-process.codi",
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
        diagram_props=LAYOUT_PROPS,
        node_props=[
            *COMMON_NODE_PROPS,
            *RENDER_NODE_PROPS,
            ("children", "list", "Nested actions inside swimlanes or regions."),
            ("lane", "node-ref", "Swimlane/partition containing this node."),
            ("operation", "string", "Required by call-operation-action."),
            ("behavior", "string", "Required by call-behavior-action."),
            ("signal", "string", "Required by accept-event-action and send-signal-action."),
            ("guard", "string", "Guard expression where applicable."),
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
            "Swimlanes are container nodes using `children:`.",
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
            "activity-approval-workflow.codi",
            "activity-object-flow.codi",
            "activity-swimlane-handoff.codi",
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
        diagram_props=LAYOUT_PROPS,
        node_props=[
            ("label", "string", "Display label."),
            ("width", "positive number", "Rendered width."),
            ("height", "positive number", "Rendered height."),
            ("entry-action", "string", "Entry behavior."),
            ("do-activity", "string", "Ongoing state activity."),
            ("exit-action", "string", "Exit behavior."),
            ("internal-transitions", "list", "Internal transition objects with trigger/guard/action."),
            ("deferred", "list[string]", "Deferred events."),
            ("regions", "mapping", "Composite state regions."),
            ("children", "list", "Nested state children where supported."),
            ("type", "shallow | deep", "History pseudostate kind."),
            *LAYOUT_PROPS,
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
            "Use `regions:` on composite states to model orthogonal regions.",
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
            "state-machine-order.codi",
            "state-machine-composite.codi",
            "state-machine-regions.codi",
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
        diagram_props=LAYOUT_PROPS,
        node_props=[
            *COMMON_NODE_PROPS,
            ("members", "list[string]", "Class/interface/enum members."),
            ("children", "list", "Nested package contents."),
            ("stereotype", "string", "UML stereotype."),
            ("stereotypes", "list[string]", "Multiple UML stereotypes."),
            ("templateParameters", "list", "Generic/template parameters."),
            ("language", "string", "Source language hint."),
        ],
        edge_props=[
            ("type", "enum", "Relationship type."),
            ("label", "string", "Relationship label."),
            ("sourceRole", "string", "Association source role."),
            ("targetRole", "string", "Association target role."),
            ("sourceMultiplicity", "string", "Source multiplicity."),
            ("targetMultiplicity", "string", "Target multiplicity."),
            ("navigable", "boolean", "Whether association is navigable."),
            ("links", "list/object", "External links attached to the relationship."),
        ],
        grammar_notes=[
            "Members can be declared as `members:` or as a direct string list under a class/interface/enum.",
            "Package nodes can contain nested classes, interfaces, enums, packages, and relationships.",
            "Member visibility commonly uses `+`, `-`, `#`, or `~`.",
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
            "class-domain-model.codi",
            "class-association-details.codi",
            "class-interface-contracts.codi",
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
        diagram_props=LAYOUT_PROPS,
        node_props=[
            *COMMON_NODE_PROPS,
            ("children", "list", "Nested software systems inside a boundary."),
            ("external", "boolean/annotation", "Marks an element external."),
            ("scope", "boolean/annotation", "Marks the software system in scope."),
        ],
        edge_props=C4_EDGE_PROPS,
        grammar_notes=[
            "Mark exactly one software system as in scope using `[software-system, scope]` or `scope: true`.",
            "Boundaries may group software systems or nested boundaries.",
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
            "c4-context-retail-platform.codi",
            "c4-context-healthcare-portal.codi",
            "c4-context-iot-fleet.codi",
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
        diagram_props=LAYOUT_PROPS,
        node_props=[
            *COMMON_NODE_PROPS,
            ("children", "list", "Containers nested inside a scoped system boundary."),
            ("technology", "string", "Container technology."),
            ("tech", "string", "Technology alias."),
            ("external", "boolean/annotation", "Marks element external."),
            ("scope", "boolean/annotation", "Marks scoped system boundary or system."),
        ],
        edge_props=C4_EDGE_PROPS,
        grammar_notes=[
            "Place containers inside a scoped `system-boundary` where possible.",
            "Use `database` or `data-store` for storage containers.",
        ],
        validation_notes=[
            "Containers should be inside the scoped system boundary.",
            "Container-to-container relationships should declare protocol, technology, tech, or transport.",
            "Strict mode requires explicit scope.",
        ],
        layout_notes=["Uses C4 boundary-aware graph layout and target-aware direction hints."],
        examples=[
            "c4-container-saas-analytics.codi",
            "c4-container-retail-checkout.codi",
            "c4-container-open-banking.codi",
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
        diagram_props=LAYOUT_PROPS,
        node_props=[
            *COMMON_NODE_PROPS,
            ("children", "list", "Components nested inside a container boundary."),
            ("technology", "string", "Component technology."),
            ("tech", "string", "Technology alias."),
            ("external", "boolean/annotation", "Marks element external."),
            ("scope", "boolean/annotation", "Marks scoped container."),
        ],
        edge_props=C4_EDGE_PROPS,
        grammar_notes=[
            "Mark the scoped container and nest components in a `container-boundary`.",
            "Keep supporting systems and containers outside the scoped boundary unless they are the scoped container.",
        ],
        validation_notes=[
            "Components should sit inside the scoped container boundary.",
            "Crossing relationships to containers or systems should declare protocol, technology, tech, or transport.",
        ],
        layout_notes=["Uses C4 boundary-aware graph layout and target-aware direction hints."],
        examples=[
            "c4-component-payment-service.codi",
            "c4-component-notification-service.codi",
            "c4-component-ingestion-service.codi",
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
        diagram_props=LAYOUT_PROPS,
        node_props=[
            *COMMON_NODE_PROPS,
            ("children", "list", "Nested package/component-boundary contents."),
            ("members", "list[string]", "Members in class-like elements."),
            ("technology", "string", "Technology for supporting nodes."),
            ("scope", "boolean/annotation", "Marks scoped component."),
        ],
        edge_props=C4_EDGE_PROPS,
        grammar_notes=[
            "Use a scoped component and code/package boundaries to organize internals.",
            "Class-like members use the same string member convention as class diagrams.",
        ],
        validation_notes=[
            "Structural relationships are type-checked.",
            "`implements` must target an interface or trait.",
            "Code elements should be inside the scoped component or package boundary.",
        ],
        layout_notes=["Uses class/code element layout with target-aware compact packing."],
        examples=[
            "c4-code-payment-module.codi",
            "c4-code-event-handler.codi",
            "c4-code-repository-layer.codi",
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
        node_props=[
            *COMMON_NODE_PROPS,
            ("children", "list", "Nested elements inside a trust boundary."),
            ("threats", "list", "Threats scoped to this element."),
            ("trust-level", "string", "Trust level for external entities."),
            ("technology", "string", "Technology for processes."),
            ("privilege-level", "string", "Privilege level for processes."),
            ("controls", "list[string]", "Security controls."),
            ("encrypted", "boolean", "Encryption status for data stores."),
            ("data-classification", "public | internal | confidential | restricted | pii | phi | pci | secret", "Data sensitivity."),
        ],
        edge_props=[
            ("label", "string", "Data flow label."),
            ("type", "data-flow", "Explicit data flow type."),
            ("encrypted", "boolean", "Whether the flow is encrypted."),
            ("authenticated", "boolean", "Whether the flow is authenticated."),
            ("protocol", "string", "Protocol used by the data flow."),
            ("data", "string", "Data carried by the flow."),
            ("data-classification", "enum", "Sensitivity of data in transit."),
            ("flow-id", "string", "Stable id for targeting threats."),
            ("id", "string", "Alias for flow-id."),
            ("threats", "list", "Threats scoped to this flow."),
            ("bidirectional", "boolean", "Whether the flow is bidirectional."),
        ],
        grammar_notes=[
            "Use trust boundaries as containers.",
            "Use `threats:` on nodes, edges, or at the top level.",
            "Top-level threats can target elements or flows by element name, source/target, or flow id.",
        ],
        validation_notes=[
            "Valid STRIDE categories: spoofing, tampering, repudiation, information-disclosure, denial-of-service, elevation-of-privilege.",
            "Valid severities: low, medium, high, critical.",
            "Valid statuses: open, mitigated, accepted.",
            "Cross-boundary flows should declare encryption and protocol/label.",
            "Sensitive data stores should declare `encrypted: true`.",
            "Elevated processes should declare controls.",
        ],
        layout_notes=["Uses trust-boundary/data-flow layout and boundary-aware packing."],
        examples=[
            "threat-model-file-upload.codi",
            "threat-model-oidc-flow.codi",
            "threat-model-ci-cd.codi",
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
        edge_types=["finish-start", "start-start", "finish-finish", "start-finish", "soft-link"],
        diagram_props=[
            ("timeline", "object", "Timeline configuration: scale, today."),
            ("calendar", "object", "Calendar configuration: timezone, work_week, holidays."),
            ("markers", "list", "Timeline markers with date/label/name/color."),
            ("dependencies", "object", "Dependency display configuration."),
        ],
        node_props=[
            ("start", "date/datetime", "Task/group/lane start."),
            ("end", "date/datetime", "Task/group/lane end."),
            ("finish", "date/datetime", "Alias for end."),
            ("duration", "duration", "Task duration."),
            ("date", "date/datetime", "Milestone date."),
            ("progress", "0..1, 0..100, or percent", "Task progress."),
            ("resource", "string", "Single resource."),
            ("resources", "list[string]", "Multiple resources."),
            ("baseline-start", "date/datetime", "Baseline start."),
            ("baseline-end", "date/datetime", "Baseline end."),
            ("deadline", "date/datetime", "Deadline marker."),
            ("critical", "boolean", "Marks critical work."),
            ("capacity", "number", "Resource capacity."),
            ("children", "list", "Nested tasks/milestones in groups or lanes."),
        ],
        edge_props=[
            ("type", "finish-start | start-start | finish-finish | start-finish | soft-link", "Dependency type."),
            ("lag", "duration", "Dependency lag."),
            ("lead", "duration", "Dependency lead."),
            ("required", "boolean", "Required dependency."),
            ("critical", "boolean", "Critical dependency."),
            ("label", "string", "Dependency label."),
        ],
        grammar_notes=[
            "Use `timeline:` for scale/today configuration.",
            "Use `calendar:` for timezone, work week, and holidays.",
            "Use tasks for date ranges, milestones for single dates, and groups/lanes for organization.",
            "Dependencies are edges between task-like nodes.",
        ],
        validation_notes=[
            "Tasks need start and end/finish/duration.",
            "Milestones need date and must have identical start/end semantics.",
            "Dependencies must reference known endpoints and cannot form cycles.",
            "Dates and durations are validated.",
            "Resources referenced by tasks should exist when modeled explicitly.",
        ],
        layout_notes=["Renders a Gantt-specific table and timeline payload rather than generic node boxes."],
        examples=[
            "gantt-product-launch.codi",
            "gantt-resource-plan.codi",
            "gantt-critical-path.codi",
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


def table(rows: list[tuple[str, str, str]], headers=("Name", "Type", "Meaning")) -> str:
    lines = [
        f"| {headers[0]} | {headers[1]} | {headers[2]} |",
        "|---|---|---|",
    ]
    for name, value_type, meaning in rows:
        lines.append(f"| `{name}` | {value_type} | {meaning} |")
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
    for filename in ["cli.md", "grammar.md", "validation.md", "rendering-and-scaling.md"]:
        copy_file(ROOT / "references" / filename, skill / "references" / filename)
    copy_file(ROOT / "scripts" / "codi-doctor.sh", skill / "scripts" / "codi-doctor.sh")
    copy_file(
        ROOT / "scripts" / "codi-validate-render.sh",
        skill / "scripts" / "codi-validate-render.sh",
    )


def build_diagram_skill(skills_dir: Path, diagram: DiagramSkill) -> None:
    skill = skills_dir / diagram.name
    example_lines = "\n".join(
        f"- `references/examples/{index:02d}-{example}`"
        for index, example in enumerate(diagram.examples, start=1)
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
        Example[{diagram.diagram_type}]:
          - FirstNode[{diagram.node_types[0].split(';')[0]}]
        ```

        ## Production Pattern

        - Declare important nodes before edges.
        - Use stable names because CoDi identity is name-based.
        - Add labels on relationships where the validator or reader benefits from intent.
        - Prefer structured properties over overloaded labels when a property exists.
        - Keep examples valid by running `codi validate`.
        - Use `codi help render` before assuming installed render flags.

        ## Common Mistakes

        - Referencing an undeclared edge endpoint.
        - Mixing a diagram type's vocabulary with a lower-level or unrelated diagram type.
        - Using a render target as source syntax. Render size belongs on the CLI, not in `.codi`.
        - Relying on stale command flags instead of `codi help <command>`.
        """,
    )
    write(
        skill / "references" / "grammar.md",
        f"""
        # {diagram.title} Grammar

        ## Declaration

        ```yaml
        DiagramName[{diagram.diagram_type}]:
          - NodeName[type]
          - NodeName --> OtherNode: "relationship label"
        ```

        ## Shared CoDi Grammar

        All CoDi diagrams are YAML. A file contains exactly one top-level mapping key with a bracketed diagram type. The top-level value is a YAML list. Node types use bracket annotations. Edges use `-->`, `<--`, or `<-->`.

        ## Type-Specific Notes

        {bullets(diagram.grammar_notes)}

        ## Nesting

        Use `children:` for nested structures when this diagram type supports containers, boundaries, packages, regions, lanes, groups, or swimlanes. Direct nested YAML sequences are accepted for some class-like/member patterns when examples show that form.

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

        Use the vocabulary above exactly unless this document says the type is open/permissive. When the validator is strict for this type, unknown node or edge types can fail validation.
        """,
    )
    write(
        skill / "references" / "properties.md",
        f"""
        # {diagram.title} Properties

        ## Diagram Properties

        {table(diagram.diagram_props) if diagram.diagram_props else "No diagram-specific properties are required. Shared render targets are CLI flags, not source properties."}

        ## Node Properties

        {table(diagram.node_props) if diagram.node_props else "No node-specific properties are required."}

        ## Edge Properties

        {table(diagram.edge_props) if diagram.edge_props else "No edge-specific properties are required."}

        ## Property Rules

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
        - Replace unsupported properties with entries from `properties.md`.
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
        - Use explicit source `direction` when layout direction matters more than target aspect ratio.
        """,
    )
    for index, example in enumerate(diagram.examples, start=1):
        copy_file(EXAMPLES / example, skill / "references" / "examples" / f"{index:02d}-{example}")


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
