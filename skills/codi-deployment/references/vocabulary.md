# CoDi Deployment Vocabulary

## Diagram Type

Use top-level annotation:

```yaml
Name[deployment]:
```

## Valid Node Types

- `cloud`
- `region`
- `zone`
- `availability-zone`
- `edge-location`
- `network`
- `vpc`
- `subnet`
- `security-group`
- `firewall`
- `private-link`
- `vpn`
- `cluster`
- `namespace`
- `node-pool`
- `node`
- `workload`
- `deployment`
- `statefulset`
- `daemonset`
- `job`
- `cronjob`
- `pod`
- `container`
- `service`
- `ingress`
- `gateway`
- `config-map`
- `secret`
- `volume`
- `persistent-volume`
- `persistent-volume-claim`
- `load-balancer`
- `api-gateway`
- `database`
- `cache`
- `queue`
- `topic`
- `bucket`
- `object-store`
- `function`
- `registry`
- `identity-provider`
- `dns`
- `cdn`
- `external-system`

## Valid Edge Types

- `hosts`
- `runs`
- `deploys-to`
- `contains`
- `scheduled-on`
- `routes-to`
- `calls`
- `connects-to`
- `exposes`
- `forwards-to`
- `reads-from`
- `writes-to`
- `publishes-to`
- `subscribes-to`
- `mounts`
- `uses-secret`
- `uses-config`
- `pulls-image-from`
- `allows`
- `denies`
- `terminates-tls`
- `authenticates-with`

## Vocabulary Guidance

Use the vocabulary above exactly unless this document says the type is open/permissive. When the validator is strict for this type, unknown node or edge types can fail validation. Type names are dash-case; property keys are snake_case.
