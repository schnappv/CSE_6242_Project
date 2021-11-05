from os import readlink
from src.database_management import create_table
from config import connect
import csv


def create_table(connection, database, table, fields_dict):
    """
    Creates a table in MySQL database

    Args:
        connection ([type]): [description]
        database ([type]): [description]
        table ([type]): [description]
        fields_dict ([type]): [description]

    Raises:
        Exception: [description]
    """
    cursor = connection.cursor()
    fields = "(" + ", ".join([k + ' ' + fields_dict[k]
                              for k in fields_dict]) + ")"
    print(fields)
    try:
        cursor.execute("CREATE TABLE {}.{} {}".format(database, table, fields))
        print("Successfully added the table {} to {}".format(table, database))
    except:
        raise Exception("Table could not be added")


def csv_to_rows(csv_file, connection, database, table, fields_dict, header=True, index_col=True):
    """
    Adds rows of a CSV into database table

    Args:
        csv_file ([type]): [description]
        connection ([type]): [description]
        database ([type]): [description]
        table ([type]): [description]
        fields_dict ([type]): [description]
        header (bool, optional): [description]. Defaults to True.
        index_col (bool, optional): [description]. Defaults to True.
    """
    cursor = connection.cursor()
    keys = ", ".join([k for k in fields_dict])
    values = ", ".join([fields_dict[k] for k in fields_dict])
    q = "INSERT INTO {}.{} ({}) VALUES ({})".format(
        database, table, keys, values)

    with open(csv_file, 'r') as file:
        csv_reader = csv.reader(file)
        if header:
            next(csv_reader)
        for row in csv_reader:
            r = row
            if index_col:
                r = row[1:]
            val = tuple(r)
            cursor.execute(q, val)
            connection.commit()
        print("Complete")

# "INSERT INTO AQI.combined (Year, State, Parameter, AQI, Age_Group, Population, CP_deaths, Total_deaths, Pct_CP_Death) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
