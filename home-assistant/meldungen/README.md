# Meldungen aufs Handy

Wenige Meldungen für Fälle, in denen jemand selbst eingreifen muss. Sie gehen als Push-Meldung über die
Companion-App von Home Assistant aufs Handy.

## Die Meldungen

| Meldung | Wann | Warum |
|---|---|---|
| **Phasengrenze überschritten** | stärkste Phase am Netzzähler 1 Minute über 30 A | Die Lade-Automatik regelt nur die Hausakkus. Laden zusätzlich Autos oder läuft der Herd, kann eine Sicherung auslösen: Dann hilft nur selbst drosseln. |
| **Wassermelder** | ein Melder wechselt von trocken auf nass | Sofort, ohne Wartezeit. |
| **Fenster bei Kälte lange offen** | Fenster oder Außentür 30 Minuten offen und draußen unter 10 °C | Eine Meldung je Öffnung. |

Dazu gehört thematisch eine vierte: „Heizung: Raum wird trotz Aus wärmer" in [../heizung/](../heizung/).

## Push kommt auch unterwegs an

Die Companion-App muss Home Assistant dafür nicht von außen erreichen. Home Assistant schickt die Meldung
ausgehend an den Push-Dienst des Handys (über die Server von Home Assistant an Google bzw. Apple), und der stellt
sie zu, egal in welchem Netz das Handy gerade ist. Es braucht also weder Portfreigabe noch VPN noch ein
Cloud-Abo. Nur wer in der Meldung auf etwas tippt, das die App öffnet, braucht dann eine Verbindung nach Hause.

## Was dabei hilft

- **Wenige, wichtige Meldungen.** Jede Meldung hier verlangt eine Handlung. Was nur interessant ist, gehört ins
  Dashboard, sonst liest bald niemand mehr die Meldungen.
- **Nicht nach einem Funkausfall melden.** Die Trigger verlangen den Wechsel von `off` auf `on`. Ein Melder, der
  nach einem Ausfall mit „nass" oder „offen" zurückkommt, löst nichts aus. Bei der Phasengrenze prüft eine
  Bedingung, dass der Sensor vorher einen gültigen Wert hatte.
- **Eine Meldung je Fall.** Die Phasengrenze meldet erst wieder, wenn die Phase zwischendurch unter 30 A war.
- **Ordnung:** In Home Assistant lassen sich alle Meldungen in einer Automations-Kategorie „Meldungen"
  zusammenfassen, siehe [../README.md](../README.md).

## Dateien

| Datei | Inhalt |
|---|---|
| `automations_meldungen.yaml` | die drei Automationen |

## Voraussetzungen und Anpassen

- Companion-App auf dem Handy. Sie legt den Dienst `notify.mobile_app_<gerätename>` an; in der Datei steht dafür
  der Platzhalter `notify.mobile_app_DEIN_HANDY`.
- **Phasengrenze:** `sensor.netz_max_phasenstrom` kommt aus [../sungrow-steuerung/](../sungrow-steuerung/),
  `sensor.import_power` aus [../sungrow-modbus/](../sungrow-modbus/) und `sensor.autoladeleistung` aus
  [../ladeplan/](../ladeplan/). Ohne diese Vorlagen einen eigenen Sensor für den Phasenstrom nehmen und den
  Meldungstext kürzen.
- **Wassermelder und Fenster:** die Listen der `binary_sensor` durch die eigenen ersetzen. Der Hersteller ist
  beliebig.
- **Außentemperatur:** `weather.forecast_home_assistant` durch die eigene Wetter-Entität ersetzen.
- Die Schwellen (30 A, 10 °C, 30 Minuten) sind Beispielwerte.
