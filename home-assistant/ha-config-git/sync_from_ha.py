"""Mirror the current Home Assistant configuration into this repository.

Reads the files through the ha-mcp server (File & YAML Tools) and exports the
storage-mode dashboards as JSON. Home Assistant stays the source of truth; this
repo is only the version history.

Usage:  python tools/sync_from_ha.py
The MCP URL (contains the secret path) is read from the environment variable
HA_MCP_URL or from the git-ignored file `.ha_mcp_url` in the repo root.

secrets.yaml is never read or written; the repo keeps its own dummy copy.
"""
import json
import os
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HEADERS = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}

# Files and directories mirrored 1:1 from /config
FILES = ["configuration.yaml", "automations.yaml", "scripts.yaml", "scenes.yaml"]
DIRS = ["integrations", "blueprints", "custom_templates"]
NEVER = {"secrets.yaml"}


def mcp_url():
    url = os.environ.get("HA_MCP_URL")
    if not url and (ROOT / ".ha_mcp_url").exists():
        url = (ROOT / ".ha_mcp_url").read_text(encoding="utf-8").strip()
    if not url:
        sys.exit("HA_MCP_URL not set and .ha_mcp_url missing")
    return url


def call(url, tool, args):
    body = {"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": tool, "arguments": args}}
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=HEADERS, method="POST")
    with urllib.request.urlopen(req, timeout=120) as r:
        raw = r.read().decode("utf-8")
    for line in raw.splitlines():
        if line.startswith("data: "):
            raw = line[6:]
            break
    res = json.loads(raw)
    if "error" in res:
        raise RuntimeError(f"{tool}: {res['error']}")
    text = res["result"]["content"][0]["text"]
    return json.loads(text)


def list_tree(url, path):
    """Yield all file paths below `path` (relative to /config)."""
    res = call(url, "ha_list_files", {"path": path.rstrip("/") + "/"})
    for f in res.get("files", []):
        p = f["path"]
        if f.get("is_dir"):
            yield from list_tree(url, p)
        else:
            yield p


def write(rel, content):
    target = ROOT / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    old = target.read_text(encoding="utf-8") if target.exists() else None
    if old != content:
        target.write_text(content, encoding="utf-8", newline="")
        print(("updated " if old is not None else "added   ") + rel)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    url = mcp_url()
    paths = list(FILES)
    for d in DIRS:
        paths += list(list_tree(url, d))
    for p in paths:
        if Path(p).name in NEVER:
            continue
        res = call(url, "ha_read_file", {"path": p})
        if not res.get("success", True) or res.get("content") is None:
            print(f"skipped {p}: {res.get('error')}")
            continue
        write(p, res["content"])

    dashboards = call(url, "ha_config_get_dashboard", {"list_only": True}).get("dashboards", [])
    for d in dashboards:
        if d.get("mode") != "storage":
            continue
        res = call(url, "ha_config_get_dashboard", {"url_path": d["url_path"], "force_reload": True})
        write(f"dashboards_storage/{d['url_path']}.json",
              json.dumps(res["config"], ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()
