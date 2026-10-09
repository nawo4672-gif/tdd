import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
import fire_gdp


class TestGetColumnIndex(unittest.TestCase):

    def test_name_present(self):
        with self.assertRaises(TypeError):
            fire_gdp.get_data()

if __name__ == '__main__':
    unittest.main()
