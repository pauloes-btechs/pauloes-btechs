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

# 2. Workflow file: the desktop bridge can't write into .github/, so it ships at the repo root
#    and gets moved here. Also retire the old snake-only workflow (replaced by tracker.yml).
mkdir -p .github/workflows
[ -f tracker.yml ] && mv -f tracker.yml .github/workflows/tracker.yml
rm -f .github/workflows/snake.yml
# exFAT sidecars that macOS drops everywhere — never commit them
find . -name '._*' -not -path './.git/*' -delete 2>/dev/null || true

# 3. Init + push
if [ ! -d .git ]; then
  git init -q -b main
fi
git add -A
git -c user.email="pauloes@btechs.io" -c user.name="Pauloes Berhe" \
    commit -q -m "Profile README update: self-hosted activity tracker, snake fix, pauloes.com card link" || echo "(nothing new to commit)"
git remote get-url origin >/dev/null 2>&1 || git remote add origin "https://github.com/$REPO.git"
git push -u origin main

# 4. Kick the tracker once so the cards exist immediately
sleep 3; gh workflow run tracker.yml -R "$REPO" >/dev/null 2>&1 && echo "Tracker workflow triggered — cards appear in ~1-2 min." || true

echo
echo "Done → https://github.com/$USER"
