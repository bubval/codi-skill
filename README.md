# CoDi Skills

Selectable Codex skills for authoring, validating, and rendering `.codi` architecture diagrams.

## Install

List the available skills:

```bash
npx skills add bubval/codi-skill --list
```

Install the shared CLI skill plus one diagram skill:

```bash
npx skills add bubval/codi-skill -a codex --skill codi-cli --skill codi-class
```

Install every CoDi skill:

```bash
npx skills add bubval/codi-skill -a codex --skill '*'
```

## Skill Layout

`codi-cli` is the shared skill for `codi help`, validation, rendering, scanning, and common `.codi` grammar.

Diagram skills are optional and should be installed with `codi-cli`:

- `codi-sequence`
- `codi-unstructured`
- `codi-flowchart`
- `codi-activity`
- `codi-state-machine`
- `codi-class`
- `codi-c4-context`
- `codi-c4-container`
- `codi-c4-component`
- `codi-c4-code`
- `codi-threat-model`
- `codi-gantt`

Each diagram skill includes its own grammar notes, vocabulary, valid properties, validation guidance, layout/rendering notes, and valid examples.

## Maintenance

Regenerate the skill folders from the local CoDi docs and checked-in shared references:

```bash
python3 scripts/build-skills.py
```
