---
name: local-dev
description: How to bring pauloes-btechs/pauloes-btechs to a working local dev state
---

# local-dev

Recorded during onboarding setup (2026-10-30). This repo is a GitHub profile
README — there is no app server or database. Dev-stack health means the two
Python scripts run and produce valid SVGs.

## Environment

- Python 3 (stdlib only; nothing to install). Verified with 3.13; CI uses 3.12.
- No env vars or secrets needed for local work (`--mock` mode covers the
  tracker without a GitHub token).
- No services to start; nothing listens on a port.

## Steps

1. Sanity-compile both scripts:
   `python3 -m py_compile gen_assets.py scripts/build_stats.py`
2. Build tracker cards with mock data:
   `GH_USER=pauloes-btechs python3 scripts/build_stats.py --mock`
   → expect `dist/stats.svg`, `dist/languages.svg`, `dist/heatmap.svg`,
   `dist/commits.svg`; all parse as valid XML. Clean up `dist/` afterwards.
3. Asset regeneration check — `gen_assets.py` hardcodes its output to
   `<script_dir>/pauloes-btechs/assets`, so from a fresh clone run:
   `cp gen_assets.py ../gen_assets.py && (cd .. && python3 gen_assets.py) && rm ../gen_assets.py`
   → expect 20 SVGs written, byte-identical to the committed `assets/` files.
4. Optional visual proof: `convert dist/stats.svg /tmp/proof-stats.png`.

## Gotchas

- Do not "fix" the `pauloes-btechs/` path in `gen_assets.py` without asking —
  the script is also run from the desktop folder layout described in
  `publish.sh`, where the repo dir is named `pauloes-btechs`.
- Never commit `dist/` or `__pycache__/` (not currently gitignored — clean up
  after runs).
- Tracker SVGs live on the `output` branch, not `main`; never copy them into
  `assets/`.

## Validation Summary

- `py_compile`: pass on both scripts.
- `build_stats.py --mock`: pass — 4 SVGs, valid XML, rasterized to PNG.
- `gen_assets.py`: pass — 20/20 SVGs byte-identical to committed assets.
- `dev_stack_healthy: true`. No blockers.
