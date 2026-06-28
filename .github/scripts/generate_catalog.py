#!/usr/bin/env python3
"""Generate OpenRouter model catalog from live /v1/models endpoint."""
import json
import urllib.request
import datetime
from pathlib import Path


def main():
    url = "https://openrouter.ai/api/v1/models"
    print(f"Fetching {url}...")
    with urllib.request.urlopen(url, timeout=30) as resp:
        data = json.loads(resp.read().decode())

    models = []
    for item in data.get("data", []):
        if not isinstance(item, dict):
            continue
        mid = str(item.get("id") or "").strip()
        if not mid:
            continue
        # Filter: must support tools (hermes requires tool calling)
        params = item.get("supported_parameters")
        if isinstance(params, list) and "tools" not in params:
            continue
        # Free detection
        pricing = item.get("pricing", {})
        try:
            free = float(pricing.get("prompt", "0")) == 0 and float(pricing.get("completion", "0")) == 0
        except (TypeError, ValueError):
            free = False
        models.append({"id": mid, "description": "free" if free else ""})

    # Sort: free first, then alphabetical
    models.sort(key=lambda m: (m["description"] != "free", m["id"].lower()))

    catalog = {
        "version": 1,
        "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z"),
        "metadata": {"source": "auto-generated from OpenRouter /v1/models via GitHub Actions"},
        "providers": {
            "openrouter": {
                "metadata": {"display_name": "OpenRouter (Full Auto-Updated)"},
                "models": models
            }
        }
    }

    output = Path("model-catalog.json")
    output.write_text(json.dumps(catalog, indent=2, ensure_ascii=False) + "\n")
    print(f"Generated {len(models)} models -> {output}")


if __name__ == "__main__":
    main()