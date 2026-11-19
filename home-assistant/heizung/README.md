# Heizung: Heizkörper folgen dem Raumthermostat

Je Raum ein Wandthermostat (misst und gibt den Sollwert vor, mit Wochenprogramm) und ein Heizkörperthermostat
(Homematic / Homematic IP). Home Assistant öffnet den Heizkörper, wenn der Raum zu kalt ist, und schließt ihn,
sobald er warm genug ist oder ein Fenster aufgeht.

<img src="bilder/wohnzimmer.png" width="420" alt="Dashboard: Raumthermostat Wohnzimmer, Balkontür und Heizkörper">

## Wie es regelt

- Heizkörper auf (Soll + 3 °C, höchstens 26 °C), sobald der Raum 0,3 °C unter Soll liegt; zu, sobald er 0,1 °C
  darüber liegt. Dazwischen bleibt der letzte Zustand (Hysterese). Gesendet wird nur, wenn sich etwas ändern muss.
- Fenster oder Tür offen → Heizkörper aus. Ein Raum kann mehrere Kontakte haben, zum Beispiel die Küche ohne
  eigene Heizung, die zum Wohnzimmer offen ist.
- Manuelles Verstellen am Wandthermostat gilt **2 Stunden**, danach zurück aufs Wochenprogramm. Solange ein Fenster
  offen ist, ruht dieser Timer. Sonst verbraucht das Lüften die 2 Stunden.
- Neuere HmIP-Thermostate kennen kein „Aus" und gehen auf 5 °C. Das zählt ebenfalls als zu.
- Zwei Absicherungen gegen per Funk verlorene Befehle, je höchstens alle 15 Minuten:
  - **Aus wiederholen:** Der Heizkörper zeigt „Aus", der Raum liegt aber mindestens 1 °C über Soll und der Fühler
    am Heizkörper mindestens 0,8 °C über dem Raum. Sonst heizt er unbemerkt weiter.
  - **Ein wiederholen:** Der Heizkörper zeigt „Heizen", der Raum liegt aber mindestens 1 °C unter Soll und der
    Fühler am Heizkörper höchstens 0,3 °C über dem Raum. Nur bei unter 15 °C Außentemperatur, weil die Heizung
    sonst ohnehin nicht läuft.

  Die Außentemperatur kommt aus `weather.forecast_home_assistant`: durch die eigene Wetter-Entität ersetzen,
  die 15 °C sind ein Vorschlag. Die Raum-Automationen laufen dafür alle 5 Minuten.
- **Raum wird trotz Aus wärmer:** Ein Trend-Helfer je Raum meldet, wenn die Raumtemperatur um mehr als 0,3 °C
  je Stunde steigt. Steht der Heizkörper dabei auf „Aus", liegt der Raum mindestens 1 °C über Soll und hat es
  draußen unter 15 °C, wird ebenfalls „Aus" wiederholt, auch wenn der Fühler am Heizkörper kaum wärmer ist als
  der Raum. Hält das 30 Minuten an, kommt eine Meldung aufs Handy: Bei einem Ventil, das mechanisch nicht
  schließt, hilft Wiederholen nicht.

## Dateien

| Datei | Inhalt |
|---|---|
| `automations_heizung.yaml` | je Raum eine Automation, dazu „Soll nach 2 h zurück aufs Programm" und die Meldung „Raum wird trotz Aus wärmer" |
| `scripts_heizung.yaml` | `heizung_raum_regeln`: die Regelung eines Raums (Thermostat, Heizkörper, Fenster, Timer, Trend-Helfer) |
| `helfer_heizung.yaml` | die 2-Stunden-Timer und die Trend-Helfer „Raumtemperatur steigt" |

Neuer Raum: eine Automation kopieren, Thermostate und Fenster eintragen, Timer und Trend-Helfer anlegen und in
„Soll nach 2 h zurück" sowie in „Raum wird trotz Aus wärmer" (Trigger und `raeume`) ergänzen.

Für die Meldung `notify.mobile_app_DEIN_HANDY` durch den Meldedienst des eigenen Handys ersetzen.
