#!/usr/bin/env bash
# Build the pinned analysis environment at environment/env/, from lock.txt.
# RESOLVE=1 re-resolves environment.yml's dependencies and rewrites lock.txt instead.
#
# environment.yml is read here with a deliberately narrow parser: `python: "X.Y"` and the
# `  - package  # comment` lines under `dependencies:`. Keep the file in that shape.
set -euo pipefail
cd "$(dirname "$0")/.."

SPEC="environment/environment.yml"
ENV_DIR="environment/env"
LOCK="environment/lock.txt"

PY="$(sed -n 's/^python:[[:space:]]*"\{0,1\}\([0-9.]*\)"\{0,1\}.*/\1/p' "$SPEC" | head -1)"
PY="${PY:-3.13}"
# Dependency lines: "  - name[constraint]  # comment", uncommented only.
DEPS=()
while IFS= read -r dep; do
    [[ -n "$dep" ]] && DEPS+=("$dep")
done < <(sed -n 's/^[[:space:]]*-[[:space:]]*\([^#[:space:]][^#]*\).*/\1/p' "$SPEC" | sed 's/[[:space:]]*$//')

command -v uv >/dev/null || { echo "uv is required (https://docs.astral.sh/uv/)"; exit 1; }

rm -rf "$ENV_DIR"
uv venv --python "$PY" "$ENV_DIR" >/dev/null

if [[ "${RESOLVE:-}" == "1" || ! -f "$LOCK" ]]; then
    if [[ ${#DEPS[@]} -gt 0 ]]; then
        uv pip install --python "$ENV_DIR/bin/python" "${DEPS[@]}"
    else
        echo "NOTE: $SPEC lists no dependencies; writing an empty $LOCK"
    fi
    uv pip freeze --python "$ENV_DIR/bin/python" > "$LOCK"
    echo "Resolved and wrote $LOCK (${#DEPS[@]} requested, $(wc -l < "$LOCK" | tr -d ' ') pinned)"
else
    if [[ -s "$LOCK" ]]; then
        uv pip install --python "$ENV_DIR/bin/python" -r "$LOCK"
    fi
    built="$(uv pip freeze --python "$ENV_DIR/bin/python" | sort)"
    locked="$(sort "$LOCK")"
    if [[ "$built" != "$locked" ]]; then
        echo "WARNING: built environment differs from $LOCK:"
        diff <(echo "$locked") <(echo "$built") || true
    else
        echo "Built environment matches $LOCK exactly."
    fi
fi

"$ENV_DIR/bin/python" -V
