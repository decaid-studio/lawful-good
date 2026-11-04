# lawful-good

**Open, machine-readable AI governance for AI systems and agents.**
By [DECAID](https://www.decaid.ai) · Code MIT · Content CC BY 4.0

> Status: v0.1 · Not legal advice · Not a basis for EU AI Act conformity. See [NOTICE.md](NOTICE.md).

[Deutsch ↓](#deutsch)

## Why

**Governance with AI, not only governance for AI.** More and more organisations use AI
agents to take in, research and pre-assess new AI use cases. Those agents need a rulebook
they can read. `lawful-good` is that open rulebook: triage, policy, controls, check items
and triggers as data, with people deciding at the gates.

Most AI systems are not high-risk under the EU AI Act. For them, the law asks for little
beyond supporting AI literacy and, for some systems, transparency. Yet companies still want
to run them safely: with clear ownership, least privilege, monitoring and a way to stop an
agent that goes wrong. There is no harmonised standard for this space. `lawful-good`
publishes DECAID's own governance recommendations for it.

**Governance, not compliance.** This repository helps you run AI systems well. It does not
show conformity with any law or standard.

## What's inside

| Content | Question it answers | Format |
|---|---|---|
| **EU AI Act triage** | Does the AI Act apply, in which role, and does the case need legal review? Ends with a record for the AI register and a list of other law to check in parallel | Decision tree, YAML (DE/EN) |
| **AI policy template** | What do we commit to? Every rule links to the controls and check items | Markdown (German) |
| **Agentic Governance Framework** | How do agents enforce it? 8 clearance levels, 7 architectural controls, 6 supplementary practices | YAML (DE/EN) |
| **AI system assessment catalog** | Does it work? 36 check items in six gates with maturity criteria, evidence and reassessment triggers, plus a module for generated content | YAML (DE/EN) |

A use case runs through them in order:

```
use case ─► triage ─┬─► stop: possibly prohibited, high-risk or unclear ─► legal review
                    ├─► outside the AI Act ─► document
                    └─► assessment catalog (G0–G5) ─► people decide ─► triggers keep it current
                              ▲
                  policy template + agentic framework
```

Scoring, weights and decision logic of the DECAID assessment are not part of this
repository. The background is explained in DECAID's white paper *Agentic Governance –
Wenn KI handelt statt antwortet*, available at [decaid.ai](https://www.decaid.ai](https://www.decaid.ai/downloads/agentic-governance).

## Principle

**Automate up to the judgement call, then a human decides.**
The data structures questions, thresholds and triggers. Weighing risks in a specific case
stays with people. On critical triage questions, "unclear" always stops; the tooling
enforces this rule.

## Repository layout

```
catalog/decision-trees/   EU AI Act triage
catalog/frameworks/       Agentic Governance Framework
catalog/assessments/      AI system assessment catalog
crosswalks/               Links between catalogs
templates/                AI policy template (Markdown)
schema/                   JSON Schemas
tools/lg.py               Validate, build and run the triage
AGENTS.md                 How agents should use this repository
```

## Quick start

```bash
pip install -r requirements.txt
python tools/lg.py triage --lang en   # walk through the triage in the terminal
python tools/lg.py validate           # schema and reference checks
python tools/lg.py build              # writes dist/lawful-good.json
```

Agents: read [AGENTS.md](AGENTS.md).

## Roadmap

- **More modules** for the assessment catalog, e.g. third-country transfers, copyright and
  licences, employees and co-determination, own development and training
- **Example governance agent**: takes in a use case from e-mail or a ticket, runs it through
  the triage and the catalog, hands decisions to people at the gates and watches the
  reassessment triggers, using tools organisations already have
- **Executable tests** per control: check that a boundary actually holds, not only that it
  is documented
- **English version** of the policy template
- **Mappings** to openly available frameworks such as the NIST AI RMF, and to AIUC-1 once
  its terms of use allow it
- **OSCAL export**
- **MCP server** on European infrastructure, so agents can query the rulebook directly

Ideas and pull requests are welcome, see [CONTRIBUTING.md](CONTRIBUTING.md).

**High-risk AI?** This repository is not the right place. For the status of the harmonised
standards see [ai-act-standards.com](https://ai-act-standards.com/), and seek legal advice.

## Licenses

| What | License |
|---|---|
| Code and schemas (`tools/`, `schema/`, workflows) | [MIT](LICENSE) |
| Content (decision tree, frameworks, catalogs, crosswalks, template) | [CC BY 4.0](LICENSE-CONTENT) |

Attribution: *"lawful-good by DECAID, CC BY 4.0"*.

---

## Deutsch

**Offene, maschinenlesbare KI-Governance für KI-Systeme und Agenten.**

**Governance mit KI, nicht nur Governance für KI.** Immer mehr Unternehmen lassen neue
KI-Anwendungsfälle von Agenten aufnehmen, recherchieren und vorbewerten. Diese Agenten
brauchen ein Regelwerk, das sie lesen können. `lawful-good` ist dieses offene Regelwerk:
Vorprüfung, Richtlinie, Controls, Prüfpunkte und Trigger als Daten, und an den Gates
entscheiden Menschen.

Die meisten KI-Systeme sind nach dem EU AI Act kein Hochrisiko. Für sie verlangt das Gesetz
wenig über die Förderung von KI-Kompetenz und, für manche Systeme, Transparenz hinaus.
Trotzdem wollen Unternehmen sie sicher betreiben: mit klarer Verantwortung, minimalen
Rechten, Monitoring und der Möglichkeit, einen fehlgeleiteten Agenten zu stoppen. Für diesen
Bereich gibt es keine harmonisierte Norm. `lawful-good` veröffentlicht dafür die
Governance-Empfehlungen von DECAID.

**Governance, nicht Compliance.** Das Repository hilft, KI-Systeme gut zu betreiben. Es weist
keine Konformität mit Gesetzen oder Normen nach.

Inhalt:

- **Vorprüfung nach dem EU AI Act**: Entscheidungsbaum zu KI-System, räumlichem und
  sachlichem Anwendungsbereich, Rolle, Verboten, Hochrisiko und Transparenz. Bei
  Verbotsverdacht, möglichem Hochrisiko oder Unklarheit: Stopp und rechtliche Prüfung. Am
  Ende stehen ein Protokoll für das KI-Register und die Rechtsgebiete, die parallel zu
  prüfen sind
- **Vorlage für eine KI-Richtlinie**, jede Regel verknüpft mit Controls und Prüfpunkten
- **Agentic Governance Framework**: 8 Level, 7 Kontrollen, 6 ergänzende Praktiken für Agenten
- **Prüfkatalog zur KI-Systemprüfung**: 36 Prüfpunkte in sechs Gates mit Reifegraden,
  Nachweisen und Reassessment-Triggern, dazu ein Modul für generierte Inhalte

Ausprobieren: `python tools/lg.py triage`

Bewertungslogik, Gewichte und Scoring der DECAID-Prüfung sind nicht Teil des Repositorys.
Hintergrund im Whitepaper *Agentic Governance – Wenn KI handelt statt antwortet* auf
[decaid.ai](https://www.decaid.ai).

Leitsatz: **Automatisieren bis zur Abwägung, dann entscheidet ein Mensch.**

**Hochrisiko-KI?** Dafür ist dieses Repository nicht gedacht. Zum Stand der harmonisierten
Normen siehe [ai-act-standards.com](https://ai-act-standards.com/); lassen Sie sich rechtlich
beraten.

Lizenzen: Code und Schemas MIT, Inhalte CC BY 4.0.
