import unittest
from core.personality.jealousy_tracker import JealousyTracker

class TestJealousy(unittest.TestCase):
    def test_escalation(self):
        t = JealousyTracker()
        self.assertEqual(t.update("siri"), 1)
        self.assertEqual(t.update("siri"), 2)
        self.assertEqual(t.update("siri"), 3)
        self.assertEqual(t.update("alexa"), 1)

if __name__ == '__main__':
    unittest.main()
