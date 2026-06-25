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
