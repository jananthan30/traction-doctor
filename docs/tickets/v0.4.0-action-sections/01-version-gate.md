# 01: Version-gated report contract and v0.4.0 pins

**What to build:** the report checker knows which contract a report follows
from its `dg.v`: reports from v0.4.0 on get the new checks (tickets 02–04
add them), older ones keep exactly today's checks. The plugin's version is
0.4.0 everywhere it is pinned, and the sample report fixture is a v0.4.0
report that still passes.

**Blocked by:** None (can start immediately).

**Status:** done

- [x] A v0.2.0 or v0.3.0 report passes exactly as before (examples, the
      self-report, the archive)
- [x] The fixture is stamped v0.4.0 (report, card re-rendered from its JSON)
      and passes
- [x] A test proves a pre-0.4 report skips the v0.4 checks
- [x] Every version pin agrees on 0.4.0 (`test_versions_agree`)
- [x] Line budget is 500 for v0.4 reports
