# Changelog

All notable changes to lawful-good. Format based on [Keep a Changelog](https://keepachangelog.com/),
versions follow [Semantic Versioning](https://semver.org/).

## How we keep it current

- **Monthly review** of all content by DECAID, noted here even when nothing changed.
- **Event-driven updates** when the EU AI Act, its delegated or implementing acts, or official
  guidelines change in a way that affects the triage or the catalogs. The `law_version` field in
  the decision tree names the consolidated version the questions refer to.
- Every content file carries a `verification` block with status and date.
- Versions: **patch** for corrections and wording, **minor** for new questions, check items,
  controls or modules, **major** for changes that alter existing ids or results.

## [Unreleased]

## [0.1.0] - 2026-11-27

First public release.

### Added
- EU AI Act triage as a decision tree (DE/EN): AI system, territorial and material scope,
  general-purpose AI models, role, prohibited practices, high-risk, transparency. "Unclear" on
  critical questions always stops; the validator enforces this. Ends with a record for the AI
  register and a list of other law to check in parallel.
- Agentic Governance Framework (DE/EN): 8 clearance levels, 7 architectural controls,
  6 supplementary practices.
- AI system assessment catalog (DE/EN): 36 check items in gates G0 to G5 with maturity
  criteria, evidence, methods and reassessment triggers; module for generated content.
- AI policy template (German), every rule linked to controls and check items.
- Agent skill for Claude and Langdock (`skill/lawful-good`).
- Worked example of a fictional use case (`examples/kundenservice-agent.md`).
- Banner and diagram (`assets/`), with editable sources.
- Tooling: JSON Schemas, `tools/lg.py` (validate, build, triage), tests, CI.

### Changed (during the soft launch, 2026-11-04 to 2026-11-26)
- Rights holder stated as DECAID Group GmbH in all licence notices.
- Output channels in the generated-content module and in G4-09 worded for any kind of
  generated content.
- Repository hygiene: least-privilege CI, sign-off check for pull requests, security policy.
