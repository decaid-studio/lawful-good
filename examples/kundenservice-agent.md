# Beispielfall: Ein Agent für Kundenmails

> **Fiktives Beispiel.** Unternehmen, System und Ergebnisse sind erfunden. Der Fall zeigt, wie
> ein Use Case durch lawful-good läuft. Er ist keine Rechtsberatung und keine Vorlage für eine
> echte Einstufung. *English: a fictional worked example of one use case running through
> lawful-good. German only for now.*

Ein Use Case, fünf Schritte: Vorprüfung, Level, Prüfkatalog, Entscheidung, Trigger. Alle
Fragen, Kontrollen und Prüfpunkte stammen unverändert aus dem Repository; die Antworten und
Begründungen sind die des fiktiven Unternehmens.

## Der Fall

Die **Radwerk Muster GmbH** verkauft Fahrräder und Zubehör online, 40 Beschäftigte, Sitz in
Leipzig. Im Kundenservice gehen täglich rund 300 Mails ein. Ein Agent soll helfen:

| | |
|---|---|
| **System** | „Mailassistent“ v1.0 auf der KI-Plattform des Unternehmens, Sprachmodell eines externen Anbieters über die Plattform |
| **Zweck** | Eingehende Kundenmails lesen, den Vorgang im Shopsystem nachschlagen und einen Antwortentwurf vorbereiten |
| **Nutzer** | 6 Beschäftigte im Kundenservice |
| **Betroffene** | Kundinnen und Kunden, die an den Service schreiben |
| **Was der Agent darf** | Mails und Bestelldaten lesen, Entwürfe im Ticketsystem anlegen. **Senden darf nur ein Mensch.** |
| **Was er nicht darf** | Mails versenden, Erstattungen auslösen, Daten im Shop ändern |

## Schritt 1: Vorprüfung

`python tools/lg.py triage` führt durch den Entscheidungsbaum. Die Antworten:

| Frage | Antwort | Begründung |
|---|---|---|
| Ist es ein KI-System? (Art. 3 Nr. 1) | Ja | Das Sprachmodell leitet aus der Mail ab, welche Antwort es entwirft. |
| Bezug zur EU? (Art. 2 Abs. 1) | Ja | Betrieb in Leipzig, Kundschaft in der EU. |
| Ausnahme vom Anwendungsbereich? (Art. 2) | Nein | Beruflicher Einsatz, keine Forschung, kein Militär. |
| Eigenes KI-Modell mit allgemeinem Verwendungszweck? (Art. 3 Nr. 63) | Nein | Das Modell wird nur über die Plattform genutzt. |
| Rolle? (Art. 3 Nr. 3, 4) | Betreiber | Radwerk setzt das System in eigener Verantwortung ein und bietet es nicht an. |
| Verbotene Praxis? (Art. 5) | Nein | Keine Manipulation, kein Scoring, keine Biometrie. |
| Hochrisiko? (Art. 6, Anhang I, III) | Nein | Kundenservice für Bestellungen fällt in keinen Bereich nach Anhang III. |
| Interagiert das System direkt mit Menschen? (Art. 50 Abs. 1) | **Unklar** | Kunden lesen Texte, die der Agent entworfen hat, aber ein Mensch prüft und sendet sie. Ob das eine direkte Interaktion ist, kann das Team nicht sicher sagen. |
| Erzeugt das System synthetische Inhalte? (Art. 50 Abs. 2) | Ja | Die Antwortentwürfe sind KI-erzeugter Text. |
| Deepfakes oder Texte zu öffentlichem Interesse? (Art. 50 Abs. 4) | Nein | Individuelle Kundenkorrespondenz, keine Veröffentlichung. |

**Ergebnis:** Weiter mit dem Prüfkatalog. Unterwegs gesammelte Hinweise:

- **Rolle: Betreiber** (Art. 3 Nr. 4)
- **KI-Kompetenz** der sechs Beschäftigten fördern (Art. 4, seit 2.2.2025), siehe Prüfpunkt G3-03
- **Transparenz unklar** (Art. 50): rechtlich zu klären. Die kritischen Fragen hätten bei
  „unklar“ gestoppt; bei der Transparenz geht der Baum mit diesem Hinweis weiter.
- **Erzeugte Inhalte** (Art. 50 Abs. 2): Kennzeichnungspflicht liegt beim Anbieter des
  Modells, Radwerk prüft die Offenlegung, siehe G3-06 und G4-09

