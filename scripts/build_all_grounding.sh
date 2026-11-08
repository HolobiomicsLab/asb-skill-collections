#!/usr/bin/env bash
set -euo pipefail
if [ "$#" -ne 2 ]; then
  echo "usage: $0 <domain-checkout> <collection-path>" >&2
  exit 2
fi
ROOT="$(cd "$1" && pwd)"
COL="$ROOT/$2"
if [ ! -d "$COL" ]; then
  echo "collection is not a directory: $COL" >&2
  exit 1
fi
python3 scripts/build_grounding_bundle.py --unit "$COL" --collection "$COL"
shopt -s nullglob
# The packs of the collection's domain: collections/<domain>/vN -> packs/<domain>/*/
DOMAIN="$(echo "$2" | cut -d/ -f2)"
packs=("$ROOT"/packs/"$DOMAIN"/*/)
shopt -u nullglob
for d in "${packs[@]}"; do
  python3 scripts/build_grounding_bundle.py --unit "$d" --collection "$COL"
done
echo "grounding emitted into full collection + ${#packs[@]} packs"
