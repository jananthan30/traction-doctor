---
type: regex
target: { source: file, path: STRATEGY.md }
pattern: '(?<!^(?:[^`\n]*`[^`\n]*`)*[^`\n]*`[^`\n]*)<(?!!--|https?:|[^\s@<>]+@|/?(?:img|br|a|details|summary|sub|sup|p|div|span|kbd|b|i|em|strong|code|pre|hr|picture|source)\b)[a-z][^<>\n]{0,80}>'
flags: im
match: not_contains
---
