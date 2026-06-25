# CoDi Deployment Validation

## Main Rules

- Every edge endpoint must reference a declared node, and each node must declare a bracket node type.
- Unknown node or edge types fall back to generic rendering and are flagged as warnings.
- Kubernetes workloads (deployment, statefulset, daemonset, job, cronjob, pod) must be nested inside a namespace.
- Namespace-scoped resources (secret, config-map, persistent-volume-claim) must be nested inside a namespace.
- Kubernetes resources should sit inside a cluster whose `platform` is kubernetes.
- Workloads should declare `image` or `version`; databases should declare `encrypted: true`.
- Provider-specific properties should only appear on nodes of the matching provider.

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
