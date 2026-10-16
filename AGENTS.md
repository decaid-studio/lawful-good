# AGENTS.md – using lawful-good as an agent

This repository is designed to be read by coding agents and governance tools.

## Load

Prefer the bundle `dist/lawful-good.json` (built by `python tools/lg.py build`).
Otherwise read the YAML files under `catalog/` and `crosswalks/` directly.
Never read or use files under `drafts/` or `private/` unless explicitly told to.

## Data model in one minute

- `regulations[].requirements[]` – legal text (`text.de`, `text.en`), editorial `summary`
  and `assessment_questions`. Treat `text` as authoritative wording, everything else as help.
- `frameworks[].levels[]` – clearance levels with `capabilities` (upper bound of what an agent
  may do), `approval_roles` and derived `mandatory_controls`.
- `frameworks[].controls[]` – `statement` (normative), `parameters` (thresholds),
  `assessment_questions` (what to check), `implementation_examples` (informative only).
- `crosswalks[].mappings[]` – `relation: supports` means *contributes to*, never *fulfils*.

## Typical task: assess an agent configuration

1. Determine the agent's level from its actual capabilities: pick the lowest level whose
   `capabilities` cover what the agent can do (read scope, write scope, external tools).
   If the agent can act autonomously without any abort mechanism, it is `prohibited`.
2. For every id in that level's `mandatory_controls`, answer each `assessment_question`
   with evidence from the repository or configuration you inspected.
3. Report per control: `status` (met / not met / not determinable), evidence (file and line),
   and the related AI Act requirements from the crosswalk.
4. Never state that a system "complies with the AI Act". State which controls are evidenced.

## Rules for agents

- Do not invent requirements, thresholds or clause numbers that are not in the data.
- Quote legal text only from `text` fields and cite the `ref` (e.g. "Art. 17(1)(h)").
- Flag content whose `verification.status` is `unverified`.
