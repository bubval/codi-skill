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
