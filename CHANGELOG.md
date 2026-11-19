# Änderungen

Was sich an den Vorlagen geändert hat, das Neueste zuerst. Jeder Eintrag nennt den Ordner: Wer eine Vorlage
kopiert hat, sieht so, ob sich daran etwas getan hat.

Releases heißen nach Jahr, Monat und laufender Nummer (`2026.11.0`) und bündeln die Einträge seit dem letzten
Release. Die Nummer sagt nichts über Kompatibilität: Die Ordner sind unabhängig voneinander.

## 2026.11.2 (2026-11-19)

### 2026-11-19

#### Neu

- **home-assistant/meldungen:** Neue Vorlage mit drei Push-Meldungen aufs Handy: Phasengrenze überschritten
  (stärkste Phase 1 Minute über 30 A), Wassermelder und Fenster bei Kälte lange offen (30 Minuten, draußen
  unter 10 °C). Die README erklärt, warum Push auch unterwegs ankommt, ohne dass Home Assistant von außen
  erreichbar ist.
- **home-assistant/heizung:** Erkennung „Raum wird trotz Aus wärmer". Ein Trend-Helfer je Raum
  (`helfer_heizung.yaml`, mehr als 0,3 °C je Stunde) zeigt, dass die Raumtemperatur steigt. Steht der
  Heizkörper dabei auf „Aus", wiederholt `heizung_raum_regeln` den Aus-Befehl auch dann, wenn der Fühler am
  Heizkörper kaum wärmer ist als der Raum (neues optionales Feld `steigt`). Hält der Zustand 30 Minuten an,
  meldet die neue Automation „Heizung: Raum wird trotz Aus wärmer" den Fall aufs Handy
  (`automations_heizung.yaml`), denn bei einem Ventil, das mechanisch nicht schließt, hilft Wiederholen nicht.
  Anzupassen: `notify.mobile_app_DEIN_HANDY` und `weather.forecast_home_assistant`.
  Wer die Dateien schon übernommen hat: Helfer, Skript und Automationen nachziehen; die vier
  Raum-Automationen übergeben zusätzlich `steigt`.

#### Behoben

- **home-assistant/heizung:** Ging ein Befehl an ein Heizkörperthermostat per Funk verloren, zeigte Home
  Assistant den neuen Zustand, der Heizkörper blieb aber im alten. Die Regelung sendet nur bei Änderungsbedarf
  und fasste deshalb nie nach. `heizung_raum_regeln` hat jetzt zwei Absicherungen, je höchstens alle 15 Minuten
  (`scripts_heizung.yaml`):
  - „Aus wiederholen": Der Heizkörper zeigt „Aus", der Raum liegt aber mindestens 1 °C über Soll und der Fühler
    am Heizkörper mindestens 0,8 °C über dem Raum.
  - „Ein wiederholen": Der Heizkörper zeigt „Heizen", der Raum liegt aber mindestens 1 °C unter Soll und der
    Fühler am Heizkörper höchstens 0,3 °C über dem Raum. Nur bei unter 15 °C Außentemperatur; dafür
    `weather.forecast_home_assistant` durch die eigene Wetter-Entität ersetzen.

  Die Raum-Automationen laufen dafür alle 5 statt alle 10 Minuten (`automations_heizung.yaml`).
  Wer die Dateien schon übernommen hat: beide Zweige, die Beschreibung und den Takt nachziehen. Ein zuerst
  veröffentlichter Zwischenstand wiederholte nur „Aus" und nur zur vollen und halben Stunde.

## 2026.11.1 (2026-11-18)

### 2026-11-18

#### Behoben

- **home-assistant/sungrow-steuerung:** „Preis-Automatik: Laden nach Plan" reagierte nur auf Zustandswechsel des
  Plans. Lehnte das Skript das Zwangsladen ab (Phasengrenze oder Netzbudget ausgeschöpft, z. B. weil ein Auto
  lädt), blieb es bis zum nächsten Wechsel ohne Ladung. Die Automation fasst jetzt alle 5 Minuten nach, solange
  der Plan laden will (`automations_preis_automatik.yaml`: neuer Trigger `nachfassen` und eine Bedingung dazu).
  Wer die Datei schon übernommen hat: Trigger, Bedingung und Beschreibung nachziehen.

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
