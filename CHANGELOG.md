# Änderungen

Was sich an den Vorlagen geändert hat, das Neueste zuerst. Jeder Eintrag nennt den Ordner: Wer eine Vorlage
kopiert hat, sieht so, ob sich daran etwas getan hat.

Releases heißen nach Jahr, Monat und laufender Nummer (`2026.11.0`) und bündeln die Einträge seit dem letzten
Release. Die Nummer sagt nichts über Kompatibilität: Die Ordner sind unabhängig voneinander.

## 2026.11.0 (2026-11-14)

Erstes Release mit dem gesamten Stand bis hierher.

### 2026-11-14

#### Behoben

- **home-assistant/sungrow-steuerung:** Die Preis-Automatik brach ab und lud nicht, wenn der Ladeplan einen
  Ziel-SoC unter 20 % lieferte (Fehler „Invalid value for input_number.zwangsladen_ziel_soc"). Der Helfer
  `zwangsladen_ziel_soc` erlaubt jetzt ab 5 % (`helfer_sungrow.yaml`), und „Laden nach Plan" begrenzt den Wert
  auf den Bereich des Helfers (`automations_preis_automatik.yaml`).
  Wer die Dateien schon übernommen hat: beide Änderungen nachziehen. Bei UI-Helfern das Minimum dort senken.

### 2026-11-13

#### Neu

- **home-assistant:** Erste Home-Assistant-Vorlagen: `sungrow-modbus`, `zwei-wechselrichter`,
  `sungrow-steuerung`, `ladeplan`, `pv-ueberschuss`, `heizung`, `jalousien`, `recorder` und `ha-config-git`.
- **home-assistant/senec-auswertung:** Dashboard-Ansicht für einen SENEC.Home-Speicher mit Live-Werten,
  Ladestand je Akku-Modul und Energie pro Tag. Die Tagesenergie kommt aus sechs Integral-Helfern, die die
  Leistungswerte selbst aufsummieren.

#### Geändert

- **home-assistant/zwei-wechselrichter:** Neues Bild der Energiefluss-Karte unter Last.
  `bilder/energiefluss.png` ersetzt `bilder/energiefluss_nacht.png`.
- **home-assistant (mehrere Ordner):** READMEs und Kommentare allgemeiner formuliert, Werte in den Kommentaren
  als Beispiele gekennzeichnet. Keine Änderung an der Konfiguration.

### 2026-11-12

#### Neu

- **claude-orchestrator:** Modell-Setup und Agents-Vorlage für Claude Code.
- **Lizenz:** MIT.
