# AGENTS.md — Operating Contract for pauloes-btechs

## Purpose

This is the GitHub profile repository for **pauloes-btechs**. GitHub renders
`README.md` on the profile overview only when the repo is public and named
exactly like the username — the name is load-bearing, never rename it. All
visuals are generated SVGs; there is no package.json or requirements.txt.

## Conventions

- **Assets are generated, never hand-edited.** Everything under `assets/` is
  produced by `gen_assets.py` (SVG, Python stdlib only). To change a visual,
  edit `gen_assets.py`, re-run it, and commit the regenerated SVGs together
  with the script change.
- **README edits are HTML-in-Markdown** (`<table>`, `<div>`, `<img>` blocks)
  with `<!-- section -->` comment dividers. Keep that structure; don't convert
  to plain Markdown.
- **Commit style:** conventional commits (`docs:`, `fix:`, `feat:`).
- **Committing `publish.sh` artifacts:** `publish.sh` is the one-shot local
  publish helper — do not run it from automation; it pushes directly to `main`.
- The `.github/workflows/tracker.yml` workflow regenerates stat cards and the
  contribution snake onto the `output` branch every 6 hours and on push to
  `main`. Don't touch workflow files in doc/asset changes.

## Verify commands

Run from the repo root:

```bash
python3 gen_assets.py          # regenerates all SVGs into assets/ — must exit 0
git diff --stat assets/        # confirms which SVGs changed
```

There is no linter, test suite, or dependency manifest in this repo. CI is the
**Activity tracker** workflow (`.github/workflows/tracker.yml`); it runs on
push to `main`, not on PRs, so a green local `gen_assets.py` run is the
primary gate for asset changes.

**Known quirk:** `gen_assets.py` writes to `dirname(gen_assets.py)/pauloes-btechs/assets/`
— one level deeper than the repo's own `assets/`. If you run it from the repo
root it exits 0 but leaves an untracked nested `pauloes-btechs/` directory;
delete it (`rm -rf pauloes-btechs/`). Do not "fix" the path as a side effect
of another change — that changes committed assets.

## Done criteria

- `python3 gen_assets.py` exits 0, and any regenerated SVGs you intend to ship
  are committed (script change + regenerated assets in the same commit).
- README renders correctly: section markers, image paths in `assets/`, and
  link tabs intact.
- Tracker workflow green after merge to `main` (check the Actions tab).

## Escalation rules

Work autonomously and return only when done or genuinely blocked. Specifically:

1. **No early returns.** Do not stop to ask for confirmation on steps you can
   verify yourself — run the verify commands, observe the results, and
   continue until the done criteria are met or a human decision is required.
2. **No silent scope expansion.** If you find an adjacent problem (broken link,
   stale card, the `gen_assets.py` path quirk above), flag it in your report or
   PR body — do not fix it unasked.
3. **No unverified completion.** Never report done without having run the
   verify commands in this session and observed them pass.

**Repo safety override (takes precedence over the above):** never push
directly to `main`, never run `publish.sh`, never modify workflow files or
secrets, and never rename the repository. Escalate anything that requires
those actions as a human decision.
