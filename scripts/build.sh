#!/usr/bin/env bash
# Lint a pack, record its audio, and build the phone page + Anki deck into dist/.
# Needs Docker and the speech-kit:local image (github.com/jotnguyen/speech-kit).
#   scripts/build.sh check packs/ja-service.yaml
#   scripts/build.sh build packs/ja-service.yaml
set -euo pipefail
cd "$(dirname "$0")/.."

IMAGE=${KE_IMAGE:-konbini-ears:local}
docker image inspect "$IMAGE" >/dev/null 2>&1 || docker build -t "$IMAGE" .

# Capped so a build never starves other services sharing the host.
docker run --rm --cpus "${KE_CPUS:-2}" --memory "${KE_MEM:-4g}" \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD":/work -w /work "$IMAGE" "$@"
