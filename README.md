# lawful-good

**Open, machine-readable AI compliance controls for agents.**
EU AI Act Art. 17 · EN 18286 crosswalk · DECAID Agentic Governance Framework

> Status: **v0.1 draft, private.** Not legal advice. See [NOTICE.md](NOTICE.md).

[Deutsch ↓](#deutsch)

## Why

Harmonised standards such as EN 18286 (quality management for the EU AI Act) sit behind a
paywall, and the law itself is written for humans. Coding agents and governance tools need
the requirements as structured data. `lawful-good` provides:

- **Legal requirements as data:** EU AI Act Art. 17 in German and English, with application
  dates as amended by the Digital Omnibus on AI (Regulation (EU) 2026/1744).
- **Agentic governance as data:** the DECAID Security Clearance levels (1–8) and the seven
  architectural control principles, with machine-readable thresholds.
- **Crosswalks:** how the controls support AI Act obligations, and (after legal review) which
  EN 18286 clauses address each Art. 17 point. **Clause numbers only, never standard text.**

## Repository layout

```
schema/        JSON Schemas (common, regulation, framework, crosswalk)
catalog/       Regulations and frameworks (YAML)
crosswalks/    Mappings between catalogs
drafts/        Content blocked until legal review – never published
tools/lg.py    Validate and build
AGENTS.md      How agents should use this repository
```

## Quick start

```bash
pip install -r requirements.txt
python tools/lg.py validate      # schema + reference checks
python tools/lg.py build         # dist/lawful-good.json (public content only)
```

## Licenses

| What | License |
|---|---|
| Code and schemas (`tools/`, `schema/`, workflows) | [MIT](LICENSE) |
| Content (controls, levels, crosswalks, summaries, assessment questions) | [CC BY 4.0](LICENSE-CONTENT) |
| EU legal texts | Reuse with acknowledgement, © European Union (EUR-Lex) |

Attribution for content: *"lawful-good by DECAID, CC BY 4.0"*.

---

## Deutsch

**Offene, maschinenlesbare KI-Compliance-Controls für Agenten.**

Harmonisierte Normen wie die EN 18286 (Qualitätsmanagement für den EU AI Act) liegen hinter
einer Paywall, und das Gesetz ist für Menschen geschrieben. Coding Agents und
Governance-Tools brauchen die Anforderungen als strukturierte Daten. `lawful-good` liefert:

- **Gesetzliche Anforderungen als Daten:** Art. 17 KI-Verordnung auf Deutsch und Englisch,
  mit den Geltungsdaten nach dem Digital Omnibus on AI (VO (EU) 2026/1744).
- **Agentic Governance als Daten:** die DECAID Security-Clearance-Level (1–8) und die sieben
  architektonischen Kontrollprinzipien mit maschinenlesbaren Schwellenwerten.
- **Crosswalks:** wie die Kontrollen Pflichten der KI-Verordnung unterstützen und (nach
  juristischer Prüfung) welche EN-18286-Klauseln welchen Buchstaben von Art. 17 adressieren.
  **Nur Klauselnummern, niemals Normtext.**

Die Nutzung dieses Repositorys begründet **keine Konformitätsvermutung** und ist keine
Rechtsberatung. Die Konformitätsvermutung entsteht nur durch Anwendung der Norm selbst.

Lizenzen: Code und Schemas MIT, Inhalte CC BY 4.0, Gesetzestexte © Europäische Union.
