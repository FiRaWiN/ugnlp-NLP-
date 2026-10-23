import unittest

from ugnlp.glossary import Glossary
from ugnlp.numbers import convert_digits, extract_numbers, ug_number_to_int


class TestGlossary(unittest.TestCase):
    def setUp(self):
        self.g = Glossary()

    def test_lookup_zh(self):
        hit = self.g.lookup("洗发水")
        self.assertEqual(hit["en"], "shampoo")
        self.assertTrue(hit["ug"])

    def test_lookup_ug(self):
        hit = self.g.lookup("چاچ سوپۇنى")
        self.assertEqual(hit["zh"], "洗发水")

    def test_fuzzy_search(self):
        results = self.g.search("洗发")
        self.assertTrue(results)
        self.assertTrue(
            results[0][0]["zh"].startswith("洗发") or results[0][1] > 0.5
        )


class TestNumbers(unittest.TestCase):
    def test_digits_ascii(self):
        self.assertEqual(convert_digits("٣ دانە ۵ yüan", to="ascii"), "3 دانە 5 yüan")

    def test_digits_arabic(self):
        self.assertEqual(convert_digits("45", to="arabic"), "٤٥")

    def test_number_words(self):
        self.assertEqual(ug_number_to_int("بەش"), 5)
        self.assertEqual(ug_number_to_int("besh"), 5)

    def test_extract_numbers(self):
        # order of extraction (digits vs words) is implementation-defined;
        # sort for a stable assertion
        self.assertEqual(sorted(extract_numbers("بەش يۈئەن ، ٣ خالتە")), [3, 5])


if __name__ == "__main__":
    unittest.main()
