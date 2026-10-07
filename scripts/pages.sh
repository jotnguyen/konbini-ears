#!/usr/bin/env bash
# Publish a built pack to GitHub Pages (the gh-pages branch): the page as index.html, the offline
# service worker, and the Anki deck. Run after scripts/build.sh, with dist/ holding the outputs.
#   scripts/pages.sh ja-service
set -euo pipefail
cd "$(dirname "$0")/.."
PACK=${1:-ja-service}
SRC=$PWD
TMP=$(mktemp -d)/site     # git worktree wants a path that does not exist yet
trap 'git -C "$SRC" worktree remove --force "$TMP" 2>/dev/null || true' EXIT

git fetch -q origin gh-pages 2>/dev/null || true
if git show-ref -q --verify refs/remotes/origin/gh-pages; then
  git worktree add -q -B gh-pages "$TMP" origin/gh-pages
else
  git worktree add -q --orphan -b gh-pages "$TMP"
fi
cp "dist/konbini-ears-$PACK.html" "$TMP/index.html"
cp web/sw.js "$TMP/sw.js"
cp "dist/konbini-ears-$PACK.apkg" "$TMP/konbini-ears.apkg"
touch "$TMP/.nojekyll"
cd "$TMP"
git add -A
git diff --cached --quiet && { echo "pages: nothing changed"; exit 0; }
git commit -q -m "pages: $PACK built $(date -u +%Y-%m-%dT%H:%MZ)"
git push -q origin gh-pages
echo "pages: pushed"
