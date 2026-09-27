#!/usr/bin/env bash
set -euo pipefail

# Build final presentation package
# Usage: ./scripts/build_final.sh [--finals]
#
# Without --finals: builds preparation version (latest snapshot)
# With --finals: builds frozen finals version with manifest

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PRES_DIR="$REPO_ROOT/presentation"
BUILD_DIR="$PRES_DIR/dist"
VARIANT="preparation"

if [[ "${1:-}" == "--finals" ]]; then
    VARIANT="finals"
fi

echo "=== Building presentation ($VARIANT) ==="

# Step 1: Install dependencies
cd "$PRES_DIR"
if [[ ! -d node_modules ]]; then
    echo "Installing dependencies..."
    npm install
fi

# Step 2: Build static HTML
echo "Building static HTML..."
# Base "/" so `python3 -m http.server` from dist/ resolves assets (no Pages deploy)
npx slidev build slides.md --base / --out dist

# Offline guard: finals must not load anything from the network
if grep -rEoh '(href|src)="https?://[^"]+"' dist --include='*.html' --include='*.css'; then
    echo "ERROR: external resources in dist/ (listed above) — build is not offline-safe" >&2
    exit 1
fi
if grep -rEoh 'url\((https?:)?//[^)]+\)|@import ["'"'"']?https?://' dist --include='*.css' --include='*.js'; then
    echo "ERROR: external CSS resources in dist/ (listed above)" >&2
    exit 1
fi

# Step 3: If finals variant, stamp manifest
if [[ "$VARIANT" == "finals" ]]; then
    echo "Stamping finals manifest..."
    COMMIT=$(git -C "$REPO_ROOT" rev-parse HEAD)
    BUILT_AT=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    SNAPSHOT=$(python3 -c "import json; print(json.load(open('deck.json'))['snapshot'])")

    python3 -c "
import json, sys
m = json.load(open('manifest.json'))
m['presentationCommit'] = '$COMMIT'
m['builtAt'] = '$BUILT_AT'
m['snapshot'] = '$SNAPSHOT'
m['variant'] = 'finals'
json.dump(m, open('manifest.json', 'w'), indent=2)
print('Manifest stamped:', json.dumps(m, indent=2))
"

    # Copy manifest into dist
    cp manifest.json dist/manifest.json
fi

# Step 4: Copy snapshot into dist for offline access
SNAPSHOT_FILE=$(python3 -c "import json; print('snapshots/' + json.load(open('deck.json'))['snapshot'] + '.json')")
if [[ -f "$SNAPSHOT_FILE" ]]; then
    cp "$SNAPSHOT_FILE" dist/
    echo "Snapshot copied to dist/"
fi

echo ""
echo "=== Build complete ==="
echo "  Output: $BUILD_DIR/"
echo "  Variant: $VARIANT"
echo ""
echo "To test offline:"
echo "  cd $BUILD_DIR && python3 -m http.server 8080"
echo "  Open http://localhost:8080 (disconnect network to verify)"
