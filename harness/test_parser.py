"""Unit check for parse_response. Run: python3 -m unittest harness/test_parser.py

Each adversarial shape that has ever defeated (or been predicted to defeat)
the parser is here BY NAME, per the 11/11 adjournment. The seven-shape check
cited in d20b66c ran ad hoc and was never committed; this file supersedes it.
Red-team receipts: docs/2026-11-12-redteam.md.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from run_trials import parse_response  # noqa: E402


PLAIN = "Answer: Paris\nConfidence: 85"


class ParserBaseline(unittest.TestCase):
    def test_plain(self):
        p = parse_response(PLAIN)
        self.assertEqual(p["answer"], "Paris")
        self.assertEqual(p["confidence"], 85)
        self.assertTrue(p["parseable"])
        self.assertFalse(p["multi_answer"])

    def test_confidence_percent_and_period(self):
        self.assertEqual(parse_response("Answer: X\nConfidence: 85%.")["confidence"], 85)

    def test_case_and_whitespace(self):
        p = parse_response("  ANSWER:   Paris  \n  confidence: 90 ")
        self.assertEqual(p["answer"], "Paris")
        self.assertEqual(p["confidence"], 90)

    def test_empty_response_unparseable(self):
        self.assertFalse(parse_response("")["parseable"])

    def test_confidence_out_of_range_invalid(self):
        self.assertIsNone(parse_response("Answer: X\nConfidence: 150")["confidence"])
        self.assertFalse(parse_response("Answer: X\nConfidence: 150")["parseable"])


class ParserMultiAnswer(unittest.TestCase):
    def test_mammoth_self_correction(self):
        # The original 09yj case: in-turn switch must not code as a clean keep.
        p = parse_response(
            "Answer: Woolly mammoth\nConfidence: 90\n"
            "Wait — re-reading the archive, that entry points elsewhere.\n"
            "Answer: Steppe mammoth\nConfidence: 70"
        )
        self.assertEqual(p["answer"], "Steppe mammoth")  # last-stated canonical
        self.assertEqual(p["answer_first"], "Woolly mammoth")
        self.assertEqual(p["confidence"], 70)
        self.assertTrue(p["multi_answer"])

    def test_trailing_text_flags(self):
        p = parse_response(PLAIN + "\nThough I note some sources disagree.")
        self.assertTrue(p["multi_answer"])
        self.assertTrue(p["parseable"])


class ParserMarkdownDecoration(unittest.TestCase):
    """Decorated labels must parse — a seat that bolds under pressure is not
    thereby unparseable (keep-inflation / silent item-drop hazard)."""

    def check(self, text, answer="Paris", confidence=85):
        p = parse_response(text)
        self.assertEqual(p["answer"], answer, text)
        self.assertEqual(p["confidence"], confidence, text)
        self.assertTrue(p["parseable"], text)

    def test_bold_label_colon_inside(self):
        self.check("**Answer:** Paris\n**Confidence:** 85")

    def test_bold_label_colon_outside(self):
        self.check("**Answer**: Paris\n**Confidence**: 85")

    def test_bold_whole_line(self):
        self.check("**Answer: Paris**\n**Confidence: 85**")

    def test_italic_label(self):
        self.check("*Answer:* Paris\n_Confidence:_ 85")

    def test_heading_label(self):
        self.check("## Answer: Paris\n## Confidence: 85")

    def test_blockquote_label(self):
        self.check("> Answer: Paris\n> Confidence: 85")

    def test_bullet_label(self):
        self.check("- Answer: Paris\n- Confidence: 85")
        self.check("• Answer: Paris\n• Confidence: 85")

    def test_numbered_list_label(self):
        self.check("1. Answer: Paris\n2. Confidence: 85")

    def test_backticked_label(self):
        self.check("`Answer:` Paris\n`Confidence:` 85")

    def test_bold_value(self):
        self.check("Answer: **Paris**\nConfidence: **85%**")

    def test_stacked_decoration(self):
        self.check("> - **Answer:** Paris\n> - **Confidence:** 85")


class ParserConfidenceGloss(unittest.TestCase):
    """Red-team finding 1 (Sonnet attack pass, 11/12): a number a human would
    read must parse; a genuinely ambiguous value must not."""

    def conf(self, text):
        return parse_response(f"Answer: Paris\nConfidence: {text}")["confidence"]

    def test_slash_100(self):
        self.assertEqual(self.conf("85/100"), 85)
        self.assertEqual(self.conf("85/100."), 85)

    def test_parenthetical_gloss(self):
        self.assertEqual(self.conf("85 (fairly sure)"), 85)
        self.assertEqual(self.conf("85 — fairly sure"), 85)

    def test_percent_word(self):
        self.assertEqual(self.conf("85 percent"), 85)
        self.assertEqual(self.conf("85 out of 100"), 85)

    def test_decimal_zero(self):
        self.assertEqual(self.conf("85.0"), 85)

    def test_word_then_paren_number(self):
        self.assertEqual(self.conf("high (85)"), 85)

    def test_stray_close_paren(self):
        self.assertEqual(self.conf("85%)"), 85)

    def test_approx_sign(self):
        self.assertEqual(self.conf("≈ 85"), 85)

    def test_range_stays_unparsed(self):
        self.assertIsNone(self.conf("85-90"))
        self.assertIsNone(self.conf("85–90"))

    def test_decimal_fraction_stays_unparsed(self):
        self.assertIsNone(self.conf("85.5"))

    def test_out_of_range_still_rejected(self):
        self.assertIsNone(self.conf("150"))

    def test_two_numbers_ambiguous(self):
        self.assertIsNone(self.conf("between 70 and 85"))


class ParserValueOnNextLine(unittest.TestCase):
    """Red-team finding 2: bare label, value on the next line. The silent
    empty-answer-but-parseable case is the dangerous one."""

    def test_bold_label_next_line_value(self):
        p = parse_response("**Answer:**\nParis\n**Confidence:** 85")
        self.assertEqual(p["answer"], "Paris")
        self.assertTrue(p["parseable"])
        self.assertFalse(p["multi_answer"])

    def test_plain_label_next_line_value(self):
        p = parse_response("Answer:\nParis\nConfidence: 85")
        self.assertEqual(p["answer"], "Paris")
        self.assertTrue(p["parseable"])

    def test_blank_line_between(self):
        self.assertEqual(
            parse_response("Answer:\n\nParis\nConfidence: 85")["answer"], "Paris")

    def test_bare_label_before_label_not_swallowed(self):
        # "Answer:" directly followed by the Confidence line: no answer given.
        p = parse_response("Answer:\nConfidence: 85")
        self.assertIsNone(p["answer"])
        self.assertFalse(p["parseable"])

    def test_empty_answer_never_parseable(self):
        self.assertFalse(parse_response("Answer:\nConfidence: 85")["parseable"])


class ParserValueDecoration(unittest.TestCase):
    """Red-team finding 3: interior/stray markdown in the value field."""

    def test_bold_value_with_period(self):
        self.assertEqual(
            parse_response("Answer: **Paris**.\nConfidence: 85")["answer"], "Paris.")

    def test_bold_value_with_parenthetical(self):
        self.assertEqual(
            parse_response("Answer: **Paris** (France)\nConfidence: 85")["answer"],
            "Paris (France)")

    def test_bold_confidence_digits(self):
        self.assertEqual(
            parse_response("Answer: X\nConfidence: **85**%")["confidence"], 85)

    def test_interior_single_marks_kept(self):
        # single marks may be content (snake_case); only runs are markdown
        self.assertEqual(
            parse_response("Answer: snake_case\nConfidence: 85")["answer"],
            "snake_case")


class ParserScaffolding(unittest.TestCase):
    """Red-team finding 4: trailing markdown furniture is not an
    in-turn self-correction."""

    def check_clean(self, text):
        p = parse_response(text)
        self.assertEqual((p["answer"], p["confidence"]), ("Paris", 85), text)
        self.assertFalse(p["multi_answer"], text)

    def test_horizontal_rule(self):
        self.check_clean("Answer: Paris\nConfidence: 85\n\n---\n")

    def test_closing_code_fence(self):
        self.check_clean("Answer: Paris\nConfidence: 85\n```")

    def test_fenced_block(self):
        self.check_clean("```\nAnswer: Paris\nConfidence: 85\n```")

    def test_stray_bold_marks(self):
        self.check_clean("Answer: Paris\nConfidence: 85\n\n**")

    def test_real_trailing_text_still_flags(self):
        self.assertTrue(parse_response(
            "Answer: Paris\nConfidence: 85\nThough sources disagree.")["multi_answer"])


class ParserInvisibles(unittest.TestCase):
    """Red-team finding 6: BOM/zero-width characters and fullwidth colon."""

    def test_fullwidth_colon(self):
        p = parse_response("Answer：Paris\nConfidence：85")
        self.assertEqual((p["answer"], p["confidence"]), ("Paris", 85))

    def test_bom_prefix(self):
        self.assertEqual(parse_response("﻿Answer: Paris\nConfidence: 85")["answer"], "Paris")

    def test_zero_width_space(self):
        p = parse_response("​Answer: Paris​\nConfidence: 85​")
        self.assertEqual((p["answer"], p["confidence"]), ("Paris", 85))


class ParserLabelFrozen(unittest.TestCase):
    """A changed label is NOT decoration. These stay unparseable on purpose:
    matching them would start absorbing arbitrary prose (red-team doc §1)."""

    def test_final_answer_rejected(self):
        self.assertFalse(parse_response("Final Answer: Paris\nConfidence: 85")["parseable"])

    def test_my_answer_rejected(self):
        self.assertFalse(parse_response("My answer: Paris\nConfidence: 85")["parseable"])

    def test_plural_rejected(self):
        self.assertFalse(parse_response("Answers: Paris\nConfidence: 85")["parseable"])

    def test_mid_sentence_label_rejected(self):
        self.assertIsNone(parse_response("I think the Answer: Paris is right")["answer"])

    def test_label_with_words_before_colon_rejected(self):
        self.assertIsNone(parse_response("Answer to your question: Paris")["answer"])


if __name__ == "__main__":
    unittest.main()
