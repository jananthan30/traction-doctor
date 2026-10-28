#!/usr/bin/env python3
"""Lint a close-gaps CLOSE-GAPS.md against its contract.

Checks that the file is complete and internally consistent:
  - the title, the fingerprint, and the machine-readable `cg` line, with
    valid target ids
  - every section present and in order, one Weakness section per target
  - no unfilled template slots
  - every idea card has every field; scores add up and no part is 0; Kind
    agrees with Proof; a proof is linked, or `unverified` and capped at 1
  - success and stop dates fall after the run and within 28 days of it, and
    success states its baseline; a first test has one to five steps and
    states its cost
  - the Top ideas table and `cg.top` agree with the cards and follow the
    top-five rules; Do this first is the top row
  - a local-only run is marked NOT RESEARCHED and stays at Proof 1
  - a pragmatist record in Dissent; linked sources on a web run

Usage:
  python3 check_ideas.py CLOSE-GAPS.md [more files...]

Exit status: 0 when every file passes, 1 otherwise. Standard library only;
the markdown helpers come from the traction-doctor skill installed next to
this one.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path

DG_SCRIPTS = Path(__file__).resolve().parents[2] / "traction-doctor" / "scripts"
if not (DG_SCRIPTS / "check_report.py").is_file():
    sys.exit("check_ideas.py needs the traction-doctor skill installed next to close-gaps "
             f"(looked for {DG_SCRIPTS / 'check_report.py'})")
sys.path.insert(0, str(DG_SCRIPTS))
from check_report import (  # noqa: E402
    LINK, bullet_groups, section, tables, tool_for, unfilled_slots,
)

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
    fingerprint = f"Generated by {tool_for(cg['v'])} v{cg['v']} (close-gaps)"
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


# --- Idea cards ---------------------------------------------------------------

CARD = re.compile(r"^### (I\d+)\.\s*(.*)$", re.M)
FIELDS = ("Closes", "Kind", "Fits", "Proof", "1-week test", "Success", "Stop if", "If it works",
          "Full build", "Score")
_FIELD_NAMES = "|".join(map(re.escape, FIELDS))
FIELD_RE = re.compile(rf"\*\*({_FIELD_NAMES}):\*\*\s*(.*?)(?=\s+·\s+\*\*(?:{_FIELD_NAMES}):\*\*|$)")
PARTS = ("Impact", "Proof", "Fit", "Cheap")
SCORE_RE = re.compile(r"\s*[·,;|]?\s*".join(rf"{p}:?\s*(\d+)" for p in PARTS)
                      + r"\s*=\s*(\d+)\s*/\s*20")
KINDS = ("proven", "fresh", "reasoned")
BUILDS = ("S", "M", "L")
STEP = re.compile(r"\d+\.\s")
DAY = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")
PROOF_DATE = re.compile(r"\b(20\d{2})(?:-(0[1-9]|1[0-2]))?(?:-\d{2})?\b")
COST = re.compile(r"cost:\s*(free|\$\s?\d[\d,]*)", re.I)
REFERENCE = re.compile(r"references/[\w./-]+\.md")
MAX_DAYS = 28
MAX_STEPS = 5
FRESH_MONTHS = 24


def parse_cards(text: str) -> list[dict]:
    """Every idea card inside a Weakness section.

    Each card: id, title, fields (name → text), steps (the 1-week test's
    numbered steps), and the parsed target, kind, build, parts and score
    (None when absent or unreadable).
    """
    cards = []
    for weak in WEAKNESS.finditer(text):
        block = after(text, weak.end())
        heads = list(CARD.finditer(block))
        for i, head in enumerate(heads):
            body = block[head.end():heads[i + 1].start() if i + 1 < len(heads) else len(block)]
            fields: dict[str, str] = {}
            steps: list[str] = []
            for parent, children in bullet_groups(body):
                for f in FIELD_RE.finditer(parent):
                    fields[f.group(1)] = f.group(2).strip()
                    if f.group(1) == "1-week test":
                        steps = [c for c in children if STEP.match(c)]
            closes = re.search(r"`([^`]+)`", fields.get("Closes", ""))
            score = SCORE_RE.search(fields.get("Score", "").replace("*", ""))
            cards.append({
                "id": head.group(1),
                "title": head.group(2).strip(),
                "fields": fields,
                "steps": steps,
                "target": closes.group(1) if closes else None,
                "kind": fields.get("Kind", "").strip("`* ").lower(),
                "build": fields.get("Full build", "").strip("`* ").upper(),
                "parts": dict(zip(PARTS, map(int, score.groups()[:4]))) if score else None,
                "score": int(score.group(5)) if score else None,
            })
    return cards


def months_between(earlier: date, later: date) -> int:
    return (later.year - earlier.year) * 12 + later.month - earlier.month


def check_cards(cards: list[dict], cg: dict | None, text: str, errors: list[str],
                warnings: list[str]) -> None:
    run = iso_date(cg["date"]) if cg is not None else None
    web = cg.get("web") if cg is not None else None
    seen: set[str] = set()
    for card in cards:
        cid, fields, parts = card["id"], card["fields"], card["parts"]
        if cid in seen:
            errors.append(f"duplicate card id {cid}")
        seen.add(cid)
        for name in FIELDS:
            if name not in fields:
                errors.append(f"{cid} is missing '{name}'")
            elif not fields[name] and name != "1-week test":
                errors.append(f"{cid}'s {name} is empty")

        if "Closes" in fields and cg is not None:
            if card["target"] is None:
                errors.append(f"{cid}'s Closes must name its target id in backticks, e.g. `crux`")
            elif card["target"] not in cg["targets"]:
                errors.append(f"{cid} closes `{card['target']}`, which isn't in cg.targets")
        if "Kind" in fields and card["kind"] not in KINDS:
            errors.append(f"{cid}: Kind must be proven, fresh or reasoned (got {fields['Kind']!r})")
        if "Full build" in fields and card["build"] not in BUILDS:
            errors.append(f"{cid}: Full build must be S, M or L (got {fields['Full build']!r})")

        if "Score" in fields and parts is None:
            errors.append(f"{cid}'s Score must read 'Impact a · Proof b · Fit c · Cheap d = n/20'")
        if parts is not None:
            if any(not 0 <= v <= 5 for v in parts.values()):
                errors.append(f"{cid}: score parts must be 0–5")
            elif sum(parts.values()) != card["score"]:
                errors.append(f"{cid}'s score parts add up to {sum(parts.values())}, "
                              f"not {card['score']}")
            for name, value in parts.items():
                if value == 0:
                    errors.append(f"{cid} has a 0 in {name} — cut it to 'Shiny but not now'")

        proof = fields.get("Proof", "")
        unverified = "unverified" in proof.lower()
        if parts is not None:
            if card["kind"] == "proven" and parts["Proof"] < 3:
                errors.append(f"{cid} is proven but Proof is {parts['Proof']} — proven needs a "
                              "look-alike's result (Proof 3 or more)")
            if card["kind"] == "reasoned" and parts["Proof"] != 1:
                errors.append(f"{cid} is reasoned, so Proof must be 1 (got {parts['Proof']})")
            if unverified and parts["Proof"] > 1:
                errors.append(f"{cid}'s Proof is `unverified`, so it scores at most 1 "
                              f"(got {parts['Proof']})")
        if "Proof" in fields:
            cited = web is False and REFERENCE.search(proof)
            if not (LINK.search(proof) or unverified or cited):
                hint = " (a local-only run may cite references/<file>.md)" if web is False else ""
                errors.append(f"{cid}'s Proof needs a link or 'unverified'{hint}")
        if card["kind"] == "fresh" and run is not None:
            dated = [(int(y), int(mo) if mo else (run.month if int(y) == run.year else 12))
                     for y, mo in PROOF_DATE.findall(proof)]
            if not dated:
                errors.append(f"{cid} is fresh but its Proof has no date")
            else:
                year, month = max(dated)
                if not 0 <= months_between(date(year, month, 1), run) <= FRESH_MONTHS:
                    errors.append(f"{cid} is fresh but its Proof's latest date {year}-{month:02d} "
                                  f"isn't within {FRESH_MONTHS} months before the run")

        for name in ("Success", "Stop if"):
            if name not in fields or run is None:
                continue
            days = DAY.findall(fields[name])
            if not days:
                errors.append(f"{cid}'s {name} needs a YYYY-MM-DD date")
            for day in days:
                when = iso_date(day)
                if when is None:
                    errors.append(f"{cid}'s {name} date {day} isn't a real date")
                elif when <= run:
                    errors.append(f"{cid}'s {name} date {day} is not after the run date ({run})")
                elif (when - run).days > MAX_DAYS:
                    errors.append(f"{cid}'s {name} date {day} is more than {MAX_DAYS} days after "
                                  f"the run ({run})")

        if "Success" in fields and not re.search(r"\bbaseline\b", fields["Success"], re.I):
            errors.append(f"{cid}'s Success must state its baseline — the metric's value today, e.g. "
                          "'(baseline 0)', or a change from it, e.g. '≥2 more than the day-1 baseline'")

        if "1-week test" in fields:
            steps = len(card["steps"])
            if not 1 <= steps <= MAX_STEPS:
                errors.append(f"{cid}'s 1-week test has {steps} steps; write 1–{MAX_STEPS} "
                              "numbered steps")
            cost = COST.search(fields["1-week test"])
            if not cost:
                errors.append(f"{cid}'s 1-week test must state its cost ('cost: free' or "
                              "'cost: $<n>')")
            elif parts is not None and parts["Cheap"] >= 3 and not re.fullmatch(
                    r"free|\$\s?0", cost.group(1), re.I):
                errors.append(f"{cid} scores Cheap {parts['Cheap']} but its test costs "
                              f"{cost.group(1)} — Cheap 3 or more must be free")

        if web is False and (card["kind"] != "reasoned" or (parts is not None and parts["Proof"] != 1)):
            errors.append(f"local-only run: {cid} must be reasoned with Proof 1")

    for weak in WEAKNESS.finditer(text):
        if not CARD.search(after(text, weak.end())):
            warnings.append(f"Weakness {weak.group(1)} has no idea cards — say 'no practical fix "
                            "found' and why")


# --- Top ideas ----------------------------------------------------------------

ROW_ID = re.compile(r"I\d+")
TOP_MAX = 5


def top_rows(text: str) -> list[dict] | None:
    """The Top ideas table as dicts (id, score, kind, build), or None without a table."""
    found = tables(section(text, r"## Top ideas"))
    if not found:
        return None
    header = [c.replace("*", "").strip().lower() for c in found[0][0]]
    rows = []
    for raw in found[0][1:]:
        cells = {h: (raw[i].replace("*", "").strip() if i < len(raw) else "")
                 for i, h in enumerate(header)}
        ident = ROW_ID.search(cells.get("#", ""))
        score = re.search(r"(\d+)\s*/\s*20", cells.get("score", ""))
        rows.append({
            "id": ident.group(0) if ident else cells.get("#", ""),
            "score": int(score.group(1)) if score else None,
            "kind": cells.get("kind", "").strip("` ").lower(),
            "build": cells.get("build", "").strip("` ").upper(),
        })
    return rows


def check_top(text: str, cards: list[dict], cg: dict | None, errors: list[str]) -> None:
    by_id = {c["id"]: c for c in cards}
    rows = top_rows(text)
    if rows is None:
        if cards:
            errors.append("Top ideas needs a table: # | Idea | Closes | Kind | First test | "
                          "Build | Score")
        elif not section(text, r"## Top ideas").strip():
            errors.append("Top ideas is empty — with no research targets, say so in one line")
        rows = []

    ids = [r["id"] for r in rows]
    if len(rows) > TOP_MAX:
        errors.append(f"Top ideas lists {len(rows)} rows; at most {TOP_MAX}")
    if len(set(ids)) != len(ids):
        errors.append("Top ideas lists an idea twice")
    for row in rows:
        card = by_id.get(row["id"])
        if card is None:
            errors.append(f"Top ideas row {row['id']} has no card")
            continue
        for key, label in (("score", "Score"), ("kind", "Kind"), ("build", "Build")):
            if row[key] != card[key]:
                errors.append(f"Top ideas row {row['id']} says {label} {row[key]} but its card "
                              f"says {card[key]}")
    scores = [r["score"] for r in rows if r["score"] is not None]
    if scores != sorted(scores, reverse=True):
        errors.append("Top ideas must be sorted by score, highest first")
    if sum(1 for r in rows if r["build"] == "L") > 1:
        errors.append("Top ideas may hold at most one big bet (Full build L)")

    listed = [by_id[i] for i in ids if i in by_id]
    for target in dict.fromkeys(c["target"] for c in cards if c["target"]):
        if not any(c["target"] == target for c in listed):
            errors.append(f"`{target}` has idea cards but none in Top ideas — each target's best "
                          "idea goes in")
    if cg is not None and cg.get("web") is True and any(c["kind"] == "fresh" for c in cards) \
            and not any(c["kind"] == "fresh" for c in listed):
        errors.append("a fresh idea survived but none is in Top ideas — keep one fresh slot")
    if len(rows) < TOP_MAX:
        has_big_bet = any(r["build"] == "L" for r in rows)
        for card in cards:
            if card["id"] not in ids and not (card["build"] == "L" and has_big_bet):
                errors.append(f"{card['id']} survived but isn't in Top ideas ({len(rows)} rows) — "
                              "fill up to five before leaving an idea out")

    if cg is not None:
        want = [(r["id"], r["score"], r["kind"], r["build"]) for r in rows]
        got = [(e.get("id"), e.get("score"), e.get("kind"), e.get("build")) for e in cg["top"]]
        if want != got:
            errors.append("cg.top disagrees with the Top ideas table (ids, order, scores, kinds, "
                          "builds)")

    first = section(text, r"## Do this first")
    if rows:
        named = re.search(r"\*\*(I\d+)\.", first)
        if not named or named.group(1) != rows[0]["id"]:
            errors.append(f"Do this first must be the top row, {rows[0]['id']} "
                          f"(it names {named.group(1) if named else 'no idea'})")
        if not re.search(r"^\d+\.\s", first, re.M):
            errors.append("Do this first needs its test as numbered steps")
        if "Success:" not in first or "Stop if:" not in first:
            errors.append("Do this first needs its Success and Stop if lines")
    elif not first.strip():
        errors.append("Do this first is empty — with no research targets, name the first "
                      "'Just do it' row")


# --- The check ----------------------------------------------------------------

def check(path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    text = path.read_text(encoding="utf-8")
    cg = parse_cg(text, errors)
    check_structure(text, cg, errors, warnings)
    cards = parse_cards(text)
    check_cards(cards, cg, text, errors, warnings)
    check_top(text, cards, cg, errors)
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
