# PV-Überschuss: Steckdose zuschalten

Zwei Automationen schalten eine Steckdose (hier „Prio 2" genannt, z. B. für einen Heizlüfter oder Akkulader) bei
PV-Überschuss ein und wieder aus:

- **an**, wenn die PV-Leistung (DC) 5 Minuten lang mehr als **2,5 kW** über dem Hausverbrauch ohne Wallbox liegt
- **aus**, wenn der Überschuss 5 Minuten lang unter **200 W** fällt

Die große Lücke zwischen den Schwellen verhindert Flattern: Läuft das Gerät, verbraucht es selbst einen Teil des
Überschusses und soll trotzdem an bleiben.

## Einbinden

`automations_pv_ueberschuss.yaml` als Package einbinden (`homeassistant: packages: !include_dir_named packages`).
Dann sind die Automationen in der UI nur lesbar. Alternativ jede einzeln in der UI anlegen und per „In YAML
bearbeiten" einfügen.

Anpassen: `switch.pv_steckdose_prio2` durch die eigene Steckdose ersetzen, Schwellen an deren Leistung anpassen.
`sensor.sum_total_dc_power` und `sensor.house_without_wallbox_power` kommen aus
[../zwei-wechselrichter/](../zwei-wechselrichter/). Mit einem Wechselrichter dessen PV- und Lastsensor nehmen.

Für mehrere Steckdosen mit Rangfolge: weitere Paare mit höheren Schwellen anlegen (Prio 3 erst ab mehr Überschuss).
