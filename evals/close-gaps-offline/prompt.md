---
description: Without web tools, close-gaps must still write a CLOSE-GAPS.md that passes check_ideas.py, drawn from the plugin's playbooks and marked NOT RESEARCHED.
tags: [close-gaps, offline]
runs: 1
max_turns: 120
timeout_seconds: 2400
allowed_tools: [Read, Glob, Grep, Bash, Write, Edit, Skill]
---

My STRATEGY.md says this project is weak in a few places. Give me practical ideas to close those gaps. There's no web access in this environment, so work from what you have, and don't ask me any questions — just produce the result.
