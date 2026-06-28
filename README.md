# Hermes OpenRouter Full Model Catalog

Auto-generated, daily-updated model catalog for Hermes Agent's model picker — includes **all** OpenRouter models that support tool calling (not just the curated ~35).

## What this does

- Fetches `https://openrouter.ai/api/v1/models` every 6 hours via GitHub Actions
- Filters for models with `supported_parameters` containing `tools` (required by Hermes)
- Detects free models from pricing data
- Publishes `model-catalog.json` to GitHub Pages
- Hermes reads this URL via `model_catalog.providers.openrouter.url` config

## Quick Start

### 1. Fork this repository

Click **Fork** → your GitHub account → `hermes-openrouter-catalog`

### 2. Enable GitHub Pages

In your fork: **Settings → Pages → Source: Deploy from branch → `main` / `/ (root)` → Save**

Your catalog URL will be:
```
https://YOUR-USERNAME.github.io/hermes-openrouter-catalog/model-catalog.json
```

### 3. Configure Hermes

In `~/.hermes/config.yaml` (or via `hermes setup`):

```yaml
model_catalog:
  enabled: true
  url: "https://YOUR-USERNAME.github.io/hermes-openrouter-catalog/model-catalog.json"
  ttl_hours: 1
  providers: {}
```

Restart Hermes or run `hermes model --refresh`.

### 4. Done

The model picker now shows **all 200+ tool-capable OpenRouter models**, with free models listed first and marked "free". Prices are fetched live from OpenRouter when you open the picker.

## Manual Trigger

Actions → **Update OpenRouter Model Catalog** → **Run workflow**

## Local Test

```bash
python3 .github/scripts/generate_catalog.py
cat model-catalog.json | jq '.providers.openrouter.models | length'
```

## Customization

Edit `.github/scripts/generate_catalog.py` to change:
- Filtering logic (e.g. include vision-only models)
- Sorting
- Description format
- Add other providers (Nous, etc.)

## License

MIT — do whatever you want.