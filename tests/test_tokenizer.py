import unittest

from ugnlp.tokenizer import split_sentences, split_suffixes, split_words, stems


class TestTokenizer(unittest.TestCase):
    def test_split_words_arabic(self):
        words = split_words("ئۇ بازارغا باردى ، ئاندىن قايتتى")
        self.assertEqual(len(words), 5)

    def test_split_suffixes_plural(self):
        # ئۆيلەرنىڭ = ئۆي (house) + لەر (plural) + نىڭ (genitive)
        parts = split_suffixes("ئۆيلەرنىڭ")[0]
        self.assertEqual(parts[0], "ئۆي")
        self.assertIn("لەر", parts[1:])
        self.assertIn("نىڭ", parts[1:])

    def test_split_suffixes_latin(self):
        parts = split_suffixes("lärning")[0]
        self.assertTrue(parts[0].startswith("l"))

    def test_stems_dedup_direction(self):
        self.assertEqual(stems("ئۆيلەرنىڭ ئۆيى")[0], "ئۆي")

    def test_sentences(self):
        sents = split_sentences("Salam! Qanday ahwal? Yaxshi.")
        self.assertEqual(len(sents), 3)


if __name__ == "__main__":
    unittest.main()
