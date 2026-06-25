# CoDi Deployment Properties

## Diagram Properties

| Name | Type | Meaning |
|---|---|---|
| `direction` | TB | LR | RL | BT | Preferred graph direction. |
| `rank_gap` | non-negative number | Space between graph ranks. |
| `node_gap` | non-negative number | Space between sibling nodes. |

## Node Properties

| Name | Type | Meaning |
|---|---|---|
| `description` | string | Short description rendered or used by validators. |
| `label` | string | Display label override. |
| `links` | list/object | External links attached to the node. |
| `refs` | list | Source references or related `.codi` files. |
| `children` | list | Nested resources inside containers such as clouds, networks, clusters, namespaces, and workloads. |
| `badge` | string | Optional compact node badge. |
| `provider` | aws | azure | gcp | k8s | generic | Provider hint. |
| `platform` | kubernetes | vm | serverless | managed | Runtime platform. |
| `environment` | string | Deployment environment such as prod or staging. |
| `region` | string | Cloud region. |
| `zone` | string | Cloud zone. |
| `replicas` | number | Replica count on workload nodes. |
| `image` | string | Container image on workload/container nodes. |
| `version` | string | Deployed version on workload/container nodes. |
| `public` | boolean | Publicly reachable resource. |
| `encrypted` | boolean | Encrypted resource (expected on databases). |
| `managed` | boolean | Managed service marker. |

## Edge Properties

| Name | Type | Meaning |
|---|---|---|
| `type` | enum | Deployment relationship type from the edge vocabulary. |
| `label` | string | Edge label. |
| `protocol` | HTTPS | HTTP | TCP | UDP | gRPC | AMQP | Kafka | Network protocol. |
| `port` | number | Network port. |
| `encrypted` | boolean | Encrypted traffic marker. |
| `internal` | boolean | Internal traffic marker. |
| `direction` | enum | Traffic direction. |
| `links` | list/object | External links attached to the relationship. |

## Property Rules

- Unknown properties may fail validation on strict diagram types.
- Use quoted strings for labels or descriptions containing punctuation, colons, dates, or symbols.
- Prefer explicit booleans (`true`/`false`) for boolean fields.
- Prefer stable ids where the diagram type supports id-like properties.
