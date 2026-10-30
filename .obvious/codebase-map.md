# Codebase map — pauloes-btechs/pauloes-btechs

| Path | What it is | Notes |
|---|---|---|
| `README.md` | The profile README itself | Rendered on github.com/pauloes-btechs; edit content directly |
| `gen_assets.py` | Generates all 20 SVGs in `assets/` | Pure stdlib; writes to `<script_dir>/pauloes-btechs/assets` (run from parent dir) |
| `scripts/build_stats.py` | Builds tracker SVGs (stats, languages, heatmap, commits) | `--mock` flag for local dev without a token; real mode hits the GitHub API |
| `publish.sh` | One-shot commit/push helper | Requires `gh` CLI authenticated; not used in CI |
| `assets/` | 20 committed SVGs referenced by README | Regenerate via `gen_assets.py`; deterministic output |
| `.github/workflows/tracker.yml` | Activity tracker CI | Cron every 6h + push to `main`; publishes SVGs to `output` branch |
| `.gitignore` | Ignores `.DS_Store`, `._*`, `preview/` | `.obvious/` is not ignored |
