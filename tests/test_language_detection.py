import unittest
from core.nlu.language_detector import detect_language

class TestLanguageDetection(unittest.TestCase):
    def test_detect(self):
        self.assertEqual(detect_language("hello"), "en_ZA")

if __name__ == '__main__':
    unittest.main()
