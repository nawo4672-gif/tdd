import os

def get_data(file_name,
             query_column=None,
             query_value=None,
             return_header=False):
    if file_name not in os.listdir("data"):
        raise FileNotFoundError(f"File '{file_name}' not found in data.")

def get_column_index(header, column_name):
    pass


def get_fire_gdp_year_data(co2_file, gdp_file, country):
    pass