**Parallel prüfen:** Datenschutz (Kundendaten, Auftragsverarbeitung mit dem Modellanbieter),
siehe G2-02 und G2-07.

Was dieser Schritt zeigt: Der Baum rät nicht. Wo das Team unsicher war, steht „unklar“, und
daraus wird ein Hinweis, den ein Mensch klärt.

## Schritt 2: Level einordnen

Das Level richtet sich nach dem, was der Agent tatsächlich kann, nicht nach dem, was er tun
soll.

| | |
|---|---|
| **Lesen** | intern und extern (Mails, Bestelldaten) |
| **Schreiben** | nur vorbereiten: Entwürfe im Ticketsystem |
| **Level** | **Level 4 „Confidential“** (`level-4`) |
| **Freigabe durch** | Product Owner |

Für Level 4 verlangt das Framework diese Kontrollen (`python skill/lawful-good/scripts/lawful_good.py controls level-4`):

| Kontrolle | Geprüft | Stand |
|---|---|---|
| DAG-C1 Least Privilege | Konfiguration: nur Mail-Postfach (lesen), Shop (lesen), Ticketsystem (Entwurf anlegen) | erfüllt |
| DAG-C2 Deterministische Tool-Calls | Zugriffe über fest definierte Schnittstellen der Plattform | erfüllt |
| DAG-C3 Guardrails auf Tool-Ebene | Versand ist im Ticketsystem für den Agenten technisch gesperrt, nicht nur per Prompt verboten | erfüllt |
| DAG-C4 Rekursions- und Abbruchgrenzen | Iterationslimit und Timeout gesetzt, **Token-Budget fehlt** | offen |
| DAG-C6 Monitoring und Drift | Stichproben wöchentlich; automatischer Entzug der Freigabe bei Modellwechsel **noch nicht eingerichtet** | offen |
| DAG-C7 Systembereinigung | Agent im Inventar, Owner benannt | erfüllt |
| DAG-P3 Audit-Trail | Plattform protokolliert Tool-Calls mit Zeitstempel | erfüllt |
| DAG-P4 Inventar und Owner | Agent Owner: Teamleitung Kundenservice | erfüllt |
| DAG-P5 Kill Switch | Admin kann den Agenten sofort deaktivieren, getestet | erfüllt |
| DAG-P6 Kennzeichnung | nicht nötig, solange Menschen senden; wird mit der Transparenzfrage aus Schritt 1 entschieden | offen |

## Schritt 3: Prüfkatalog (Auszug)

Eine vollständige Prüfung geht alle 36 Prüfpunkte in den Gates G0 bis G5 durch. Hier ein
Auszug, eingestuft nach den Reifegraden des Katalogs (Basic, Advanced, High):

| Prüfpunkt | Nachweis | Reifegrad |
|---|---|---|
| **G0-01** Use Case eindeutig beschrieben? | Use-Case-Steckbrief (oben) | Advanced |
| **G1-02** Klar, was Menschen entscheiden? | Prozess: Agent entwirft, Mensch prüft und sendet | Advanced |
| **G2-06** Anbieter, Auftragsverarbeitung, Datenstandorte bewertet? | AV-Vertrag mit der Plattform liegt vor, Subprozessoren noch nicht geprüft | Basic |
| **G3-02** Eingriff und Stopp praktisch nutzbar? | Kill Switch getestet, Eskalation an Teamleitung beschrieben | Advanced |
| **G3-05** Betroffene informiert? | Hinweis in der Signatur fehlt bisher | nicht erfüllt |
| **G4-02** Berechtigungen technisch beschränkt? | Rollenmatrix, Sendesperre im Ticketsystem | Advanced |
| **G4-04** Ausgaben auf Halluzinationen, Datenabfluss getestet? | 40 Testmails, darunter 10 mit Fangfragen; 2 Entwürfe nannten falsche Lieferzeiten | Basic |
| **G5-04** Trigger für erneute Prüfung definiert? | Triggerliste (Schritt 5) | Basic |

Der Katalog liefert Fragen, Kriterien und Nachweise. Wie die Einstufungen gewichtet und zu
einer Empfehlung verdichtet werden, ist nicht Teil des Repositorys. Das bleibt eine Abwägung.

## Schritt 4: Ein Mensch entscheidet

Der Product Owner Kundenservice gibt den Agenten **unter Auflagen** frei, zunächst als Pilot
mit zwei der sechs Beschäftigten:

