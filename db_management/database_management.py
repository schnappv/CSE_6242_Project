from config import connect
import csv
import pandas as pd


def create_table(connection, database, table, fields_dict):
    """
    Creates a table in MySQL database

    Args:
        connection (mysql.connector.connect): MySQL database connection
        database (str): MySQL database connection
        table (str): Name of table
        fields_dict (dict): Dictionary of columns and types
    Raises:
        Exception: Table cannot be added
    """
    cursor = connection.cursor()
    fields = "(" + ", ".join([k + " " + fields_dict[k] for k in fields_dict]) + ")"
    print(fields)
    try:
        cursor.execute("CREATE TABLE {}.{} {}".format(database, table, fields))
        print("Successfully added the table {} to {}".format(table, database))
    except Exception as e:
        print(e)
        raise Exception("Table could not be added")


def csv_to_rows(
    csv_file, connection, database, table, fields_dict, header=True, index_col=True
):
    """
    Adds rows of a CSV into database table

    Args:
        csv_file (str): CSV file name in the data folder
        connection (mysql.connector.connect): MySQL database connection
        database (str): Name of database
        table (str): Name of table
        fields_dict (dict): Dictionary of columns and types
        header (bool, optional): If the header row is in CSV. Defaults to True.
        index_col (bool, optional): If and index column is in CSV. Defaults to True.
    """
    cursor = connection.cursor()
    keys = ", ".join([k for k in fields_dict])
    values = ", ".join([fields_dict[k] for k in fields_dict])
    q = "INSERT INTO {}.{} ({}) VALUES ({})".format(database, table, keys, values)

    data = []

    with open(csv_file, "r") as file:
        csv_reader = csv.reader(file)
        if header:
            next(csv_reader)
        for row in csv_reader:
            for i in range(len(row)):
                if row[i] == "NA":
                    row[i] = None
            r = row
            if index_col:
                r = row[1:]
            val = tuple(r)
            data.append(val)

    cursor.executemany(q, data)
    connection.commit()
    print("Complete")


def load_data(connection, database, table, q=None):
    """
    Loads the data from a database table

    Args:
        connection (mysql.connector.connect): MySQL database connection
        database (str): Name of database
        table (str): Name of table
        q (str, optional): SQL query string. Defaults to None which just selects all.

    Returns:
        pd.DataFrame: Pandas DataFrame of the queried data
    """
    cursor = connection.cursor()
    if q is None:
        q = "SELECT * FROM {}.{}".format(database, table)
    cursor.execute(q)
    field_names = [i[0] for i in cursor.description]
    table_rows = cursor.fetchall()
    df = pd.DataFrame(table_rows, columns=field_names)
    return df
