import unittest
from core.actions.weather import get_weather

class TestWeather(unittest.TestCase):
    def test_weather(self):
        result = get_weather("Johannesburg")
        self.assertIsInstance(result, str)

if __name__ == '__main__':
    unittest.main()
