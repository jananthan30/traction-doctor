---
type: regex
target: { source: file, path: FIRST-CUSTOMERS.md }
pattern: '## Openings\s+[\s\S]*?(?:\| 1 \| \[[^\]]+\]\(https?://[^)]+\) \| \d{4}-\d{2}-\d{2} \| \d{4}-\d{2}-\d{2} \| "[^"]+"|[Oo]nly \d+ openings? found|[Nn]o openings found)'
---
