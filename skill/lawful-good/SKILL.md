---
name: lawful-good
description: >-
  Pre-assess an AI system or AI agent that an organisation wants to run, using DECAID's open
  governance rulebook lawful-good: EU AI Act triage with a record for the AI register, clearance
  level and mandatory controls for an agent, check items per gate, and reassessment triggers after
  a change. Use when someone brings a new AI use case, asks whether the AI Act applies or whether a
  case needs legal review, wants an agent configuration reviewed, or asks whether a change (model,
  provider, purpose, permissions) calls for a new assessment. Triggers: "AI use case", "AI Act
  triage", "AI register", "agent clearance level", "agent governance", "reassessment",
  "KI-Anwendungsfall", "KI-Use-Case prüfen", "Vorprüfung AI Act", "KI-Register", "Agent
  einstufen", "Agenten-Governance", "Reassessment". Not for: legal advice, proof of conformity,
  high-risk AI systems, scoring or approval of a system.
---

# lawful-good

Governance recommendations as data. You gather facts, ask the questions and report with evidence.
People decide. The script holds the rules that are not yours to bend.

## Rules

- Never state that a system complies with the EU AI Act or any law or standard. This is governance,
  not compliance, and not legal advice.
- Never invent a question, threshold, level or control. If it is not in the script output, it does
  not exist.
- If the facts you have do not answer a triage question, the answer is `unclear`. Never guess. Ask
  the person first if they can know it.
- After a stop outcome you do not continue. A person decides after legal review.
- Every output carries `notices`. Repeat them to the person in your report: they say which content
  is unverified or machine-translated.
- Say "Gate G2", never just "G2".
- Answer in the person's language and pass `--lang de` or `--lang en` (default `de`) before the
  command.

## The script

All content comes from one script. It prints JSON in one language. Run it from the skill folder:

```bash
python scripts/lawful_good.py triage [node=answer[=justification] ...]
python scripts/lawful_good.py levels
python scripts/lawful_good.py controls <level-id>
python scripts/lawful_good.py gate <gate-id> [--module <module-id>]
python scripts/lawful_good.py triggers
```

Do not read `data/lawful-good.json` directly. It is large and bilingual; the script returns the
part you need.

## Task 1: pre-assess a new use case

1. Collect what is known: the system and version, purpose, user groups, who provides and who
   operates it.
2. Run `triage` with no answers. It returns the first question with its legal references, a help
   text and the allowed answers.
3. Answer from the facts, with a one-sentence justification that names the fact:
   `triage "ai-system=yes=LLM-based assistant that drafts replies"`. Run it again with all answers
   so far; it returns the next question. The script refuses skipped or made-up answers.
4. Repeat until `status` is `outcome`. Then act on `outcome.type`:
   - `stop`: report the outcome and hand over to a person for legal review. Do not open the
     catalog.
   - `out-of-scope`: report the result and the reason.
   - `continue`: go on with the check items, and carry the `flags` along.
5. Whatever the outcome, give the person the `record` for the AI register. Fill `system`,
   `use-case` and `assessed-by`. Leave `approved-by` empty: a person approves the classification.
6. Report the `parallel_checks` with every outcome. The triage covers the AI Act only.

Check items after `continue`: run `gate G0`, then the following gates one at a time. For each item
report what you found against the `criteria` (`basic`, `advanced`, `high`) and which `evidence` you
saw. Where you saw none, say so. Items of a module appear only with `--module`; `modules_available`
tells you when a module applies. Apply the `principles` in the output. You do not score and you do
not approve.

## Task 2: review an agent configuration

1. Run `levels`. Derive the agent's level from what it can actually read, write and call: the
   lowest level whose `capabilities` cover that. An agent that acts autonomously with no way to
   abort it is `prohibited`.
2. Run `controls <level-id>`. For each control, answer every assessment question with evidence from
   what you inspected.
3. Report per control: met, not met or not determinable, with the evidence (file and line, or
   setting).
4. Name the `approval_roles` of the level. Flag judgement calls for a person instead of deciding
   them.

## Task 3: check a change against the reassessment triggers

Run `triggers`. Compare the change (pull request, configuration diff, model or provider switch, new
purpose or user group) with the triggers of every item. Report which items are due for a new
assessment and which trigger fired. If purpose, user group or function changed, the triage runs
again as well.
