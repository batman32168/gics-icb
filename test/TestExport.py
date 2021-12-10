import unittest
from src.taxonomy import Taxonomy


class TextExport(unittest.TestCase):
    def test_export_icb(self):
        valid_ICB = Taxonomy('10', 'ICB', '2021')
        self.assertTrue(valid_ICB.is_valid)
        f =open('icb.text','w')
        f.write(valid_ICB.write_pp_file())

    def test_export_gics(self):
        valid = Taxonomy('10', 'GICS', '2018')
        self.assertTrue(valid.is_valid)
        f = open('gics.text', 'w')
        f.write(valid.write_pp_file())

if __name__ == '__main__':
    unittest.main()