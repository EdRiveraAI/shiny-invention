#!/usr/bin/env bash
# Run the tests, then build the customer zip: dist/ship-check-<version>.zip
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"

version="$(python3 skills/ship-check/scripts/scan.py --version | awk '{print $2}')"
python3 -m unittest discover -s tests

stage="$(mktemp -d)"
trap 'rm -rf "$stage"' EXIT
pkg="${stage}/ship-check"
mkdir -p "$pkg"
cp -R .claude-plugin skills install.sh README.md LICENSE.md CHANGELOG.md "$pkg/"
find "$pkg" -name '__pycache__' -prune -exec rm -rf {} +

mkdir -p dist
out="$(pwd)/dist/ship-check-${version}.zip"
rm -f "$out"
(cd "$stage" && zip -qr "$out" ship-check)
echo "Built ${out}"
