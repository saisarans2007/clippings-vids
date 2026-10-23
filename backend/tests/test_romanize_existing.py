"""
romanize_words must keep a word's existing ``hinglish`` value. Re-running it on
an edited transcript used to replace user edits with the Devanagari text.
"""
import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from captions import romanize  # noqa: E402


class RomanizeKeepsExistingTest(unittest.TestCase):
    def setUp(self):
        # Rule path only: no LLM call in tests.
        patcher = mock.patch.object(romanize, "_llm_romanize_chunk", return_value=None)
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_existing_hinglish_is_kept(self):
        out = romanize.romanize_words([{"start": 0, "end": 1, "text": "क्या", "hinglish": "kyaa"}])
        self.assertEqual(out[0]["hinglish"], "kyaa")
        self.assertEqual(out[0]["text"], "क्या")

    def test_edited_word_kept_next_to_one_that_still_needs_romanizing(self):
        out = romanize.romanize_words([
            {"start": 0, "end": 1, "text": "क्या", "hinglish": "kyaa"},
            {"start": 1, "end": 2, "text": "मतलब"},
        ])
        self.assertEqual(out[0]["hinglish"], "kyaa")
        self.assertEqual(out[1]["hinglish"], romanize._rule_romanize("मतलब"))

    def test_latin_words_still_pass_through(self):
        out = romanize.romanize_words([{"start": 0, "end": 1, "text": "hello", "lang": "en"}])
        self.assertEqual(out[0]["hinglish"], "hello")


if __name__ == "__main__":
    unittest.main()
