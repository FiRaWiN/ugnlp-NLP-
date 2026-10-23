import unittest

from ugnlp.translit import is_arabic_script, to_arabic, to_latin


class TestTranslit(unittest.TestCase):
    def test_basic_consonants_roundtrip(self):
        s = "salam dostum"
        ar = to_arabic(s)
        self.assertTrue(is_arabic_script(ar))
        self.assertEqual(to_latin(ar), s)

    def test_clusters(self):
        self.assertEqual(to_latin(to_arabic("shunchak")), "shunchak")
        self.assertEqual(to_latin(to_arabic("gher")), "gher")

    def test_word_initial_vowel_hamza(self):
        ar = to_arabic("oy")
        self.assertTrue(ar.startswith("ئ"))  # UEY marks initial vowels with hamza
        self.assertEqual(to_latin(ar), "oy")

    def test_mixed_text_preserved(self):
        ar = to_arabic("2026-yil")
        self.assertIn("2026", ar)  # digits untouched

    def test_arabic_to_latin_hamza_vowel(self):
        self.assertEqual(to_latin("ئىككى"), "ikki")
        self.assertEqual(to_latin("ئۈچ"), "üch")


if __name__ == "__main__":
    unittest.main()
