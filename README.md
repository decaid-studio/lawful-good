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

## Roadmap

`lawful-good` grows with the harmonised standards for the EU AI Act. Status per public
sources as of October 2026; check [jtc21.eu](https://jtc21.eu/) for the latest.

| Standard | Topic | AI Act | Status | lawful-good |
|---|---|---|---|---|
| EN 18286 | Quality management system | Art. 17 | Harmonised (Implementing Decision (EU) 2026/2274, since 14 Oct 2026) | v0.1: Art. 17 catalog, crosswalk pending legal review |
| prEN 18228 | AI risk management | Art. 9 | Draft, public enquiry closed | v0.2: Art. 9 catalog |
| prEN 18282 | Cybersecurity for AI systems | Art. 15 | Draft, public enquiry closed | v0.2: Art. 15 catalog, mapping to agent isolation controls |
| prEN 18229-1 | Logging | Art. 12 | Draft, public enquiry closed | v0.2: Art. 12 catalog, mapping to machine identity and audit trail |
| EN 18284 | Quality and governance of datasets | Art. 10 | In preparation | later |
| EN 18229-2 | Accuracy and robustness | Art. 15 | In preparation | later |
| ISO/IEC 42001 | AI management system (all organisations) | – (not harmonised) | Published | planned: crosswalk for non-high-risk use |

Also planned: OSCAL export, an example agent that checks a repository against the
controls, and an MCP server so agents can query the catalog directly.

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

### Roadmap

`lawful-good` wächst mit den harmonisierten Normen zum AI Act: als Nächstes Art. 9
(Risikomanagement, prEN 18228), Art. 12 (Logging, prEN 18229-1) und Art. 15
(Cybersicherheit, prEN 18282), danach Daten (EN 18284) und ein Crosswalk zu ISO/IEC 42001
für alle, die keine Hochrisiko-KI anbieten. Außerdem geplant: OSCAL-Export, ein
Beispiel-Agent zur Prüfung von Repositories und ein MCP-Server. Den aktuellen Stand der
Normen findet ihr auf [jtc21.eu](https://jtc21.eu/).

Lizenzen: Code und Schemas MIT, Inhalte CC BY 4.0, Gesetzestexte © Europäische Union.
