#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUTPUT="$ROOT/src/andocgen/generated/config_models.py"
PYTHON="${PYTHON:-$ROOT/.venv/bin/python}"
CODEGEN="${CODEGEN:-$ROOT/.venv/bin/datamodel-codegen}"

if [[ ! -x "$PYTHON" ]]; then
  PYTHON="python3"
fi

if [[ ! -x "$CODEGEN" ]]; then
  CODEGEN="datamodel-codegen"
fi

mkdir -p "$(dirname "$OUTPUT")"

"$CODEGEN" \
  --input "$ROOT/config.schema.yaml" \
  --input-file-type jsonschema \
  --output "$OUTPUT" \
  --output-model-type pydantic_v2.BaseModel \
  --target-python-version 3.11 \
  --use-subclass-enum \
  --field-constraints \
  --disable-timestamp

"$PYTHON" <<PY
from pathlib import Path

path = Path("${ROOT}/src/andocgen/generated/config_models.py")
text = path.read_text(encoding="utf-8")
header = (
    "# AUTO-GENERATED from config.schema.yaml — do not edit manually.\n"
    "# Regenerate: ./scripts/generate_config_models.sh\n\n"
)
if not text.startswith("# AUTO-GENERATED"):
    path.write_text(header + text, encoding="utf-8")
PY
