---
type: regex
target: { source: file, path: FIRST-CUSTOMERS.md }
pattern: 'reddit\.com/r/[^/\s)]+/comments/|news\.ycombinator\.com/item\?id=|github\.com/[^/\s)]+/[^/\s)]+/(?:issues|discussions|pull)/\d+|stackoverflow\.com/(?:questions|q|a)/\d+'
match: not_contains
---
