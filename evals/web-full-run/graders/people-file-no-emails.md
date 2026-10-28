---
type: regex
target: { source: file, path: FIRST-CUSTOMERS.md }
pattern: '[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}\b|mailto:'
match: not_contains
---
