#!/usr/bin/env bash
set -euo pipefail
COL="collections/metabolomics/v2"
python3 scripts/build_grounding_bundle.py --unit "$COL" --collection "$COL"
for d in packs/metabolomics/*/; do
  python3 scripts/build_grounding_bundle.py --unit "$d" --collection "$COL"
done
echo "grounding emitted into full collection + $(ls -d packs/metabolomics/*/ | wc -l | tr -d ' ') packs"
