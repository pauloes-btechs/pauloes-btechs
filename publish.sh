#!/usr/bin/env bash
# One-shot publish of the profile README to github.com/pauloes-btechs/pauloes-btechs
#
# Prereqs (once):  brew install gh && gh auth login
# Usage:           cd into this folder, then:  bash publish.sh
set -euo pipefail

USER="pauloes-btechs"
REPO="$USER/$USER"      # profile READMEs must live in a public repo named after the username

cd "$(dirname "$0")"

if ! command -v gh >/dev/null; then
  echo "GitHub CLI not found. Install with: brew install gh   then: gh auth login"; exit 1
fi
gh auth status >/dev/null 2>&1 || { echo "Run: gh auth login   (choose GitHub.com → HTTPS → login with browser)"; exit 1; }

# 1. Create the special repo if it doesn't exist yet (must be PUBLIC to show on the profile)
if ! gh repo view "$REPO" >/dev/null 2>&1; then
  echo "Creating $REPO ..."
  gh repo create "$REPO" --public --description "Profile README" >/dev/null
fi

# 2. Init + push
if [ ! -d .git ]; then
  git init -q -b main
fi
git add -A
git -c user.email="pauloes@btechs.io" -c user.name="Pauloes Berhe" \
    commit -q -m "Profile README: btechs.io palette, link tabs, featured projects, timeline, stack, stats" || echo "(nothing new to commit)"
git remote get-url origin >/dev/null 2>&1 || git remote add origin "https://github.com/$REPO.git"
git push -u origin main

# 3. Kick the contribution-snake workflow once so the image exists immediately
gh workflow run snake.yml -R "$REPO" >/dev/null 2>&1 && echo "Snake workflow triggered (takes ~1 min)." || true

echo
echo "Done → https://github.com/$USER"
