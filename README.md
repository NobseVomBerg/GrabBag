# GrabBag

Viel vielleicht Nützliches und etwas Müll obendrauf: Vorlagen zum
Kopieren und Anpassen.

## Inhalt

### Claude Code: Modelle und Agents (`claude-orchestrator/`)

| Datei | Worum es geht |
|---|---|
| [claude-modell-setup.md](claude-orchestrator/claude-modell-setup.md) | Welches Modell welche Aufgabe übernimmt, `settings.json`, Abschnitt für `CLAUDE.md`, Kosten im Blick behalten |
| [claude-agents-vorlage.md](claude-orchestrator/claude-agents-vorlage.md) | Subagents fürs Nachschlagen, für Tests, für fertig geplante Umsetzung und für eigene Dateiformate |

Am schnellsten: Gib beide Dateien einer Claude-Session in deinem Projekt
und lass sie das Setup anpassen. Wie genau, steht in der Setup-Datei.

### Home Assistant (`home-assistant/`)

| Ordner | Worum es geht |
|---|---|
| [sungrow-modbus/](home-assistant/sungrow-modbus/) | Modbus-Sensoren für zwei Sungrow SH-RT, abgewandelt von [mkaiser](https://github.com/mkaiser/Sungrow-SHx-Inverter-Modbus-Home-Assistant) (dort gibt es neuere Versionen) |
| [zwei-wechselrichter/](home-assistant/zwei-wechselrichter/) | Summen und Energiefluss für zwei Wechselrichter |
| [sungrow-steuerung/](home-assistant/sungrow-steuerung/) | Hausakkus schalten und absichern: Zwangsladen mit Leistungsregelung, Akku halten, Notbremsen, Preis-Automatik |
| [ladeplan/](home-assistant/ladeplan/) | Hausakkus nach Tibber-Preis und PV-Prognose laden und halten, effektiven Strompreis verfolgen |
| [pv-ueberschuss/](home-assistant/pv-ueberschuss/) | Steckdose bei PV-Überschuss zuschalten |
| [senec-auswertung/](home-assistant/senec-auswertung/) | SENEC-Speicher: Live-Werte, Akku-Module und Energie pro Tag aus selbst aufsummierten Zählern |
| [heizung/](home-assistant/heizung/) | Heizkörper folgen dem Raumthermostat, Fenster offen → aus |
| [jalousien/](home-assistant/jalousien/) | Jalousien nach Sonnenstand, robust gegen WLAN-Aussetzer |
| [recorder/](home-assistant/recorder/) | Datenbank klein halten |
| [ha-config-git/](home-assistant/ha-config-git/) | HA-Konfiguration über ha-mcp ins Git spiegeln |

Mehr dazu in [home-assistant/README.md](home-assistant/README.md).

## Lizenz

[MIT](LICENSE): Kopieren, ändern, weitergeben — alles erlaubt, solange
der Copyright- und Lizenzhinweis mitkommt. Ohne Gewähr. Ausnahme:
`home-assistant/sungrow-modbus/` steht zusätzlich unter der MIT-Lizenz
des Originalautors ([LICENSE-mkaiser](home-assistant/sungrow-modbus/LICENSE-mkaiser)).
