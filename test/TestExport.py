import unittest
from src.taxonomy import Taxonomy


class TextExport(unittest.TestCase):
    def test_export_icb(self):
        valid_ICB = Taxonomy('10', 'ICB', '2021')
        self.assertTrue(valid_ICB.is_valid)
        print(valid_ICB.write_pp_file())

if __name__ == '__main__':
    unittest.main()