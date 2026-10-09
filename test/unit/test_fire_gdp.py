import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
import fire_gdp


class TestGetColumnIndex(unittest.TestCase):

    def test_name_present(self):
        with self.assertRaises(TypeError):
            fire_gdp.get_data()

    def test_file_found(self):
        with self.assertRaises(FileNotFoundError):
            fire_gdp.get_data("non_existent_file.csv")

if __name__ == '__main__':
    unittest.main()
