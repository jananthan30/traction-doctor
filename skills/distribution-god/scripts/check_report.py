#!/usr/bin/env python3
"""Lint a distribution-god STRATEGY.md against the report contract.

Checks that the report is complete and internally consistent:
  - every template section is present, in order, with no unfilled slots
  - the machine-readable `dg` line agrees with the Verdict, the Bigness
    breakdown and the Moat today tables, and band labels match the rubric
  - market-size figures are labeled ESTIMATE; other money figures in the
    Market section carry ESTIMATE, `unverified`, or a source link
  - every written calculation `a × b ÷ c = d` in the Market section adds up
  - every rival row has a source; exactly one PRIMARY channel; five actions;
    a red-team record in Dissent
  - the linked strategy card exists, parses, and shows the same scores
  - from v0.4.0 (read off the dg line; older reports keep their contract):
    the Verdict's Path to the next band states the gap to each next band
    correctly, and its 2–5 moves start at today's scores, raise real rubric
    rows, are labeled outcome or rubric-only (at least one outcome), and
    project no total

Usage:
  python3 check_report.py STRATEGY.md [more reports...]

Exit status: 0 when every report passes, 1 otherwise. Standard library only.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from strategy_card import (  # noqa: E402
    BIGNESS_BANDS, BIGNESS_DIMENSIONS, MOAT_BANDS, CardError, band_for, validate_svg_text,
)

RUBRIC_VERSION = 2
SECTIONS = [
    r"## Verdict",
    r"## 1\. What the repo says",
    r"## 2\. Market",
    r"## 3\. Competitive field",
    r"## 4\. Strategy",
    r"## 5\. Distribution plan",
    r"## 6\. Gaps",
    r"## 7\. Moat roadmap",
    r"## 8\. What would have to be true",
    r"## 9\. Kill criteria",
    r"## 10\. Next 5 actions",
    r"## Dissent",
    r"## Sources",
]
SUB_KEYS = dict(zip(BIGNESS_DIMENSIONS, ["market", "why_now", "wedge", "expansion", "delivery"]))
MOAT_ROWS = {
    "Network economies": "network",
    "Switching costs": "switching",
    "Scale economies / data": "scale_data",
    "Brand / category ownership": "brand",
    "Cornered resource / counter-positioning": "cornered_counter",
}
HTML_TAGS = {"img", "br", "a", "details", "summary", "sub", "sup", "p", "div", "span",
             "picture", "source", "kbd", "b", "i", "em", "strong", "code", "pre", "hr"}
SLOT = re.compile(r"<(?!!--)(/?)([A-Za-z][^<>\n]{0,80})>")
MONEY = re.compile(r"(?:[$€£]\s?\d|\b(?:USD|EUR|GBP|US\$)\s?\d)")
LINK = re.compile(r"\]\(https?://|<https?://|https?://\S")
# Reports from V4 on carry the action parts (path to the next band, pivot
# options, first customers); older reports keep the contract they were
# written under, so the examples and the archive stay valid.
V4 = (0, 4, 0)
LINE_BUDGET = 450
LINE_BUDGET_V4 = 500

# --- Market arithmetic -------------------------------------------------------
# A tiny tokenizer + evaluator for calculations written in prose, e.g.
# "400k teams × $300–1,200/yr = $120M–$480M" or "~$14M–$407M + $10M–$72M = …".
_MAG = {"": 1.0, "%": 0.01, "k": 1e3, "K": 1e3, "thousand": 1e3, "M": 1e6, "mn": 1e6,
        "million": 1e6, "B": 1e9, "bn": 1e9, "billion": 1e9}
_NUM_RE = re.compile(
    r"(?<![\w.$€£])[~≈]?\s?(?P<cur>[$€£])?(?P<val>\d[\d,]*(?:\.\d+)?)"
    r"(?:\s?(?P<mag>%|thousand|million|billion|bn|mn|k|K|M|B)(?![A-Za-z]))?"
    r"(?:/[A-Za-z][A-Za-z-]*)*")
_RANGE_SEP = re.compile(r"\s?(?:[–—-]|to)\s?")
_TOKEN_RE = re.compile(
    r"(?P<op>[×÷+]|(?<=\s)x(?=\s+[~≈$€£\d]))"
    r"|(?P<eq>[=≈])"
    r"|(?P<paren>\([^()=\n]{0,150}\))"
    r"|(?P<word>[A-Za-z][A-Za-z0-9'’-]*)"
    r"|(?P<space>\s+)"
    r"|(?P<other>.)")
BIG_BANDS_USD = [(10e9, 5), (2e9, 4), (500e6, 3), (200e6, 2), (50e6, 1), (0, 0)]


def _num(m: re.Match) -> tuple[float, bool, str]:
    return float(m.group("val").replace(",", "")), bool(m.group("cur")), m.group("mag") or ""


def _tokens(text: str) -> list[tuple[str, object, int]]:
    """[(kind, value, offset)]; kind is num / op / eq / fill / break."""
    out, i = [], 0
    while i < len(text):
        m = _NUM_RE.match(text, i)
        if m:
            lo_v, lo_cur, lo_mag = _num(m)
            end, hi = m.end(), None
            sep = _RANGE_SEP.match(text, end)
            if sep:
                m2 = _NUM_RE.match(text, sep.end())
                if m2:
                    hi, end = _num(m2), m2.end()
            if hi is None:
                v = lo_v * _MAG[lo_mag]
                out.append(("num", (v, v), i))
            else:
                hi_v, hi_cur, hi_mag = hi
                # "150–300k" shares the suffix; "$500–$2k" doesn't.
                if not lo_mag and not hi_cur and lo_v * _MAG[hi_mag] <= hi_v * _MAG[hi_mag]:
                    lo_mag = hi_mag
                out.append(("num", (lo_v * _MAG[lo_mag], hi_v * _MAG[hi_mag]), i))
            i = end
            continue
        t = _TOKEN_RE.match(text, i)
        kind = t.lastgroup
        if kind == "op":
            out.append(("op", "×" if t.group() == "x" else t.group(), i))
        elif kind == "eq":
            out.append(("eq", None, i))
        elif kind in ("paren", "word"):
            out.append(("fill", None, i))
        elif kind == "other":
            out.append(("break", None, i))
        i = t.end()
    return out


def calculations(text: str) -> list[dict]:
    """Every parseable `a op b … = c` in the text, evaluated."""
    text = text.replace("*", "").replace("`", "")  # markdown emphasis and code marks
    toks = _tokens(text)
    found, i = [], 0
    while i < len(toks):
        if toks[i][0] != "num" or (i and _prev_sig(toks, i) == "op"):
            i += 1
            continue
        terms, cur, j = [], [("×", toks[i][1])], i + 1
        result = None
        while j < len(toks):
            j = _skip_fill(toks, j)
            if j < len(toks) and toks[j][0] == "op":
                k = j + 1
                if k < len(toks) and toks[k][0] == "num":
                    if toks[j][1] == "+":
                        terms.append(cur)
                        cur = [("×", toks[k][1])]
                    else:
                        cur.append((toks[j][1], toks[k][1]))
                    j = k + 1
                    continue
                break
            if j < len(toks) and toks[j][0] == "eq" and (terms or len(cur) > 1):
                k = j + 1
                if k < len(toks) and toks[k][0] == "num":
                    result = toks[k][1]
                    j = k + 1
            break
        if result is None:
            i += 1
            continue
        terms.append(cur)
        lo = hi = 0.0
        valid = True
        for term in terms:
            t_lo = t_hi = 1.0
            for op, (a, b) in term:
                if op == "÷":
                    if not a or not b:
                        valid = False
                        break
                    t_lo, t_hi = t_lo / b, t_hi / a
                else:
                    t_lo, t_hi = t_lo * a, t_hi * b
            lo, hi = lo + t_lo, hi + t_hi
        end = toks[j][2] if j < len(toks) else len(text)
        if valid:
            found.append({"text": " ".join(text[toks[i][2]:end].split()).strip(" .;,"),
                          "want": (lo, hi), "got": result})
        i = j
    return found


def _prev_sig(toks, i):
    j = i - 1
    while j >= 0 and toks[j][0] == "fill":
        j -= 1
    return toks[j][0] if j >= 0 else None


def _skip_fill(toks, j, limit=4):
    n = 0
    while j < len(toks) and toks[j][0] == "fill" and n < limit:
        j, n = j + 1, n + 1
    return j


def _close(a: float, b: float, tolerance: float = 0.06) -> bool:
    return abs(a - b) <= tolerance * max(abs(a), abs(b), 1e-9)


def arithmetic_errors(block: str, tolerance: float = 0.06) -> list[str]:
    errors = []
    for c in calculations(block):
        (w_lo, w_hi), (g_lo, g_hi) = c["want"], c["got"]
        if not (_close(w_lo, g_lo, tolerance) and _close(w_hi, g_hi, tolerance)):
            errors.append(f"market arithmetic doesn't add up: '{c['text']}' "
                          f"works out to {_fmt(w_lo)}–{_fmt(w_hi)}")
    return errors


def headroom_band(midpoint: float) -> int:
    return next(score for floor, score in BIG_BANDS_USD if midpoint >= floor)


def _fmt(v: float) -> str:
    for div, sfx in ((1e9, "B"), (1e6, "M"), (1e3, "k")):
        if abs(v) >= div:
            return f"{v / div:.3g}{sfx}"
    return f"{v:.3g}"


# --- Markdown helpers --------------------------------------------------------

def section(text: str, heading: str) -> str:
    m = re.search(rf"^{heading}.*$", text, re.M)
    if not m:
        return ""
    rest = text[m.end():]
    nxt = re.search(r"^## ", rest, re.M)
    return rest[: nxt.start()] if nxt else rest


def table_rows(block: str) -> list[list[str]]:
    rows = []
    for line in block.splitlines():
        line = line.strip()
        if line.startswith("|") and not re.match(r"^\|[\s:|-]+\|$", line):
            rows.append([c.strip() for c in line.strip("|").split("|")])
    return rows


def tables(block: str) -> list[list[list[str]]]:
    """Each markdown table in the block, as rows (header first)."""
    found, cur = [], []
    for line in block.splitlines() + [""]:
        if line.strip().startswith("|"):
            if not re.match(r"^\s*\|[\s:|-]+\|\s*$", line):
                cur.append([c.strip() for c in line.strip().strip("|").split("|")])
        elif cur:
            found.append(cur)
            cur = []
    return found


def strip_code(text: str) -> str:
    """Drop fenced code, inline code and HTML comments (e.g. the dg line)."""
    keep_lines = lambda m: "\n" * m.group(0).count("\n")  # noqa: E731 — preserve line numbers
    text = re.sub(r"```.*?```", keep_lines, text, flags=re.S)
    text = re.sub(r"<!--.*?-->", keep_lines, text, flags=re.S)
    return re.sub(r"`[^`\n]*`", "", text)


def bullet_groups(block: str) -> list[tuple[str, list[str]]]:
    """Split a section into groups: [(parent, [children])].

    A top-level bullet is a group; deeper-indented bullets are its children and
    wrapped lines join the item above them. Paragraphs outside any bullet and
    each table row are groups of their own, so no text escapes the checks.
    """
    groups: list[tuple[str, list[str]]] = []
    mode, blank = None, False  # mode: "bullet", "para" or "table"
    for line in block.splitlines():
        stripped = line.strip()
        if not stripped:
            blank = True
            continue
        bullet = re.match(r"^(\s*)(?:[-*+]|\d+\.)\s", line)
        indented = line[:1].isspace()
        if bullet:
            if bullet.group(1) and mode == "bullet":
                groups[-1][1].append(stripped)
            else:
                groups.append((stripped, []))
            mode = "bullet"
        elif stripped.startswith("|"):
            groups.append((stripped, []))
            mode = "table"
        elif (mode == "bullet" and (not blank or indented)) or (mode == "para" and not blank):
            parent, children = groups[-1]
            if children:
                children[-1] += " " + stripped
            else:
                groups[-1] = (parent + " " + stripped, children)
        else:
            groups.append((stripped, []))
            mode = "para"
        blank = False
    return groups


def unfilled_slots(text: str) -> list[str]:
    """Template slots left in the text. Autolinks, email addresses and HTML
    tags are fine; code spans and HTML comments (e.g. the dg line) are skipped."""
    problems = []
    for n, line in enumerate(strip_code(text).splitlines(), 1):
        if "{{" in line or "}}" in line:
            problems.append(f"line {n}: unfilled '{{{{…}}}}' slot")
        for sm in SLOT.finditer(line):
            inner = sm.group(2)
            if "://" in inner or inner.lower().startswith("mailto:") or re.fullmatch(r"[^\s@]+@[^\s@]+\.\w+", inner):
                continue
            tag = re.match(r"[A-Za-z]+", inner).group(0).lower()
            if tag not in HTML_TAGS:
                problems.append(f"line {n}: unfilled slot {sm.group(0)!r}")
    return problems


def numbered(block: str) -> list[str]:
    return [p for p, _ in bullet_groups(block) if re.match(r"\d+\. ", p)]


def score_cell(cell: str) -> int | None:
    m = re.search(r"(\d+)\s*/\s*(5|25)\b", cell.replace("*", ""))
    return int(m.group(1)) if m else None


def version_tuple(v) -> tuple[int, int, int] | None:
    m = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", str(v))
    return tuple(int(x) for x in m.groups()) if m else None


# --- Path to the next band (v0.4.0+) -----------------------------------------

PATH_KINDS = ("outcome", "rubric-only")
ARROW = r"\s*(?:→|->)\s*"


def next_band(score: int, bands: list[tuple[int, str]]) -> tuple[int, str] | None:
    """The band above `score` as (floor, label), or None in the top band."""
    above = [(floor, label) for floor, label in bands if floor > score]
    return min(above) if above else None


def path_errors(verdict: str, dg: dict) -> list[str]:
    """The Verdict's Path to the next band block: its gap arithmetic matches
    the dg line, every move starts at today's score and names a real rubric
    row, kinds are honest labels, and no projected total sneaks in."""
    head = re.search(r"^\*\*Path to the next band:?\*\*:?[ \t]*(?P<rest>.*)$", verdict, re.M)
    if not head:
        return ["## Verdict needs a '**Path to the next band:**' block under the scores"]
    problems = []
    caps = re.search(r"^\*\*Locked by caps:?\*\*:?[ \t]*\S.*$", verdict[head.end():], re.M)
    block = verdict[head.start(): head.end() + caps.end()] if caps else verdict[head.start():]
    if not caps:
        problems.append("the path block must end with a '**Locked by caps:**' line (or 'none')")
    rest = head.group("rest")
    for name, total, bands in (("Bigness", dg["bigness"], BIGNESS_BANDS), ("Moat", dg["moat"], MOAT_BANDS)):
        nb = next_band(total, bands)
        if nb is None:
            top = re.search(rf"\b{name}\s+(\d+)\s*[—–-]+\s*top band", rest, re.I)
            if not top or int(top.group(1)) != total:
                problems.append(f"{name} {total} is in its top band: the path line must say "
                                f"'{name} {total} — top band: …'")
            continue
        want = f"'{name} {total} → {nb[0]} ({nb[1]}) needs +{nb[0] - total}'"
        m = re.search(rf"\b{name}\s+(\d+){ARROW}(\d+)\s*\(([^)]+)\)\s*needs\s*\+\s*(\d+)", rest)
        if not m:
            problems.append(f"the path line must state {want}")
        elif (int(m.group(1)), int(m.group(2)), m.group(3).strip(), int(m.group(4))) != (
                total, nb[0], nb[1], nb[0] - total):
            problems.append(f"the path line's {name} arithmetic is off: it should read {want}")
    if re.search(r"\b\d{1,2}\s*/\s*25\b", block):
        problems.append("the path block must not project a total (…/25): a point counts once its "
                        "evidence exists, and the next run scores it")

    moves = [t for t in tables(block) if t and any(c.replace("*", "").strip().lower() == "raises"
                                                     for c in t[0])]
    if not moves:
        return problems + ["the path block needs its moves table (columns #, Move, Raises, "
                           "Now → next, The next point needs, Kind, Effort)"]
    header = [c.replace("*", "").strip().lower() for c in moves[0][0]]

    def col(prefix: str) -> int | None:
        return next((i for i, c in enumerate(header) if c.startswith(prefix)), None)

    idx = {k: col(k) for k in ("raises", "now", "the next point", "kind", "effort")}
    if None in idx.values():
        missing = [k for k, v in idx.items() if v is None]
        return problems + [f"the path table is missing columns: {', '.join(missing)}"]
    rows = moves[0][1:]
    if not 2 <= len(rows) <= 5:
        problems.append(f"the path table needs 2–5 moves (found {len(rows)})")
    raised, kinds = set(), []
    for r in rows:
        cell = lambda k: r[idx[k]].strip() if idx[k] < len(r) else ""  # noqa: E731
        num = r[0].strip()
        if not re.fullmatch(r"\d+", num):
            problems.append(f"path table rows must start with a move number, not {num[:30]!r}")
            continue
        target = cell("raises").replace("*", "").strip()
        if target in SUB_KEYS:
            today, raised_kind = dg["subs"].get(SUB_KEYS[target]), "bigness"
        elif target in MOAT_ROWS:
            today, raised_kind = dg["moat_rows"].get(MOAT_ROWS[target]), "moat"
        else:
            problems.append(f"path move {num} raises {target!r}, which is not a Bigness dimension "
                            "or Moat row (use the exact name)")
            continue
        raised.add(raised_kind)
        step = re.fullmatch(rf"(\d){ARROW}(\d)", cell("now").replace("*", ""))
        if not step:
            problems.append(f"path move {num}: 'Now → next' must read like '2 → 3'")
        else:
            a, b = int(step.group(1)), int(step.group(2))
            if a != today:
                problems.append(f"path move {num}: {target} is {today} today, not {a}")
            if not a < b <= 5:
                problems.append(f"path move {num}: {a} → {b} must raise the score, to at most 5")
        if not cell("the next point"):
            problems.append(f"path move {num}: quote the anchor the move would meet")
        kind = cell("kind").strip("`*_ ").lower()
        kinds.append(kind)
        if kind not in PATH_KINDS:
            problems.append(f"path move {num}: Kind must be 'outcome' or 'rubric-only', not {kind!r}")
        if cell("effort").strip("*") not in ("S", "M", "L"):
            problems.append(f"path move {num}: Effort must be S, M or L")
    if kinds and "outcome" not in kinds:
        problems.append("every path move is rubric-only: that's score gaming — add an outcome move "
                        "or say there is no cheap path")
    if next_band(dg["bigness"], BIGNESS_BANDS) and "bigness" not in raised:
        problems.append("the path needs at least one move that raises a Bigness dimension")
    if next_band(dg["moat"], MOAT_BANDS) and "moat" not in raised:
        problems.append("the path needs at least one move that raises a Moat row")
    return problems


# --- The check ---------------------------------------------------------------

def check(path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    text = path.read_text(encoding="utf-8")

    if not re.match(r"# Strategy Report — \S", text):
        errors.append("first line must be '# Strategy Report — <product name>'")

    # Sections present, in order.
    pos = -1
    for heading in SECTIONS:
        m = re.search(rf"^{heading}", text, re.M)
        if not m:
            errors.append(f"missing section: {heading.replace(chr(92), '')}")
        elif m.start() < pos:
            errors.append(f"section out of order: {heading.replace(chr(92), '')}")
        else:
            pos = m.start()

    # Machine-readable dg line.
    dg = None
    m = re.search(r"<!-- dg: (\{.*?\}) -->", text)
    if not m:
        errors.append("missing the '<!-- dg: {...} -->' line under the title")
    else:
        try:
            dg = json.loads(m.group(1))
        except json.JSONDecodeError as exc:
            errors.append(f"dg line is not valid JSON: {exc}")
    if dg is not None:
        for key in ("v", "rubric", "date", "mode", "web", "bigness", "subs", "confidence",
                    "moat", "moat_rows"):
            if key not in dg:
                errors.append(f"dg line missing key {key!r}")
        if "rubric" in dg and dg["rubric"] != RUBRIC_VERSION:
            errors.append(f"dg.rubric must be {RUBRIC_VERSION} (the rubric this checker enforces)")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(dg.get("date", ""))):
            errors.append("dg.date must be the run's UTC date as YYYY-MM-DD")
        subs = dg.get("subs") if isinstance(dg.get("subs"), dict) else {}
        rows = dg.get("moat_rows") if isinstance(dg.get("moat_rows"), dict) else {}
        if sorted(subs) != sorted(SUB_KEYS.values()):
            errors.append(f"dg.subs must have keys {sorted(SUB_KEYS.values())}")
        if sorted(rows) != sorted(MOAT_ROWS.values()):
            errors.append(f"dg.moat_rows must have keys {sorted(MOAT_ROWS.values())}")
        values = list(subs.values()) + list(rows.values())
        if any(isinstance(v, bool) or not isinstance(v, int) or not 0 <= v <= 5 for v in values):
            errors.append("dg sub-scores must be integers 0–5")
        elif subs and rows:
            if sum(subs.values()) != dg.get("bigness"):
                errors.append(f"dg.bigness is {dg.get('bigness')} but its subs sum to {sum(subs.values())}")
            if sum(rows.values()) != dg.get("moat"):
                errors.append(f"dg.moat is {dg.get('moat')} but its moat_rows sum to {sum(rows.values())}")
        if dg.get("mode") not in ("parallel", "generic-subagents", "sequential"):
            errors.append("dg.mode must be parallel, generic-subagents or sequential")
        if dg.get("confidence") not in ("High", "Medium", "Low"):
            errors.append("dg.confidence must be High, Medium or Low")
        if not isinstance(dg.get("web"), bool):
            errors.append("dg.web must be true or false")
        if f"Generated by distribution-god v{dg.get('v')}" not in text:
            errors.append(f"fingerprint 'Generated by distribution-god v{dg.get('v')}' missing")
        if "v" in dg and version_tuple(dg["v"]) is None:
            errors.append('dg.v must be the plugin version as MAJOR.MINOR.PATCH, e.g. "0.4.0"')
    v4 = dg is not None and (version_tuple(dg.get("v")) or (0, 0, 0)) >= V4
    scores_ok = (dg is not None
                 and all(isinstance(dg.get(k), int) and not isinstance(dg.get(k), bool)
                         and 0 <= dg[k] <= 25 for k in ("bigness", "moat")))
    if dg is not None and not scores_ok:
        errors.append("dg.bigness and dg.moat must be integers 0–25")

    # Verdict table.
    verdict = section(text, r"## Verdict")
    vrows = {r[0].replace("*", "").strip(): r for r in table_rows(verdict) if len(r) >= 2}
    big_row = vrows.get("Bigness")
    moat_row = vrows.get("Moat today")
    if not big_row or not moat_row:
        errors.append("Verdict table needs 'Bigness' and 'Moat today' rows")
    elif scores_ok:
        cell = big_row[1]
        if score_cell(cell) != dg["bigness"]:
            errors.append(f"Verdict Bigness shows {score_cell(cell)}/25 but dg.bigness is {dg['bigness']}")
        band = band_for(dg["bigness"], BIGNESS_BANDS)
        if band not in cell:
            errors.append(f"Verdict Bigness must name the band '{band}'")
        if dg.get("confidence") == "Low" and "PROVISIONAL" not in cell:
            errors.append("Low confidence: the Bigness headline must read '(PROVISIONAL — Low confidence: …)'")
        if dg.get("confidence") in ("High", "Medium") and dg["confidence"] not in cell:
            errors.append(f"Verdict Bigness must state confidence: {dg['confidence']}")
        mcell = moat_row[1]
        if score_cell(mcell) != dg["moat"]:
            errors.append(f"Verdict Moat shows {score_cell(mcell)}/25 but dg.moat is {dg['moat']}")
        mband = band_for(dg["moat"], MOAT_BANDS)
        if mband.lower() not in mcell.lower():
            errors.append(f"Verdict Moat must name the band '{mband}'")

    # Bigness breakdown and Moat today tables agree with dg.
    def check_breakdown(block: str, labels: dict, dg_key: str, total_key: str, name: str):
        found = {}
        for r in table_rows(block):
            label = r[0].replace("*", "").strip()
            if label in labels and len(r) >= 2:
                found[labels[label]] = score_cell(r[1])
                if len(r) < 3 or not r[2].strip():
                    errors.append(f"{name}: '{label}' has no evidence")
            if label == "Total" and len(r) >= 2 and dg is not None:
                if score_cell(r[1]) != dg.get(total_key):
                    errors.append(f"{name}: Total {score_cell(r[1])} ≠ dg.{total_key} {dg.get(total_key)}")
        if len(found) != 5:
            missing = sorted(set(labels) - {k for k, v in labels.items() if v in found})
            errors.append(f"{name} table is missing rows: {', '.join(missing)}")
        elif dg is not None and isinstance(dg.get(dg_key), dict):
            for key, val in found.items():
                if dg[dg_key].get(key) != val:
                    errors.append(f"{name}: {key} shows {val} but dg.{dg_key}.{key} is {dg[dg_key].get(key)}")

    check_breakdown(verdict, SUB_KEYS, "subs", "bigness", "Bigness breakdown")
    check_breakdown(section(text, r"## 7\. Moat roadmap"), MOAT_ROWS, "moat_rows", "moat", "Moat today")

    # v0.4.0+: the action parts.
    dg_ok = (scores_ok and isinstance(dg.get("subs"), dict) and isinstance(dg.get("moat_rows"), dict))
    if v4 and dg_ok:
        errors.extend(path_errors(verdict, dg))

    # Unfilled template slots (autolinks like <https://…> are fine).
    errors.extend(unfilled_slots(text))

    # Market: labels, sources, arithmetic; no-web runs say so.
    market = section(text, r"## 2\. Market")
    field = section(text, r"## 3\. Competitive field")
    offline = dg is not None and dg.get("web") is False
    for name, block in (("2", market), ("3", field)):
        says = "NOT RESEARCHED" in block
        if offline and not says:
            errors.append(f"dg.web is false but section {name} does not say 'NOT RESEARCHED'")
        if not offline and says:
            errors.append(f"section {name} says 'NOT RESEARCHED' but dg.web isn't false — only a "
                          "local-only run may skip research (write 'none found' instead)")
    if offline and isinstance((dg or {}).get("subs"), dict):
        for key in ("market", "why_now"):
            if isinstance(dg["subs"].get(key), int) and dg["subs"][key] > 2:
                errors.append(f"local-only run: dg.subs.{key} is capped at 2")
        if dg.get("confidence") != "Low":
            errors.append("local-only run: confidence must be Low")
    researched = not offline
    if researched:
        labeled = re.compile(r"ESTIMATE|(?i:unverified)")
        size_groups = []
        for parent, children in bullet_groups(market):
            group_text = " ".join([parent, *children])
            if re.match(r"[-*+]\s+\**(?:market\s+)?size\b", parent, re.I):
                size_groups.append(group_text)
                if "ESTIMATE" not in group_text:
                    errors.append("the market Size bullet must be labeled ESTIMATE")
            parent_ok = bool(labeled.search(parent) or LINK.search(parent))
            for item in [parent, *children]:
                if MONEY.search(item) and not (parent_ok or labeled.search(item) or LINK.search(item)):
                    errors.append("market figure without ESTIMATE, 'unverified' or a source link: "
                                  f"{item[:90]!r}")
        plain = re.sub(r"<!--.*?-->", "", market, flags=re.S)  # inline code still counts
        errors.extend(arithmetic_errors(plain))
        if not size_groups:
            errors.append("section 2 needs a '**Size:**' bullet with the ESTIMATE range")
        for group_text in size_groups[:1]:
            errors.extend(size_consistency(group_text, dg))

    # Rivals carry sources.
    no_rivals = re.search(r"only 0 direct rivals|no direct rivals found", field, re.I)
    if researched and not no_rivals:
        def source_col(header):
            return next((i for i, c in enumerate(header) if "source" in c.replace("*", "").lower()), None)
        rival_tables = [t for t in tables(field) if t and source_col(t[0]) is not None]
        if not rival_tables:
            errors.append("Competitive field table needs a Source column "
                          "(or write 'only 0 direct rivals found')")
        else:
            src = source_col(rival_tables[0][0])
            data = rival_tables[0][1:]
            if not data:
                errors.append("Competitive field table has no rivals")
            for r in data:
                cell = r[src] if src < len(r) else ""
                if "http" not in cell and "unverified" not in cell.lower():
                    errors.append(f"rival '{r[0][:40]}' has no source link (or 'unverified')")

    # Exactly one PRIMARY channel, counted in the channel table only.
    plan = section(text, r"## 5\. Distribution plan")
    channel_tables = [t for t in tables(plan) if t and t[0] and t[0][-1].replace("*", "").strip() == "Call"]
    if len(channel_tables) != 1:
        errors.append("section 5 needs one channel-ranking table whose last column is 'Call'")
    else:
        calls = [r[-1].replace("*", "").strip() for r in channel_tables[0][1:]]
        primaries = sum(1 for c in calls if re.match(r"PRIMARY\b", c))
        if primaries != 1:
            errors.append(f"channel table must mark exactly one PRIMARY channel (found {primaries})")

    # Five next actions.
    actions = numbered(section(text, r"## 10\. Next 5 actions"))
    if len(actions) != 5:
        errors.append(f"section 10 must list exactly 5 numbered actions (found {len(actions)})")

    # Red-team record.
    if "Red-team adjustments" not in section(text, r"## Dissent"):
        errors.append("Dissent must start with a 'Red-team adjustments:' line")

    # Strategy card: exists, parses, shows the report's scores.
    card = re.search(r"!\[Strategy card\]\(([^)]+)\)", verdict)
    if card:
        svg_path = (path.parent / card.group(1)).resolve()
        if not svg_path.exists():
            errors.append(f"strategy card linked but missing: {card.group(1)}")
        else:
            svg = svg_path.read_text(encoding="utf-8")
            try:
                validate_svg_text(svg)
            except CardError as exc:
                errors.append(f"strategy card {card.group(1)}: {exc}")
            else:
                if scores_ok:
                    errors.extend(card_mismatches(svg, dg, card.group(1)))
    else:
        warnings.append("no strategy card linked under ## Verdict")

    lines = text.count("\n")
    budget = LINE_BUDGET_V4 if v4 else LINE_BUDGET
    if lines > budget:
        warnings.append(f"report is {lines} lines; the template targets under ~{budget}")
    return errors, warnings


def size_consistency(group_text: str, dg: dict | None) -> list[str]:
    """The Size headline must match its own calculation, its stated geometric
    midpoint, and the Market headroom sub-score's dollar band."""
    problems = []
    head = re.search(r"ESTIMATE:?\s*", group_text)
    toks = _tokens(group_text[head.end():]) if head else []
    if not toks or toks[0][0] != "num":
        return ["the Size bullet must state its range right after ESTIMATE, e.g. 'ESTIMATE $12M–$126M'"]
    lo, hi = toks[0][1]
    calcs = calculations(group_text)
    if calcs and not any(_close(c["got"][0], lo) and _close(c["got"][1], hi) for c in calcs):
        problems.append(f"the Size headline {_fmt(lo)}–{_fmt(hi)} doesn't match the result of any "
                        "calculation written under it")
    elif not calcs and not LINK.search(group_text):
        problems.append("the Size bullet must show its calculation (a × b = c) or link a source")
    if lo <= 0 or hi < lo:
        return problems
    mid = (lo * hi) ** 0.5
    stated = re.search(r"geometric midpoint[^$€£\d~≈]{0,20}", group_text, re.I)
    if stated:
        after = _tokens(group_text[stated.end():])
        if after and after[0][0] == "num" and not _close(after[0][1][0], mid, 0.10):
            problems.append(f"stated geometric midpoint {_fmt(after[0][1][0])} ≠ √(low × high) = {_fmt(mid)}")
    subs = (dg or {}).get("subs")
    if isinstance(subs, dict) and isinstance(subs.get("market"), int):
        band = headroom_band(mid)
        if subs["market"] != band:
            problems.append(f"Market headroom is scored {subs['market']} but the SAM geometric midpoint "
                            f"{_fmt(mid)} falls in band {band}")
    return problems


