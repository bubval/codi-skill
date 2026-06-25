# CoDi Deployment Authoring Guide

## Purpose

infrastructure and runtime deployment topology across clouds, regions, networks, clusters, namespaces, workloads, data stores, routing, and the relationships between them.

## Choose This Type When

- You need to show where software runs: cloud/region/zone, networks, clusters, namespaces, nodes, and workloads.
- You need Kubernetes-style placement (deployments, pods, containers, jobs, cronjobs) and namespace-scoped resources.
- You need traffic and placement relationships such as routes-to, connects-to, mounts, uses-secret, and scheduled-on.

## Prefer Another Type When

- You need logical system/container architecture rather than physical placement; use C4.
- You need security data-flow analysis with STRIDE threats; use threat-model.

## Minimal Shape

```yaml
Example[deployment]:
  - FirstNode[cloud]
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
