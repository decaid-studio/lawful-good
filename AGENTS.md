# AGENTS.md – using lawful-good as an agent

This repository holds governance recommendations as data. Use them to structure checks
and questions. Do not present results as legal compliance.

## Load

Prefer `dist/lawful-good.json` (built by `python tools/lg.py build`); otherwise read the
YAML files under `catalog/`.

## Data model

- `frameworks[].levels[]` – clearance levels with `capabilities` (upper bound of what an
  agent may do), `approval_roles` and derived `mandatory_controls`.
- `frameworks[].controls[]` – `statement` (the recommendation), `parameters` (thresholds),
  `assessment_questions` (what to check), `implementation_examples` (illustrative only).
- `assessment_catalogs[].items[]` – check questions per gate with maturity criteria
  (`basic`, `advanced`, `high`), expected `evidence`, `methods` and
  `reassessment_triggers`. Items with a `module` apply only if the module's `applies_if`
  holds. Apply the catalog's `principles`.
- `crosswalks[]` – links check items to agent controls (`relation: supports`).
- `templates/` – a human-readable AI policy; the `→ DAG-…` and `→ G…` markers point to the
  data above.

## Typical task: watch for reassessment triggers

Compare a change (pull request, config diff, model or provider switch) with the
`reassessment_triggers` of every item and report which items are due for a new assessment.

## Typical task: review an agent configuration

1. Derive the agent's level from its actual capabilities: the lowest level whose
   `capabilities` cover what the agent can read, write and call. An agent that can act
   autonomously without any way to abort it is `prohibited`.
2. For every id in that level's `mandatory_controls`, answer each `assessment_question`
   with evidence from what you inspected.
3. Report per control: met / not met / not determinable, with evidence (file and line).
4. Hand judgement calls to a human. Flag them instead of deciding them.

## Rules

- Never state that a system "complies" with the EU AI Act or any standard.
- Do not invent thresholds, levels or controls that are not in the data.
- Flag content whose `verification.status` is `unverified` or whose
  `translation_status` is `machine-assisted-review-needed`.
