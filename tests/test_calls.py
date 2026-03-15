import unittest
from core.actions.calls import make_call

class TestCalls(unittest.TestCase):
    def test_call(self):
        result = make_call("Mom")
        self.assertIn("Mom", result)

if __name__ == '__main__':
    unittest.main()
