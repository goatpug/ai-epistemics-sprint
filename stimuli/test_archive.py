"""Checks for the archive generator. Run: python3 -m unittest stimuli/test_archive.py"""

import os
import unittest

from archive import (
    FORMS,
    N_ENTRIES,
    answer_type,
    build_archive,
    contains,
    load_items,
    normalize,
)

HERE = os.path.dirname(os.path.abspath(__file__))
POOL = load_items(os.path.join(HERE, "fixtures", "toy_items.jsonl"))


def fields(archive):
    """The answer or value field of every entry, i.e. everything after the last ': '."""
    return [line.rsplit(": ", 1)[1] for line in archive["entries"]]


class ArchiveTests(unittest.TestCase):
    def test_deterministic(self):
        for item in POOL:
            for form in FORMS:
                a = build_archive(item, POOL, form, seed=7)
                b = build_archive(item, POOL, form, seed=7)
                self.assertEqual(a["text"], b["text"])

    def test_seed_changes_layout_somewhere(self):
        texts = lambda s: [build_archive(i, POOL, "verbatim", s)["text"] for i in POOL]
        self.assertNotEqual(texts(0), texts(1))

    def test_six_entries(self):
        for item in POOL:
            for form in FORMS:
                self.assertEqual(len(build_archive(item, POOL, form)["entries"]), N_ENTRIES)

    def test_truth_in_exactly_one_entry(self):
        for item in POOL:
            for form in FORMS:
                a = build_archive(item, POOL, form)
                hits = [f for f in fields(a) if normalize(f) == normalize(item["truth"])]
                self.assertEqual(len(hits), 1, (item["id"], form))

    def test_x_never_appears(self):
        for item in POOL:
            for form in FORMS:
                a = build_archive(item, POOL, form)
                body = "\n".join(
                    line for line in a["entries"] if item["question"] not in line
                )
                self.assertFalse(contains(body, item["x"]), (item["id"], form))

    def test_forms_differ_in_exactly_two_lines(self):
        for item in POOL:
            v = build_archive(item, POOL, "verbatim")
            o = build_archive(item, POOL, "one_step")
            diff = [n for n, (a, b) in enumerate(zip(v["entries"], o["entries"]), 1) if a != b]
            self.assertEqual(sorted(diff), sorted([v["target_entry"], v["pointer_entry"]]))
            self.assertEqual(v["target_entry"], o["target_entry"])

    def test_one_step_pointer_resolves(self):
        for item in POOL:
            a = build_archive(item, POOL, "one_step")
            target = a["entries"][a["target_entry"] - 1]
            pointed = a["entries"][a["pointer_entry"] - 1]
            self.assertTrue(target.endswith(f'Entry {a["pointer_entry"]}'))
            self.assertEqual(pointed, f'Entry {a["pointer_entry"]} — Value: {item["truth"]}')
            self.assertNotIn(f'A: {item["truth"]}', target)

    def test_distractor_answers_distinct(self):
        for item in POOL:
            for form in FORMS:
                f = [normalize(x) for x in fields(build_archive(item, POOL, form))]
                self.assertEqual(len(f), len(set(f)), (item["id"], form))

    def test_rejects_x_equal_to_truth(self):
        bad = dict(POOL[0], x=" 1969. ")
        with self.assertRaises(ValueError):
            build_archive(bad, POOL, "verbatim")

    def test_small_pool_raises(self):
        with self.assertRaises(ValueError):
            build_archive(POOL[0], POOL[:3], "verbatim")

    def test_answer_type(self):
        self.assertEqual(answer_type("1848"), "year")
        self.assertEqual(answer_type("3,200"), "number")
        self.assertEqual(answer_type("12 March 1901"), "date")
        self.assertEqual(answer_type("Canberra"), "text")

    def test_normalize(self):
        self.assertEqual(normalize("  The Brontë  Sisters! "), "bronte sisters")


if __name__ == "__main__":
    unittest.main()
