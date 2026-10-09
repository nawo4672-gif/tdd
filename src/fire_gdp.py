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
    if query_column is not None and query_value is not None:
        header = rows[0]
        try:
            col_index = header.index(query_column)
        except ValueError:
            raise ValueError(f"Column '{query_column}' not found in header")
        return [row for row in rows[1:] if row[col_index] == query_value]

    x = 0 if return_header else 1
    return [row for row in rows[x:]]


def get_column_index(header, column_name):
    if column_name not in header:
        raise ValueError(f"Column '{column_name}' not found in header")
    return header.index(column_name)


def get_fire_gdp_year_data(co2_file, gdp_file, country):
    co2_header = get_data(co2_file, return_header=True)[0]
    co2_rows = get_data(co2_file, query_column="Area", query_value=country)
    gdp_header = get_data(gdp_file, return_header=True)[0]
    gdp_rows = get_data(gdp_file, query_column="Country", query_value=country)

    if not gdp_rows:
        return []

    forest_fires_index = get_column_index(co2_header, "Forest fires")
    year_index = get_column_index(co2_header, "Year")
    gdp_row = gdp_rows[0]
    result = []

    for co2_row in co2_rows:
        year = co2_row[year_index]
        try:
            gdp_index = get_column_index(gdp_header, year)
        except ValueError:
            continue

        if forest_fires_index >= len(co2_row) or gdp_index >= len(gdp_row):
            continue

        forest_fires = co2_row[forest_fires_index]
        gdp = gdp_row[gdp_index]
        if forest_fires == "" or gdp == "":
            continue

        result.append([int(year), float(forest_fires), float(gdp)])

    return result