def card_mismatches(svg: str, dg: dict, name: str) -> list[str]:
    """Compare the card's headline and breakdown numbers with the dg line."""
    problems = []
    m = re.search(r'aria-label="[^"]*Bigness (\d+) of 25, Moat (\d+) of 25', svg)
    if not m:
        return [f"strategy card {name}: can't read its scores (was it rendered by strategy_card.py?)"]
    if (int(m.group(1)), int(m.group(2))) != (dg["bigness"], dg["moat"]):
        problems.append(f"strategy card {name} shows Bigness {m.group(1)}, Moat {m.group(2)} "
                        f"but the report says {dg['bigness']}, {dg['moat']} — re-render it")
    conf = re.search(r'class="conf"[^>]*>([^<]+)</text>', svg)
    want_conf = ("LOW · PROVISIONAL" if dg.get("confidence") == "Low"
                 else f"{str(dg.get('confidence', '')).upper()} CONFIDENCE")
    if conf and conf.group(1).strip() != want_conf:
        problems.append(f"strategy card {name} says '{conf.group(1).strip()}' but the report's "
                        f"confidence is {dg.get('confidence')} — re-render it")
    stamp = re.search(r"Generated by distribution-god v([\w.]+) · (\d{4}-\d{2}-\d{2})", svg)
    if stamp and (stamp.group(1), stamp.group(2)) != (str(dg.get("v")), str(dg.get("date"))):
        problems.append(f"strategy card {name} is stamped v{stamp.group(1)} · {stamp.group(2)} but the "
                        f"report is v{dg.get('v')} · {dg.get('date')} — re-render it")
    labels = re.findall(r'class="row">([^<]+)</text>', svg)
    nums = re.findall(r'class="num"[^>]*>(\d+)/5</text>', svg)
    subs = dg.get("subs") if isinstance(dg.get("subs"), dict) else {}
    for label, num in zip(labels, nums):
        key = SUB_KEYS.get(label.strip())
        if key and subs.get(key) != int(num):
            problems.append(f"strategy card {name}: {label.strip()} shows {num}/5 but dg.subs.{key} "
                            f"is {subs.get(key)} — re-render it")
    return problems


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
