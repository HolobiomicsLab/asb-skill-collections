#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 3 ] || [ "$#" -gt 5 ]; then
  echo "usage: $0 <tooling-root> <content-root> <collection_path> [receipts_path] [--strict]" >&2
  exit 2
fi

tooling="$(cd "$1" && pwd)"
content="$(cd "$2" && pwd)"
collection="$3"
receipts="${4:-}"
strict=0
if [ "${5:-}" = "--strict" ]; then
  strict=1
elif [ "$#" -eq 5 ]; then
  echo "the fifth argument must be --strict" >&2
  exit 2
fi

python="${PYTHON:-python3}"
mode=(--no-strict)
if [ "$strict" -eq 1 ]; then
  mode=(--strict)
fi

export PYTHONDONTWRITEBYTECODE=1
exec "$python" "$tooling/scripts/domain_content_gates.py" \
  --tooling "$tooling" --content "$content" --collection "$collection" \
  --receipts "$receipts" --offline "${mode[@]}"
