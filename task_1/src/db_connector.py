import mysql.connector
from config import host, user, password, db_name, port
from logger import logger
from sql.sql_scripts import create_table_rooms,create_table_students


class DBConnector:
    """
    Connects to the MySQL database and creates tables if they do not exist
    """

    def __init__(self):
        """
        Initializes a new instance of the DBConnector class.
        """
        try:
            self.connection = mysql.connector.connect(
                host=host, user=user, password=password, database=db_name, port=port
            )
            if self.connection.is_connected():
                logger.info("Connected to MySQL database")
            self.cur = self.connection.cursor()
            self.create_tables()
        except mysql.connector.Error as err:
            logger.error(f"MySQL Connection Error: {err}")
        except Exception as ex:
            logger.error(f"Unexpected error with MySQL connection : {ex}")

    def create_tables(self) -> None:
        """
        Creates tables 'rooms' and 'students' if they do not exist.

        Returns:
            None
        """
        try:
            self.cur.execute(create_table_rooms)
            self.cur.execute(create_table_students)
            logger.info("Tables are created")
            self.connection.commit()
        except Exception as ex:
            logger.error(f"Unexpected error with creating tables : {ex}")

    def close_connection(self) -> None:
        """
        Closes the connection to the MySQL database

        Returns:
            None
        """
        if self.connection.is_connected():
            self.cur.close()
            self.connection.close()
            logger.info("Connection closed")
