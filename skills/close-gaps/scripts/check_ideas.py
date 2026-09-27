#!/usr/bin/env python3
"""Lint a close-gaps CLOSE-GAPS.md against its contract.

Checks that the file is complete and internally consistent:
  - the title, the fingerprint, and the machine-readable `cg` line, with
    valid target ids
  - every section present and in order, one Weakness section per target
  - no unfilled template slots
  - every idea card has every field; scores add up and no part is 0; Kind
    agrees with Proof; a proof is linked, or `unverified` and capped at 1
  - success and stop dates fall after the run and within 28 days of it; a
    first test has one to five steps and states its cost
  - the Top ideas table and `cg.top` agree with the cards and follow the
    top-five rules; Do this first is the top row
  - a local-only run is marked NOT RESEARCHED and stays at Proof 1
  - a pragmatist record in Dissent; linked sources on a web run

Usage:
  python3 check_ideas.py CLOSE-GAPS.md [more files...]

Exit status: 0 when every file passes, 1 otherwise. Standard library only;
the markdown helpers come from the distribution-god skill installed next to
this one.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path

DG_SCRIPTS = Path(__file__).resolve().parents[2] / "distribution-god" / "scripts"
if not (DG_SCRIPTS / "check_report.py").is_file():
    sys.exit("check_ideas.py needs the distribution-god skill installed next to close-gaps "
             f"(looked for {DG_SCRIPTS / 'check_report.py'})")
sys.path.insert(0, str(DG_SCRIPTS))
from check_report import LINK, bullet_groups, section, tables, unfilled_slots  # noqa: E402

SECTIONS = [r"## Do this first", r"## Top ideas", r"## Just do it", r"## Can['’]t move now",
            r"## Shiny but not now", r"## Dissent", r"## Sources"]
WEAKNESS = re.compile(r"^## Weakness (\d+):(.*)$", re.M)
CG_KEYS = ("v", "date", "mode", "web", "report", "targets", "top")
REPORT_KEYS = ("date", "bigness", "moat")
TOP_KEYS = ("id", "score", "kind", "build")
MODES = ("parallel", "generic-subagents", "sequential")
BIGNESS_KEYS = ("market", "why_now", "wedge", "expansion", "delivery")
MOAT_KEYS = ("network", "switching", "scale_data", "brand", "cornered_counter")
TARGET_PART = re.compile(r"bigness\.(?:%s)|moat\.(?:%s)|crux|gap\.[1-9]\d*"
                         % ("|".join(BIGNESS_KEYS), "|".join(MOAT_KEYS)))
MAX_TARGETS = 3
LINE_BUDGET = 300
NOT_RESEARCHED = "NOT RESEARCHED"


def valid_target(target: object) -> bool:
    """A target id, or several joined with '+' (see idea-rubric.md → Target ids)."""
    return isinstance(target, str) and all(TARGET_PART.fullmatch(p) for p in target.split("+"))


def iso_date(value: object) -> date | None:
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def after(text: str, start: int) -> str:
    """The text from `start` up to the next `## ` heading."""
    nxt = re.search(r"^## ", text[start:], re.M)
    return text[start:start + nxt.start()] if nxt else text[start:]


def parse_cg(text: str, errors: list[str]) -> dict | None:
    """The `cg` line as a dict with `targets` and `top` normalized to lists, or None."""
    m = re.search(r"<!-- cg: (\{.*?\}) -->", text)
    if not m:
        errors.append("missing the '<!-- cg: {...} -->' line under the title")
        return None
    try:
        cg = json.loads(m.group(1))
    except json.JSONDecodeError as exc:
        errors.append(f"cg line is not valid JSON: {exc}")
        return None
    if not isinstance(cg, dict):
        errors.append("cg line must be a JSON object")
        return None
    missing = [k for k in CG_KEYS if k not in cg]
    for key in missing:
        errors.append(f"cg line missing key {key!r}")
    if missing:
        return None
    if not isinstance(cg["v"], str) or not re.fullmatch(r"\d+\.\d+\.\d+", cg["v"]):
        errors.append('cg.v must be the plugin version, e.g. "0.3.0"')
    if iso_date(cg["date"]) is None:
        errors.append("cg.date must be the run's UTC date as YYYY-MM-DD")
    if cg["mode"] not in MODES:
        errors.append("cg.mode must be parallel, generic-subagents or sequential")
    if not isinstance(cg["web"], bool):
        errors.append("cg.web must be true or false")
    report = cg["report"]
    if not isinstance(report, dict) or any(k not in report for k in REPORT_KEYS):
        errors.append(f"cg.report must be an object with keys {list(REPORT_KEYS)}")
    else:
        if iso_date(report["date"]) is None:
            errors.append("cg.report.date must be the report's run date as YYYY-MM-DD")
        for key in ("bigness", "moat"):
            value = report[key]
            if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value <= 25:
                errors.append(f"cg.report.{key} must be an integer 0–25")
    targets = cg["targets"] if isinstance(cg["targets"], list) else []
    if not isinstance(cg["targets"], list):
        errors.append("cg.targets must be a list of target ids")
    for target in targets:
        if not valid_target(target):
            errors.append(f"cg.targets: invalid target id {target!r} (see idea-rubric.md → Target ids)")
    if len(targets) > MAX_TARGETS:
        errors.append(f"cg.targets lists {len(targets)} targets; research at most {MAX_TARGETS}")
    if len(set(map(str, targets))) != len(targets):
        errors.append("cg.targets lists a target twice")
    cg["targets"] = [t for t in targets if isinstance(t, str)]
    top = cg["top"]
    if not isinstance(top, list) or not all(isinstance(e, dict) and all(k in e for k in TOP_KEYS)
                                            for e in top):
        errors.append(f"cg.top must be a list of objects with keys {list(TOP_KEYS)}")
        cg["top"] = []
    fingerprint = f"Generated by distribution-god v{cg['v']} (close-gaps)"
    if fingerprint not in text:
        errors.append(f"fingerprint '{fingerprint}' missing")
    return cg


def check_structure(text: str, cg: dict | None, errors: list[str], warnings: list[str]) -> None:
    if not re.match(r"# Closing the gaps — \S", text):
        errors.append("first line must be '# Closing the gaps — <product name>'")

    # Fixed sections, in order.
    found: dict[str, int] = {}
    pos = -1
    for pattern in SECTIONS:
        label = pattern.replace("['’]", "'")
        m = re.search(rf"^{pattern}\s*$", text, re.M)
        if not m:
            errors.append(f"missing section: {label}")
            continue
        found[label] = m.start()
        if m.start() < pos:
            errors.append(f"section out of order: {label}")
        else:
            pos = m.start()

    # One Weakness section per target, between Just do it and Can't move now.
    weak = list(WEAKNESS.finditer(text))
    lo, hi = found.get("## Just do it"), found.get("## Can't move now")
    for m in weak:
        if lo is not None and hi is not None and not lo < m.start() < hi:
            errors.append(f"Weakness {m.group(1)} must sit between '## Just do it' and "
                          "'## Can't move now'")
    if [int(m.group(1)) for m in weak] != list(range(1, len(weak) + 1)):
        errors.append("Weakness sections must be numbered 1, 2, 3 … in order")
    if cg is not None:
        targets = cg["targets"]
        if len(weak) != len(targets):
            errors.append(f"cg.targets lists {len(targets)} target(s) but there are "
                          f"{len(weak)} Weakness sections")
        for i, m in enumerate(weak):
            ident = re.search(r"\(`([^`]+)`\)", m.group(2))
            if not ident:
                errors.append(f"Weakness {m.group(1)}'s heading must name its target id, e.g. (`crux`)")
            elif i < len(targets) and ident.group(1) != targets[i]:
                errors.append(f"Weakness {m.group(1)} is `{ident.group(1)}` but cg.targets[{i}] "
                              f"is `{targets[i]}`")

    errors.extend(unfilled_slots(text))

    if "Pragmatist adjustments:" not in section(text, r"## Dissent"):
        errors.append("Dissent must start with a 'Pragmatist adjustments:' line")

    web = cg.get("web") if cg is not None else None
    if web is True:
        if not LINK.search(section(text, r"## Sources")):
            errors.append("a web run's Sources section needs at least one link")
        if NOT_RESEARCHED in text:
            errors.append(f"the file says '{NOT_RESEARCHED}' but cg.web is true — only a "
                          "local-only run may")
    elif web is False:
        for m in weak:
            if NOT_RESEARCHED not in after(text, m.end()):
                errors.append(f"cg.web is false but Weakness {m.group(1)} does not say "
                              f"'{NOT_RESEARCHED}'")

    lines = text.count("\n")
    if lines > LINE_BUDGET:
        warnings.append(f"file is {lines} lines; the template targets under {LINE_BUDGET}")


# --- The check ----------------------------------------------------------------

def check(path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    text = path.read_text(encoding="utf-8")
    cg = parse_cg(text, errors)
    check_structure(text, cg, errors, warnings)
    return errors, warnings


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__.strip().split("\n\n")[2], file=sys.stderr)
        return 2
    failed = False
    for arg in argv:
        path = Path(arg)
        if not path.exists():
            print(f"{arg}: not found", file=sys.stderr)
            failed = True
            continue
        errors, warnings = check(path)
        for w in warnings:
            print(f"{arg}: warning: {w}")
        if errors:
            failed = True
            print(f"{arg}: {len(errors)} problem(s)")
            for e in errors:
                print(f"  - {e}")
        else:
            print(f"{arg}: ok")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
