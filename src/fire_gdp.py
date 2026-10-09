import os
import csv


def get_data(file_name,
             query_column=None,
             query_value=None,
             return_header=False):
    if file_name is None:
        raise ValueError("file_name cannot be None")

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    candidate_paths = [
        file_name,
        os.path.join(project_root, file_name),
        os.path.join(project_root, 'data', file_name),
        os.path.join(project_root, 'test', file_name),
        os.path.join(project_root, 'test', 'unit', file_name),
    ]

    file_path = None
    for candidate in candidate_paths:
        if os.path.exists(candidate):
            file_path = candidate
            break

    if file_path is None:
        raise FileNotFoundError(f"File '{file_name}' not found")

    with open(file_path, newline="", encoding="utf-8") as f:
        rows = [row for row in csv.reader(f) if row]
    x=1
    if return_header:
        x=0

    return [
        
        row for row in rows[x:]
    ]


def get_column_index(header, column_name):
    pass


def get_fire_gdp_year_data(co2_file, gdp_file, country):
    pass
