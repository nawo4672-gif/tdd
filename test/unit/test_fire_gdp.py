import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'data'))
import fire_gdp


class TestGetColumnIndex(unittest.TestCase):

    def test_name_present(self):
        with self.assertRaises(TypeError):
            fire_gdp.get_data()

    def test_file_found(self):
        with self.assertRaises(FileNotFoundError):
            fire_gdp.get_data("non_existent_file.csv")

    def test_returns_rows(self):
        x = fire_gdp.get_data("Agrofood_co2_emission_test.csv")
        self.assertEqual(len(x), 5)

    def test_returns_header(self):
        x = fire_gdp.get_data("Agrofood_co2_emission_test.csv", return_header=True)
        self.assertEqual(len(x), 6)
           
        

if __name__ == '__main__':
    unittest.main()
