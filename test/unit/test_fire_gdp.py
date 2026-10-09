import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'data'))
import fire_gdp  # noqa: E402


class TestGetData(unittest.TestCase):

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
        x = fire_gdp.get_data(
            "Agrofood_co2_emission_test.csv", return_header=True
        )
        self.assertEqual(len(x), 6)

    def test_returns_rows_with_query(self):
        x = fire_gdp.get_data(
            "Agrofood_co2_emission_test.csv",
            query_column="Year",
            query_value="1990",
        )
        self.assertEqual(len(x), 1)
        self.assertEqual(x[0][1], "1990")


class TestGetColumnIndex(unittest.TestCase):

    def test_column_found(self):
        header = fire_gdp.get_data(
            "Agrofood_co2_emission_test.csv", return_header=True
        )[0]
        index = fire_gdp.get_column_index(header, "Year")
        self.assertEqual(index, 1)

    def test_column_not_found(self):
        with self.assertRaises(ValueError):
            fire_gdp.get_column_index(
                fire_gdp.get_data(
                    "Agrofood_co2_emission_test.csv", return_header=True
                )[0],
                "NonExistentColumn",
            )

    def test_no_header(self):
        with self.assertRaises(ValueError):
            fire_gdp.get_column_index([], "Year")


class TestGetFireGdpYearData(unittest.TestCase):

    def test_function_exists(self):
        self.assertTrue(callable(fire_gdp.get_fire_gdp_year_data))

    def test_returns_matching_years_as_numeric_rows(self):
        rows = fire_gdp.get_fire_gdp_year_data(
            "Agrofood_co2_emission.csv", "IMF_GDP_test.csv", "Afghanistan"
        )

        self.assertEqual(rows[0], [2002, 0.0, 178756.0])
        self.assertTrue(all(type(row[0]) is int for row in rows))
        self.assertTrue(all(type(row[1]) is float for row in rows))
        self.assertTrue(all(type(row[2]) is float for row in rows))


if __name__ == '__main__':
    unittest.main()
