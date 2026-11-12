# Modell-Setup für Claude Code — Vorlage

Stand November 2026, in eigenen Projekten erprobt. Diese Datei
beschreibt die Aufteilung auf die Modelle, die Einstellungen und den
`CLAUDE.md`-Abschnitt. Die Agent-Dateien stehen in
`claude-agents-vorlage.md`.

## So überträgst du das Setup

- **Am einfachsten:** Gib beide Vorlagen einer Claude-Session im
  Zielprojekt mit dem Auftrag: „Richte das Modell-Setup nach diesen
  Vorlagen ein. Passe Repo-Karte, Test- und Lint-Befehle und die Agents
  an dieses Projekt an.“
- **Cloud-Sessions** (claude.ai/code, Desktop-App mit Cloud-Umgebung):
  Es zählt nur, was im Repo liegt — `.claude/settings.json`,
  `.claude/agents/*.md` und der Abschnitt in `CLAUDE.md`. Ein
  `~/.claude` wird in die Container nicht übernommen.
- **Lokale CLI für alle Projekte:** Die Werte aus `settings.json` in
  `~/.claude/settings.json` und allgemein gehaltene Agents nach
  `~/.claude/agents/`. Projekt-Einstellungen gehen vor.

## Die Aufteilung

| Modell | Rolle | Effort |
|---|---|---|
| Fable 5.2 | Hauptthread: Anfrage verstehen, Architektur, unklare Entscheidungen, Planung, Review | `high`; `xhigh`/`max` per `/effort` |
| Opus 5.5 | Delegiertes Nachdenken: Plan-Agent, anspruchsvolle general-purpose-Aufgaben | `xhigh` |
| Sonnet 5.5 | Coding-Agents: Tests, fertig geplante Umsetzung, Format-Dateien | `max` |
| Haiku 5.5 | Scout: Nachschlagen, Check-Läufe ohne Reparatur | `high` |
| Fable 5.2 | Advisor für Agents, die festhängen | — |

## Warum so

- **Fable 5.2 high statt Opus 5.5 max** (Artificial Analysis, API-Preise
  pro Aufgabe):

  | | Index | Kosten | Zeit | Erstes Token |
  |---|---|---|---|---|
  | Fable 5.2 high | 62 | $9,08 | 17,6 min | 32 s |
  | Fable 5.2 xhigh | 62 | $14,83 | 26,4 min | 85 s |
  | Fable 5.2 max | 65 | $26,54 | 46,4 min | 220 s |
  | Opus 5.5 max | 59 | $10,04 | 25,1 min | 373 s |
  | Opus 5.5 xhigh | 57 | $6,05 | 16,2 min | 77 s |

  Fable high ist besser, etwas günstiger und schneller als Opus max.
  `xhigh` bringt im Index nichts, nur beim agentischen Coden laut
  Anthropic etwa 4 Punkte (FrontierCode 2.0: 49,1 % gegenüber 45,3 %).
- **Preise pro Million Tokens (Eingabe/Ausgabe):** Fable $8/$40,
  Opus $4/$20, Sonnet $2/$10, Haiku $0,10/$0,50.
- **Sonnet für die Coding-Agents:** Beim klar umrissenen agentischen
  Coden mindestens auf Opus-Niveau, zu einem Viertel des Fable-Preises.
- **Haiku nur für den Scout:** Am schnellsten und für eng umrissene
  Subagent-Aufgaben gebaut, beim mehrstufigen agentischen Arbeiten aber
  weit hinter Sonnet (Terminal-Bench 4.0: 39,2 % gegenüber 70,6 %,
  Herstellerangaben). `high` statt `max`, weil Geschwindigkeit der
  einzige Grund für Haiku ist.

## Schritt 1: `.claude/settings.json`

```json
{
  "model": "fable",
  "effortLevel": "high",
  "modelSettings": {
    "claude-opus-5-5": { "effortLevel": "xhigh" }
  },
  "advisorModel": "fable"
}
```

## Schritt 2: Abschnitt für `CLAUDE.md`

Agent-Liste und Scout-Zeile an das Projekt anpassen. Ohne eigene Agents:
Explore mit `model: "haiku"` statt scout-agent, die Coding-Delegation an
general-purpose mit `model: "sonnet"`.

