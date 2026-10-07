#!/usr/bin/env bash
# Make a claude.ai Artifact copy of a built page. The Artifact host adds its own doctype, head and
# body (with safe-area padding), so drop ours and keep the rest.
#   scripts/artifact.sh dist/konbini-ears-ja-service.html > dist/konbini-ears.html
set -euo pipefail
sed -e '/^<!doctype html>$/d' -e '/^<html lang="en">$/d' -e '/^<\/\?head>$/d' -e '/^<\/\?body>$/d' \
    -e '/^<\/html>$/d' -e '/<meta charset="utf-8">/d' -e '/<meta name="viewport"/d' \
    -e 's/^\(body { font: .*sans-serif;\)$/\1 background: var(--bg);/' \
    -e 's/^       padding: env(safe-area-inset-top) 0 /       padding: 0 0 /' "$1"
