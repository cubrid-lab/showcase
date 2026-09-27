#!/usr/bin/env bash
set -euo pipefail

# Export presentation as PDF
# Usage: ./scripts/export_pdf.sh
#
# Requires: playwright (installed by slidev export)

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PRES_DIR="$REPO_ROOT/presentation"

cd "$PRES_DIR"

if [[ ! -d node_modules ]]; then
    echo "Installing dependencies..."
    npm install
fi

# Install playwright if needed
npx playwright install chromium 2>/dev/null || true

echo "Exporting PDF..."
npx slidev export slides.md --output slides.pdf --timeout 60000

if [[ -f slides.pdf ]]; then
    echo "PDF exported: $PRES_DIR/slides.pdf"
    echo "Pages: $(python3 -c "
try:
    # Quick page count via file size estimate
    import os
    size_mb = os.path.getsize('slides.pdf') / 1024 / 1024
    print(f'{size_mb:.1f} MB')
except: print('unknown size')
")"
else
    echo "PDF export failed" >&2
    exit 1
fi
