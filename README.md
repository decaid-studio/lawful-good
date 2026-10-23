# lawful-good

**Open, machine-readable AI governance controls for AI systems and agents.**
By [DECAID](https://www.decaid.ai) · Code MIT · Content CC BY 4.0

> Status: v0.1 · Not legal advice · Not a basis for EU AI Act conformity. See [NOTICE.md](NOTICE.md).

[Deutsch ↓](#deutsch)

## Why

Most AI systems are not high-risk under the EU AI Act. For them, the law asks for little
beyond supporting AI literacy and, for some systems, transparency. Yet companies still want to run
them safely: with clear ownership, least privilege, monitoring and a way to stop an agent
that goes wrong. There is no harmonised standard for this space.

`lawful-good` publishes DECAID's own governance recommendations as structured data, so
that people, governance tools and coding agents can read and apply them directly.

**Governance, not compliance.** This repository helps you run AI systems well. It does
not show conformity with any law or standard.

## What's inside

| Content | What it is | Format |
|---|---|---|
| **AI policy template** | A policy for organisations using AI, with every rule linked to the controls and check items below | Markdown (German) |
| **Agentic Governance Framework** | 8 clearance levels, 7 architectural controls, 6 supplementary practices for AI agents, with machine-readable thresholds | YAML (DE/EN) |
| **AI system assessment catalog** | 36 check items in six gates with maturity criteria, evidence, methods and reassessment triggers, plus a module for generated content | YAML (DE/EN) |

Together they answer three questions: what do we commit to (policy), how do agents enforce
it (framework), and how do we check that it works (assessment catalog). A crosswalk links
the catalog to the framework.

Scoring, weights and decision logic of the DECAID assessment are not part of this
repository.

## Principle

**Automate up to the judgement call, then a human decides.**
The data structures questions, thresholds and triggers. Weighing risks in a specific
case stays with people.

## Repository layout

```
templates/     AI policy template (Markdown)
schema/        JSON Schemas (framework, assessment catalog, crosswalk)
catalog/       Agentic framework and assessment catalog (YAML)
crosswalks/    Links between catalogs
tools/lg.py    Validate and build
AGENTS.md      How agents should use this repository
```

## Quick start

```bash
pip install -r requirements.txt
python tools/lg.py validate      # schema and reference checks
python tools/lg.py build         # writes dist/lawful-good.json
```

Agents: read [AGENTS.md](AGENTS.md).

## Roadmap

- **English version** of the policy template
- **Executable tests** per control: check that a boundary actually holds, not only that it is documented
- **Decision trees** for openly available obligations, e.g. transparency
- **Mappings** to openly available frameworks such as the NIST AI RMF
- **OSCAL export**
- **MCP server** on European infrastructure, so agents can query the controls directly

Ideas and pull requests are welcome, see [CONTRIBUTING.md](CONTRIBUTING.md).

## Licenses

| What | License |
|---|---|
| Code and schemas (`tools/`, `schema/`, workflows) | [MIT](LICENSE) |
| Content (frameworks, catalogs, crosswalks) | [CC BY 4.0](LICENSE-CONTENT) |

Attribution: *"lawful-good by DECAID, CC BY 4.0"*.

---

## Deutsch

**Offene, maschinenlesbare Governance-Controls für KI-Systeme und Agenten.**

Die meisten KI-Systeme sind nach dem EU AI Act kein Hochrisiko. Für sie verlangt das Gesetz
wenig über die Förderung von KI-Kompetenz und, für manche Systeme, Transparenz hinaus. Trotzdem wollen
Unternehmen sie sicher betreiben: mit klarer Verantwortung, minimalen Rechten, Monitoring und
der Möglichkeit, einen fehlgeleiteten Agenten zu stoppen. Für diesen Bereich gibt es keine
harmonisierte Norm.

`lawful-good` veröffentlicht die Governance-Empfehlungen von DECAID als strukturierte Daten,
damit Menschen, Governance-Tools und Coding Agents sie direkt lesen und anwenden können.

**Governance, nicht Compliance.** Das Repository hilft, KI-Systeme gut zu betreiben. Es weist
keine Konformität mit Gesetzen oder Normen nach.

Inhalt:

- **Vorlage für eine KI-Richtlinie**, jede Regel verknüpft mit Controls und Prüfpunkten
- **Agentic Governance Framework**: 8 Level, 7 Kontrollen, 6 ergänzende Praktiken für Agenten
- **Prüfkatalog zur KI-Systemprüfung**: 36 Prüfpunkte in sechs Gates mit Reifegraden,
  Nachweisen und Reassessment-Triggern, dazu ein Modul für generierte Inhalte

Bewertungslogik, Gewichte und Scoring der DECAID-Prüfung sind nicht Teil des Repositorys.

Leitsatz: **Automatisieren bis zur Abwägung, dann entscheidet ein Mensch.**

Lizenzen: Code und Schemas MIT, Inhalte CC BY 4.0.
