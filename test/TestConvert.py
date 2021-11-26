import unittest
from src.taxonomy import Taxonomy
from src.convert import Convert

class TestConvert(unittest.TestCase):
    def test_convert_first_level(self):
        valid_GICS = Taxonomy('10','GICS','2018')

        valid_ICB = Convert.gcis_to_icb(valid_GICS)
        self.assertIsNotNone(valid_ICB)
        self.assertTrue(valid_GICS.is_valid)
        self.assertIs(valid_ICB["code"], "60")
        self.assertIs(valid_ICB["name"], "Energy")

if __name__ == '__main__':
    unittest.main()
