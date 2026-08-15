#!/usr/bin/env bash
# Run CycleX latest API Newman suite against a TEST Odoo 18 instance.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

if [[ ! -f CycleX.latest.local.postman_environment.json ]]; then
  echo "error: create CycleX.latest.local.postman_environment.json from the template" >&2
  exit 2
fi

if [[ ! -x ./node_modules/.bin/newman ]]; then
  npm install newman@^6 newman-reporter-htmlextra@^1
fi

mkdir -p report screenshots
STAMP="$(date +%Y%m%dT%H%M%S)"
NAME="cyclex-latest-${STAMP}"

set +e
./node_modules/.bin/newman run CycleX.latest.postman_collection.json \
  -e CycleX.latest.local.postman_environment.json \
  -k --timeout-request 30000 --delay-request 250 \
  -r cli,htmlextra,json \
  --reporter-htmlextra-export "report/${NAME}-report.html" \
  --reporter-json-export "report/${NAME}-report.json"
RC=$?
set -e

python3 sanitize_report.py \
  "report/${NAME}-report.json" \
  "report/${NAME}-report.sanitized.json" || true

ln -sfn "${NAME}-report.html" report/latest-report.html
ln -sfn "${NAME}-report.json" report/latest-report.json
ln -sfn "${NAME}-report.sanitized.json" report/latest-report.sanitized.json

if command -v wkhtmltoimage >/dev/null 2>&1; then
  wkhtmltoimage --width 1400 "report/${NAME}-report.html" \
    "screenshots/${STAMP}_newman_summary.png" || true
fi

echo "exit_code: $RC"
echo "html: $ROOT/report/${NAME}-report.html"
exit "$RC"
