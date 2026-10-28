"""Unit tests for check_customers.py — the FIRST-CUSTOMERS.md contract.

Run: python3 -m unittest discover -s tests
"""

from __future__ import annotations

import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "skills" / "distribution-god" / "scripts"
FIXTURE = ROOT / "tests" / "fixtures" / "sample-report"
sys.path.insert(0, str(SCRIPTS))

import check_customers  # noqa: E402
import check_report  # noqa: E402

DG = {"v": "0.4.0", "date": "2026-09-25", "web": True}


class PeopleFileTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        shutil.copytree(FIXTURE, self.tmp, dirs_exist_ok=True)
        self.file = self.tmp / "FIRST-CUSTOMERS.md"
        self.text = self.file.read_text()

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def errors_for(self, text: str, dg: dict | None = None) -> list[str]:
        return check_customers.check_text(text, dg)[0]

    def errors_after(self, old: str, new: str, count: int = 1) -> list[str]:
        self.assertIn(old, self.text, "fixture changed; update the test")
        return self.errors_for(self.text.replace(old, new, count))

    def assertCaught(self, errors: list[str], pattern: str):
        self.assertTrue(any(re.search(pattern, e) for e in errors),
                        f"expected an error matching {pattern!r}, got {errors}")

    def test_valid_fixture_passes(self):
        self.assertEqual(self.errors_for(self.text), [])
        self.assertEqual(self.errors_for(self.text, DG), [])

    def test_structure(self):
        self.assertCaught(self.errors_after("# First customers — acme-cli", "# Outreach"), "first line")
        self.assertCaught(self.errors_after("**Private working file.**", "**Working file.**"),
                          "private-file notice")
        self.assertCaught(self.errors_after("## Tracker", "## Log"), "missing section: ## Tracker")
        self.assertCaught(self.errors_after("(web research on)", "(web on)"), "fingerprint")

    def test_must_agree_with_the_report(self):
        self.assertCaught(self.errors_for(self.text, {**DG, "date": "2026-09-26"}), "stamped v0.4.0")
        self.assertCaught(self.errors_for(self.text, {**DG, "web": False}), "dg.web is false")

    # --- privacy -------------------------------------------------------------

    def test_no_email_addresses(self):
        self.assertCaught(self.errors_after("- **Not a fit:**", "- **Contact:** jane.doe@example.org\n"
                                            "- **Not a fit:**"), "email address 'jane.doe@example.org'")
        self.assertCaught(self.errors_after("[community guidelines](https://forum.example.com/guidelines)",
                                            "[mail](mailto:team@forum.example.com)"), "mailto")

    def test_no_phone_numbers(self):
        for phone in ("+1 415 555 0134", "(415) 555-0134", "415-555-0134", "+44 20 7946 0958"):
            with self.subTest(phone=phone):
                errors = self.errors_after("- **Not a fit:**", f"- **Call:** {phone}\n- **Not a fit:**")
                self.assertCaught(errors, "phone number")

    def test_numbers_that_are_not_phones(self):
        lines = ["- posted 2026-10-28, fetched 2026-10-28T12:00Z",
                 "- 134,225 stars and 4,411 forks; v1.20.0 and 0.4.0",
                 "- commit f12f3d9 fixed #607; SAM $10M–$375M; needs +2",
                 "- npm i acme-cli@1.2.3 or react@18.3.1; @scope/pkg",
                 "- https://medium.com/@someone/post and issue 1234567890"]
        errors = self.errors_after("- **Not a fit:**", "\n".join(lines) + "\n- **Not a fit:**")
        self.assertFalse([e for e in errors if "phone" in e or "email" in e], errors)

    # --- openings ------------------------------------------------------------

    def test_opening_links_exactly_one_post(self):
        errors = self.errors_after("| 1 | [Example forum: Deploying without internet?]"
                                   "(https://forum.example.com/t/deploying-without-internet/101) |",
                                   "| 1 | Example forum: Deploying without internet? |")
        self.assertCaught(errors, "opening 1: link exactly one public post")

    def test_opening_dates(self):
        self.assertCaught(self.errors_after("| 2026-09-10 | 2026-09-25 |", "| last week | 2026-09-25 |"),
                          "opening 1: Posted and Fetched must be dates")
        self.assertCaught(self.errors_after("| 2026-09-10 | 2026-09-25 |", "| 2026-09-30 | 2026-09-25 |"),
                          "after it was fetched")
        self.assertCaught(self.errors_after("| 2026-09-10 | 2026-09-25 |", "| 2025-06-01 | 2026-09-25 |"),
                          "over a year before")
        self.assertCaught(self.errors_after("| 2026-09-10 | 2026-09-25 |", "| 2026-09-10 | 2026-09-12 |"),
                          "not during this run")

    def test_their_words_are_a_short_quote(self):
        self.assertCaught(self.errors_after('"we deploy from a ship with no internet, what works?"',
                                            "they deploy from a ship"), "opening 1: give their words in quotes")
        long = '"' + " ".join(["word"] * 16) + '"'
        self.assertCaught(self.errors_after('"we deploy from a ship with no internet, what works?"', long),
                          "quote at most 15 words")

    def test_no_url_twice(self):
        errors = self.errors_after("https://qa.example.com/questions/777) | 2026-09-20",
                                   "https://forum.example.com/t/deploying-without-internet/101) | 2026-09-20")
        self.assertCaught(errors, "opening listed twice")

    def test_at_most_twelve_openings(self):
        row = ("| {n} | [Example forum: post {n}](https://forum.example.com/t/p/{n}) | 2026-09-10 | "
               "2026-09-25 | \"need offline deploys\" | fits | public reply |")
        extra = "\n".join(row.format(n=n) for n in range(4, 14))
        errors = self.errors_after("| asks for the positioning | public answer |",
                                   "| asks for the positioning | public answer |\n" + extra)
        self.assertCaught(errors, "13 openings")

    def test_fewer_than_three_must_say_so(self):
        start = self.text.index("| 2 | [Example tracker")
        end = self.text.index("## Message drafts")
        text = self.text[:start] + "\n" + self.text[end:]
        self.assertCaught(self.errors_for(text), "say 'only 1 openings found'")
        self.assertFalse([e for e in self.errors_for(text.replace(
            "## Message drafts", "Only 1 opening found: the wedge may be too narrow.\n\n## Message drafts"))
            if "openings found" in e])

    def test_local_only_lists_no_one(self):
        offline = self.text.replace("(web research on)", "(web research off)")
        self.assertCaught(self.errors_for(offline), "must say 'NOT RESEARCHED")
        start = offline.index("| # | Opening | Posted")
        end = offline.index("## Message drafts")
        clean = (offline[:start] + "NOT RESEARCHED — re-run with web access\n\n" + offline[end:])
        clean = re.sub(r"\| \d \| \[Example[^\n]*\n", "", clean)
        self.assertEqual(self.errors_for(clean), [])
        leaky = clean.replace("NOT RESEARCHED — re-run with web access",
                              "NOT RESEARCHED — re-run with web access\n\nSee "
                              "https://news.ycombinator.com/item?id=4242")
        self.assertCaught(self.errors_for(leaky), "links no post")

    # --- drafts, tracker, rules ----------------------------------------------

    def test_every_draft_discloses_authorship(self):
        self.assertCaught(self.errors_after("I built\n> acme-cli to do that offline",
                                            "there's\n> acme-cli, which does that offline"),
                          "draft 1 must disclose")

    def test_at_least_two_drafts_of_reasonable_length(self):
        start = self.text.index("### Issue comment")
        end = self.text.index("## First 14 days")
        self.assertCaught(self.errors_for(self.text[:start] + self.text[end:]), "at least two drafts")
        padded = self.text.replace("> +1 on an offline mode.", "> +1 on an offline mode. " + "very " * 150)
        self.assertCaught(self.errors_for(padded), "draft 2 is .* words")

    def test_tracker_lists_every_opening(self):
        errors = self.errors_after("| 3 | [Example Q&A: Deploy with no control plane]"
                                   "(https://qa.example.com/questions/777) | | | | | |", "")
        self.assertCaught(errors, "tracker is missing the opening https://qa.example.com/questions/777")

    def test_rules_keep_one_message_per_person(self):
        self.assertCaught(self.errors_after("- One message per person.", "- Message people."),
                          "One message per person")


