import mysql.connector
import json
from db_connector import DBConnector
from logger import logger
from sql.sql_scripts import create_idx_rooms_id,create_idx_students_room


class DBLoader(DBConnector):
    """
    A class for loading data into the database.
    """

    @staticmethod
    def read_json(path_json_file: str) -> list[dict]:
        """
        Reads data from a JSON file.

        Parameters:
            path_json_file (str): The path to the JSON file.

        Returns:
            list[dict]: A list of dictionaries containing the data.
        """
        with open(path_json_file, "r") as js_file:
            data_from_json_file = json.load(js_file)
            return data_from_json_file

    def insert_data(self, path_json_file: str, table_name: str) -> None:
        """
        Inserts data into the specified database table.

        Parameters:
            path_json_file (str): The path to the JSON file with data.
            table_name (str): The name of the table in database.

        Returns:
            None
        """
        data = self.read_json(path_json_file)
        first_item = data[0]
        columns = list(first_item.keys())
        logger.info(
            f"Inserting data into table '{table_name}' with columns: {columns}"
        )
        placeholders = ", ".join(["%s"] * len(columns))
        try:
            for items in data:
                values = [items[column] for column in columns]
                sql = f"insert into {table_name} ({', '.join(columns)}) values ({placeholders})"
                self.cur.execute(sql, values)
                self.connection.commit()
            logger.info(f"Inserted data into {table_name} successfully.")
            self.add_index()
            self.close_connection()
        except mysql.connector.Error as err:
            logger.error(f"MySQL Error: {err}")

    def add_index(self) -> None:
        """
        Adds indexes to the database tables.

        Returns:
            None
        """
        try:
            self.cur.execute(create_idx_rooms_id)
            self.cur.execute(create_idx_students_room)
            logger.info("Indexes are created")
            self.connection.commit()
        except Exception as ex:
            logger.error(f"Unexpected error with creating indexes : {ex}")
