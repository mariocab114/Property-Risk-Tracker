import unittest
from models import Property

class TestProperty(unittest.TestCase):

    def test_property_creation(self):
        p = Property("Warehouse A", "Chicago", 450000, "Fire", 7)
        self.assertEqual(p.name, "Warehouse A")
        self.assertEqual(p.value, 450000)
        self.assertEqual(p.risk_score, 7)

    def test_property_string_format(self):
        p = Property("Office B", "Boston", 200000, "Flood", 5)
        result = str(p)
        self.assertIn("Office B", result)
        self.assertIn("Flood", result)

if __name__ == "__main__":
    unittest.main()