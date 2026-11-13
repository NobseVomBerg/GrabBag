# Home-Assistant-Konfiguration ins Git spiegeln

`sync_from_ha.py` liest die Konfiguration über den MCP-Server [ha-mcp](https://github.com/homeassistant-ai/ha-mcp)
und schreibt sie in ein Git-Repo: `configuration.yaml`, `automations.yaml`, `scripts.yaml`, `scenes.yaml`, die Ordner
`integrations/` (Packages), `blueprints/`, `custom_templates/` und alle UI-Dashboards als JSON.
Home Assistant bleibt die Quelle, das Repo ist die Versionsgeschichte: was wann geändert wurde, mit Commit-Nachricht.

Passt gut zu Claude Code: Claude ändert über ha-mcp direkt in Home Assistant, ruft danach das Skript auf und committet.

## Einrichten

1. ha-mcp installieren und die **File & YAML Tools** einschalten (das Skript nutzt `ha_list_files`, `ha_read_file`
   und `ha_config_get_dashboard`).
2. Skript nach `tools/` im Repo legen. Die MCP-URL (mit geheimem Pfad) in die Umgebungsvariable `HA_MCP_URL` oder in die
   Datei `.ha_mcp_url` im Repo-Hauptordner schreiben und diese **in `.gitignore` eintragen**.
3. `python tools/sync_from_ha.py`, dann `git diff` ansehen und committen.

`secrets.yaml` wird nie gelesen oder geschrieben. Lege im Repo eine Dummy-`secrets.yaml` mit Platzhaltern an,
damit klar ist, welche Schlüssel es gibt. Was sonst nicht ins Repo gehört (`.storage/`, Datenbank, Logs):
siehe `.gitignore` eines HA-Config-Repos.

Das Modul liefert außerdem `mcp_url()` und `call(url, tool, args)` für eigene Skripte, z. B.
[../ladeplan/pv_historie.py](../ladeplan/pv_historie.py).
