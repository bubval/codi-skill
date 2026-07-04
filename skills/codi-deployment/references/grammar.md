# CoDi Deployment Grammar

## Declaration

A minimal valid `deployment` diagram:

```yaml
Production[deployment]:
  - AppCluster[cluster]:
      - platform: kubernetes
      - WebNamespace[namespace]:
          - Web[deployment]:
              image: "registry/web:1.0.0"
  - Internet[external-system]: "Public traffic"
  - Internet --> Web:
      type: routes-to
      protocol: HTTPS
      encrypted: true
```

## Shared CoDi Grammar

All CoDi diagrams are YAML. A file contains exactly one top-level mapping key with a bracketed diagram type. The top-level value is a YAML list. Node types use bracket annotations. Edges use `-->`, `<--`, or `<-->`.

Every property belongs to one of three buckets: `layout:` (nested map), `style:` (nested map), or semantic keys (bare top-level). Property keys are snake_case; node/edge type names are dash-case. `layout:` and `style:` maps are written in YAML block form only — inline `{ }` maps are not supported.

## Type-Specific Notes

- Nest physical scope as list items: cloud/region/network/cluster/namespace/workload/pod containers hold their resources as nested children.
- A container that also carries properties (provider, platform, replicas, …) writes them as property items (`- provider: aws`) in the same child list.
- Use placement edges (`hosts`, `runs`, `deploys-to`, `contains`, `scheduled-on`) for where things run.
- Use traffic edges (`routes-to`, `calls`, `connects-to`, `exposes`, `forwards-to`) and data edges (`reads-from`, `writes-to`, `publishes-to`, `subscribes-to`) for runtime interaction.
- Mark Kubernetes clusters with `platform: kubernetes`; mark cloud provider with `provider:`.

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