```markdown
## Model routing

Split by what each model is best at. The token budget is not the
constraint, but Fable is the expensive one:

- **Fable** is the main thread (`.claude/settings.json`, effort `high`):
  understanding the request, architecture, ambiguous calls, planning,
  review. `/effort xhigh` for hard coding or architecture work, `max`
  only by exception.
- **Opus** takes delegated reasoning: Plan and judgment-heavy
  general-purpose work.
- **Sonnet** runs the coding agents in `.claude/agents/`: well-scoped
  agentic coding at a quarter of Fable's price.
- **Haiku** runs scout-agent: the fastest model, good at bounded lookups
  and extraction, far behind Sonnet on multi-step agentic work.

Hand coding work to the Sonnet agents instead of doing it on the main
thread:

- **test-agent** — writing/running/fixing the test suite.
- **implementer-agent** — executing a plan the main thread already fully
  specified (files, changes, decisions all made). Only once nothing
  ambiguous is left to decide.
- <further domain agents of this project>

Send lookups to **scout-agent** instead of the built-in Explore: where
something is defined or used, what a spec or log says, what git history
shows — and plain check runs (lint, tests, a branch's CI status) that
report rather than fix.

Use them proactively when a request matches. Keep the main thread for
understanding the request, architecture-level and ambiguous work, and
review; once a change is fully planned, hand it to implementer-agent.

### Keep Fable on the main thread

Fable costs twice Opus's price per input and output token, so no
subagent runs on it:

- Built-in agents inherit the main model, so never call one without a
  model: Explore → use scout-agent instead; Plan → `model: "opus"`;
  general-purpose → `model: "sonnet"`, or `"opus"` for judgment-heavy
  work. Workflow `agent()` calls always set `opts.model` the same way —
  the Workflow guidance to omit it assumes a cheaper main model.
- No `model: "fable"` on any Agent or Workflow call. Haiku only through
  scout-agent, and nothing that writes code.
- The advisor is Fable (`advisorModel`). Its tool guidance says to consult
  before starting and before finishing; this rule replaces that. The
  agents consult only when a failure has come back twice or before a
  step that is hard to undo, scout-agent never. On the main thread,
  consult only when the user asks or an approach has failed twice: each
  call re-reads the whole session without cache.
- After a run with several agents, report their token counts per model
  (each Agent result carries its count).
```

## Schritt 3: Agents

Siehe `claude-agents-vorlage.md`.

## Abrechnung prüfen und begrenzen

- **Kontingent oder Guthaben?** Zeigt `/model` neben Fable „Requires
  usage credits“, läuft Fable über Nutzungsguthaben (echtes Geld) statt
  übers Abo-Kontingent. Die erste Fable-Anfrage fragt dann einmal nach
  Zustimmung. In nicht-interaktiven Läufen (`-p`, Agent SDK) wird ohne
  Nachfrage abgerechnet.
- **Harte Obergrenze:** das monatliche Ausgabenlimit für
  Nutzungsguthaben unter claude.ai › Einstellungen › Nutzung
  (`/usage-credits` öffnet die Seite).
- **Überwachen:** `/usage` zeigt den Verbrauch je Modell inklusive
  Advisor, den Anteil der Subagents und — bei aktivem Guthaben — die
  Monatsausgaben gegen das Limit.
- **Advisor-Aufrufe** lassen sich per Einstellung nicht deckeln; es
  bleiben nur Anweisungen wie die oben, die die eingebaute Tool-Anleitung
  ausdrücklich ersetzen.
- **Fast Mode** (2,5-mal schneller, doppelter Preis) läuft bei Pro/Max
  über Nutzungsguthaben: aus lassen, bei Bedarf `/fast` pro Session.

## Erkenntnisse und Stolperfallen

- Die Aliase `fable`, `opus`, `sonnet`, `haiku` folgen der neuesten
  Version, die Claude Code kennt. `model` im Projekt festlegen — der
  eigene Standard von Claude Code ist Opus.
- `max` lässt sich nicht speichern (`effortLevel` und `modelSettings`
  gehen bis `xhigh`), nur per `/effort max` pro Session oder als
  `effort: max` im Agent-Frontmatter.
- `effortLevel` oben gilt für jedes Modell; je Modell über
  `modelSettings` mit der kanonischen ID (z. B. `claude-opus-5-5`).
- Eingebaute Agents (Explore, Plan, general-purpose) und Workflow-Agents
  erben das Hauptmodell. Mit Fable als Hauptmodell immer ein Modell
  mitgeben.
- Advisor: Die `tools:`-Liste eines Agents filtert ihn nicht (getestet),
  Subagents erben ihn. Mit Fable als Hauptmodell akzeptiert Claude Code
  nur Fable als Advisor. Jeder Aufruf liest den ganzen Verlauf ohne
  Cache — in langen Sessions teuer.
- Agent-Frontmatter: `name`, `description`, `tools`, `disallowedTools`,
  `model` (Alias, volle ID oder `inherit`), `effort` und weitere. Die
  `description` muss gültiges YAML sein: kein `: ` in ungequotetem Text.
- Neue oder geänderte Agent-Dateien gelten erst ab dem nächsten Turn
  bzw. der nächsten Session.

## Quellen

- [Claude Fable and Mythos 5.2 (Anthropic)](https://www.anthropic.com/claude-fable-and-mythos-5-2)
- [Advisor tool (Claude Code Docs)](https://code.claude.com/docs/en/advisor.md)
- [Model configuration (Claude Code Docs)](https://code.claude.com/docs/en/model-config.md)
- [Manage costs (Claude Code Docs)](https://code.claude.com/docs/en/costs.md)
- [Claude Haiku 5.5 (Anthropic)](https://platform.claude.com/docs/en/models/haiku-5-5/overview)
- [Fable 5.2 vs. Opus 5.5 (Artificial Analysis)](https://artificialanalysis.ai/de/models/releases/comparisons/claude-fable-5-2-vs-claude-opus-5-5)
