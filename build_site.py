#!/usr/bin/env python3
"""
rose.tech site builder
-----------------------
Reads entries.json + template.html and writes a self-contained index.html
with the data inlined (so it opens reliably by double-click, no server needed).

Run after adding new entries:  python3 build_site.py
"""
import json, sys, datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / "entries.json"
TEMPLATE = HERE / "template.html"
OUTPUT = HERE / "index.html"
PLACEHOLDER = "__DATA_JSON__"

def main():
    if not DATA.exists():
        sys.exit(f"❌ Missing {DATA.name}")
    if not TEMPLATE.exists():
        sys.exit(f"❌ Missing {TEMPLATE.name}")

    data = json.loads(DATA.read_text(encoding="utf-8"))

    entries = data.get("entries", [])
    # sort newest first, stable by id
    entries.sort(key=lambda e: (e.get("date", ""), e.get("id", "")), reverse=True)
    data["entries"] = entries

    # keep the site "updated" stamp honest = newest entry date (fallback: today)
    newest = entries[0]["date"] if entries else datetime.date.today().isoformat()
    data.setdefault("site", {})
    data["site"]["updated"] = newest

    template = TEMPLATE.read_text(encoding="utf-8")
    if PLACEHOLDER not in template:
        sys.exit(f"❌ {TEMPLATE.name} is missing the {PLACEHOLDER} placeholder")

    payload = json.dumps(data, ensure_ascii=False)
    html = template.replace(PLACEHOLDER, payload)
    OUTPUT.write_text(html, encoding="utf-8")

    cats = {}
    for e in entries:
        cats[e.get("category", "?")] = cats.get(e.get("category", "?"), 0) + 1
    print(f"✅ Built {OUTPUT.name}: {len(entries)} entries, {len(data.get('glossary', []))} glossary terms.")
    print(f"   Newest date: {newest}")
    print("   By category: " + ", ".join(f"{k} ({v})" for k, v in cats.items()))

if __name__ == "__main__":
    main()
