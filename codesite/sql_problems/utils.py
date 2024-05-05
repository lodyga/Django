import pandas as pd

ascii_object_table = """
| personId | lastName | firstName |
| -------- | -------- | --------- |
| 1        | Wang     | Allen     |
| 2        | Alice    | Bob       |
"""

ascii_type_table = """
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| personId    | int     |
| lastName    | varchar |
| firstName   | varchar |
+-------------+---------+
"""


# Convert ASCII-like table to list of dicts


def ascii_table_to_dict(ascii_object_table):
    """
    object_table = [
        {'personId': '1', 'lastName': 'Wang', 'firstName': 'Allen'},
        {'personId': '2', 'lastName': 'Alice', 'firstName': 'Bob'}
    ]
    """
    lines = ascii_object_table.strip().split('\n')
    if lines[0][0] == "|":
        first_line = 0
    else:
        first_line = 1

    headers = [header.strip()
               for header in lines[first_line].split('|') if header.strip()]
    data = []

    for line in lines[first_line + 2:]:
        if line[0] == "|":
            values = [value.strip()
                      for value in line.split('|') if value.strip()]
            row = dict(zip(headers, values))
            # row = {headers[i]: int(values[i]) if values[i].isdigit() else values[i] for i in range(len(headers))}

            data.append(row)

    return data


object_table = ascii_table_to_dict(ascii_object_table)


# Convert ASCII-like type table to dict
def ascii_type_to_dict(ascii_type_table):
    """
    {'personId': 'int', 'lastName': 'str', 'firstName': 'str'}
    """
    type_convert = {"int": "int", "varchar": "str"}
    lines = ascii_type_table.strip().split("\n")
    type_dict = {}
    for line in lines:
        if "|" in line:
            values = [value.strip()
                      for value in line.split("|") if value.strip()]
            if values[0] != "Column Name":
                type_dict[values[0]] = type_convert[values[1]]
    return type_dict


ascii_type_to_dict(ascii_type_table)


# apply dtypes to an object_table
def change_dtype(object_table, type_table):
    """
       personId lastName firstName
    0         1     Wang     Allen
    1         2    Alice       Bob
    """
    for column, dtype in type_table.items():
        object_table[column] = object_table[column].astype(dtype)
    return object_table


change_dtype(pd.DataFrame(ascii_table_to_dict(ascii_object_table)),
             ascii_type_to_dict(ascii_type_table))