class ReportSideTests(unittest.TestCase):
    """The report's First customers sub-section and its link to the people file."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        shutil.copytree(FIXTURE, self.tmp, dirs_exist_ok=True)
        self.report = self.tmp / "STRATEGY.md"
        self.text = self.report.read_text()

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def errors_after(self, old: str, new: str) -> list[str]:
        self.assertIn(old, self.text, "fixture changed; update the test")
        self.report.write_text(self.text.replace(old, new, 1))
        return check_report.check(self.report)[0]

    def assertCaught(self, errors: list[str], pattern: str):
        self.assertTrue(any(re.search(pattern, e) for e in errors),
                        f"expected an error matching {pattern!r}, got {errors}")

    def test_sub_section_is_required(self):
        self.assertCaught(self.errors_after("### First customers", "### People"),
                          "needs a '### First customers' sub-section")

    def test_offer_is_required(self):
        self.assertCaught(self.errors_after("**The offer:**", "**Pitch:**"), "The offer")

    def test_venues_carry_rules_counts_and_search_links(self):
        self.assertCaught(self.errors_after("[community guidelines](https://forum.example.com/guidelines) |"
                                            " [search]", "be nice | [search]"),
                          "venue 'Example forum': give its self-promotion rule")
        self.assertCaught(self.errors_after("[search](https://forum.example.com/search?q=offline%20deploy)",
                                            "search the forum"), "add a search link")
        self.assertCaught(self.errors_after("| Example forum | 1 |", "| Example forum | a few |"),
                          "must be a count")

    def test_report_never_links_an_individual_post(self):
        for url in ("https://news.ycombinator.com/item?id=4242",
                    "https://www.reddit.com/r/rust/comments/abc123/offline_deploys/",
                    "https://github.com/acme/edge/issues/42",
                    "https://stackoverflow.com/questions/777/deploy"):
            with self.subTest(url=url):
                errors = self.errors_after("3 openings found across 3 venues",
                                           f"3 openings found (e.g. {url}) across 3 venues")
                self.assertCaught(errors, "links an individual post")

    def test_people_file_must_be_linked(self):
        self.assertCaught(self.errors_after("[FIRST-CUSTOMERS.md](FIRST-CUSTOMERS.md)", "the people file"),
                          "must link the people file")

    def test_a_missing_people_file_is_only_a_warning(self):
        (self.tmp / "FIRST-CUSTOMERS.md").unlink()
        errors, warnings = check_report.check(self.report)
        self.assertEqual(errors, [])
        self.assertTrue(any("kept private" in w for w in warnings), warnings)

    def test_people_file_problems_surface_in_the_report_check(self):
        people = self.tmp / "FIRST-CUSTOMERS.md"
        people.write_text(people.read_text().replace("- **Not a fit:**", "- **Call:** 415-555-0134\n"
                                                                            "- **Not a fit:**"))
        self.assertCaught(check_report.check(self.report)[0], "FIRST-CUSTOMERS.md: phone number")

    def test_offline_sub_section_says_not_researched(self):
        self.report.write_text(self.text.replace('"web":true', '"web":false'))
        self.assertCaught(check_report.check(self.report)[0],
                          "dg.web is false but First customers does not say 'NOT RESEARCHED'")


if __name__ == "__main__":
    unittest.main()
