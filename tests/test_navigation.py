import unittest
from core.actions.navigation import navigate

class TestNavigation(unittest.TestCase):
    def test_navigate(self):
        result = navigate("Cape Town")
        self.assertIn("Cape Town", result)

if __name__ == '__main__':
    unittest.main()