| Auflage | Bezug | Owner | Frist |
|---|---|---|---|
| Token-Budget setzen | DAG-C4 | Plattform-Admin | vor Start |
| Automatischen Entzug der Freigabe bei Modell- oder Promptänderung einrichten | DAG-C6 | Plattform-Admin | 2 Wochen |
| Transparenzfrage rechtlich klären, danach Hinweis in der Signatur entscheiden | Art. 50, G3-05, DAG-P6 | Geschäftsführung | 4 Wochen |
| Lieferzeiten nur aus dem Shopsystem übernehmen, Testfälle wiederholen | G4-04 | Agent Owner | vor Ausweitung |
| Subprozessoren des Modellanbieters prüfen | G2-06 | Datenschutz | 4 Wochen |
| Kurzschulung für die Nutzer: Grenzen des Agenten, wann eskalieren | Art. 4, G3-03 | Teamleitung | vor Start |

Was dieser Schritt zeigt: Die Daten strukturieren die Entscheidung, sie treffen sie nicht.

## Schritt 5: Trigger halten den Fall aktuell

Eine erneute Prüfung ist fällig, wenn:

- das Sprachmodell oder der Anbieter wechselt (DAG-C6, G2-06, G4-04)
- der Agent selbst senden soll: Das wäre schreibender Zugriff nach außen, also mindestens
  Level 5 mit Freigabe durch den Governance Owner
- ein neuer Kanal dazukommt, etwa ein Chat auf der Website: dann interagiert das System direkt
  mit Kundinnen und Kunden (Art. 50 Abs. 1, DAG-P6)
- sich Zweck, Nutzergruppe oder Datenzugriffe ändern (G0-01, G4-02)
- spätestens nach 90 Tagen (DAG-C6)

## Protokoll für das KI-Register

So sieht der Eintrag aus, den `triage` vorbefüllt und das Team ergänzt hat:

```yaml
system: Mailassistent v1.0
use-case: Antwortentwürfe für Kundenmails im Kundenservice, 6 Nutzer, Versand nur durch Menschen
tree-version: decaid.eu-ai-act-triage 0.1.0 / Regulation (EU) 2024/1689, consolidated version 02024R1689-20260727
answers:
  - {question: ai-system, answer: "yes", justification: Sprachmodell leitet Antwortentwurf aus der Mail ab}
  - {question: territorial, answer: "yes", justification: Betrieb und Kundschaft in der EU}
  - {question: scope, answer: "no", justification: beruflicher Einsatz}
  - {question: gpai, answer: "no", justification: Modell nur über die Plattform genutzt}
  - {question: role, answer: deployer, justification: Einsatz in eigener Verantwortung}
  - {question: prohibited, answer: "no", justification: keine Praxis nach Art. 5}
  - {question: high-risk, answer: "no", justification: kein Bereich nach Anhang III}
  - {question: transparency-interaction, answer: unclear, justification: Mensch prüft und sendet, Einordnung offen}
  - {question: transparency-synthetic, answer: "yes", justification: Entwürfe sind KI-erzeugter Text}
  - {question: transparency-deepfake, answer: "no", justification: keine Veröffentlichung}
outcome: continue-catalog
flags: [role-deployer, ai-literacy, transparency-unclear, transparency-synthetic]
assessed-by: Agent Owner Kundenservice
approved-by: Product Owner Kundenservice
date: '2026-11-26'
legal-review: Transparenzfrage offen, Frist 4 Wochen
next-review: Modell- oder Anbieterwechsel, neuer Kanal, Versand durch den Agenten, spätestens 90 Tage
```

## Variante: Derselbe Agent für Bewerbermails

Würde Radwerk denselben Agenten Bewerbungen vorsortieren lassen, sähe die Vorprüfung anders
aus. Bei der Frage nach Hochrisiko lautet die Antwort „Ja“: Beschäftigung und
Personalmanagement, etwa die Auswahl von Bewerbern, ist ein Bereich nach Anhang III.

**Ergebnis: Stopp, möglicherweise Hochrisiko.** Der Baum geht nicht weiter in den
Prüfkatalog. Vor jedem Einsatz steht eine rechtliche Prüfung, danach entscheidet ein Mensch.
Für Hochrisiko-Systeme ist lawful-good nicht gedacht.

---

*Keine Rechtsberatung. Das Ergebnis beruht auf Governance-Empfehlungen von DECAID und weist
keine Konformität mit dem EU AI Act oder anderen Gesetzen und Normen nach.*
