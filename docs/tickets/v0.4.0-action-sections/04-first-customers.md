# 04: First customers — customer-scout and FIRST-CUSTOMERS.md

**What to build:** after the red team settles the wedge, a `customer-scout`
sensor finds real, recent public posts where the wedge ICP asked for what the
product does. The strategist writes a private `FIRST-CUSTOMERS.md` (who,
offer, venues with their rules, openings, disclosed drafts, 14-day plan,
tracker, rules) and a *First customers* sub-section in §5 with no
individual posts. A people-file checker enforces the contract, including
privacy. Offline runs produce search links and drafts, marked NOT
RESEARCHED, with no people.

**Blocked by:** 01 (path and pivots are independent; build after 02–03 to
avoid edit conflicts in the same files).

**Status:** ready-for-agent

- [ ] Sensor method + agent file (web and read-only tools only)
- [ ] Skill: Phase 6, briefing with the final wedge and watering holes,
      brief checks (spot-check openings), file collision and re-run rules,
      allowed writes, chat reply order, gitignore advice
- [ ] File template + report sub-section template
- [ ] People-file checker: structure, privacy (emails, phones — narrow),
      openings, drafts' disclosure, tracker, offline rules; standalone CLI;
      called from the report checker when the linked file exists
- [ ] Report checker: sub-section present, offer, venue table, link to the
      file, no individual post links
- [ ] Fixture people file + tests, including false-positive tests for the
      phone pattern
