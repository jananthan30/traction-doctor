#!/usr/bin/env bash
# Seed a tiny, deliberately under-distributed CLI repo: no LICENSE, no install
# command in the README, no CHANGELOG, no telemetry.
set -euo pipefail
mkdir -p src
cat > README.md <<'MD'
# quickcsv

Turn messy CSV exports into clean JSON. Handles quoted fields, BOMs, and
Excel's semicolon exports.

## Usage

    quickcsv input.csv > output.json
MD
cat > package.json <<'JSON'
{
  "name": "quickcsv",
  "version": "0.3.1",
  "description": "Turn messy CSV exports into clean JSON",
  "bin": { "quickcsv": "src/cli.js" },
  "dependencies": { "csv-parse": "^5.5.0" }
}
JSON
cat > src/cli.js <<'JS'
#!/usr/bin/env node
const { parse } = require("csv-parse/sync");
const fs = require("fs");
const input = fs.readFileSync(process.argv[2], "utf8").replace(/^﻿/, "");
const delimiter = input.split("\n")[0].includes(";") ? ";" : ",";
process.stdout.write(JSON.stringify(parse(input, { columns: true, delimiter }), null, 2));
JS
git init -q
git -c user.name=dev -c user.email=dev@example.com add -A
git -c user.name=dev -c user.email=dev@example.com commit -qm "quickcsv: first working version"
