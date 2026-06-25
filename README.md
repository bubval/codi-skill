# CoDi Skills

Selectable agent skills for authoring, validating, and rendering `.codi` architecture diagrams.

Each skill follows the standard Agent Skills format (a `SKILL.md` with `name`/`description` frontmatter plus `references/` and `scripts/`), so it works with both Codex and Claude. The only agent-specific piece is the `agents/openai.yaml` adapter; Claude reads `SKILL.md` directly and ignores it.

## Install

List the available skills:

```bash
npx skills add bubval/codi-skill --list
```

### Codex

Install the shared CLI skill plus one diagram skill:

```bash
npx skills add bubval/codi-skill -a codex --skill codi-cli --skill codi-class
```

Install every CoDi skill:

```bash
npx skills add bubval/codi-skill -a codex --skill '*'
```

### Claude

If your `skills` CLI supports a Claude target, use the same commands with `-a claude`:

```bash
npx skills add bubval/codi-skill -a claude --skill codi-cli --skill codi-class
```

Or install natively for Claude Code by copying the skill folders into a skills
directory — `~/.claude/skills/` for personal use, or `.claude/skills/` inside a
project. Each skill is self-contained under its own folder:

```bash
mkdir -p ~/.claude/skills
cp -r skills/codi-cli skills/codi-class ~/.claude/skills/
```

Always install `codi-cli` alongside any diagram skill. The CoDi CLI must be on
`PATH` (or available as a shell alias/function) for validation and rendering;
the skills do not fabricate output without it.

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
- `codi-deployment`

Each diagram skill includes its own grammar notes, vocabulary, valid properties, validation guidance, layout/rendering notes, and valid examples.

## Maintenance

Regenerate the skill folders from the local CoDi docs and checked-in shared references:

```bash
python3 scripts/build-skills.py
```
