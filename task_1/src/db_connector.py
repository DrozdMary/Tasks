import mysql.connector
from config import host, user, password, db_name, port
from logger import logger


class DBConnector:
    def __init__(self):
        # подключение к созданной базе данных и создание таблиц
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

    # метод создание таблиц в базе данных
    def create_tables(self):
        try:
            self.cur.execute(
                "create table  IF NOT EXISTS rooms ( id int NOT NULL, name varchar(50), primary key(id) )"
            )
            self.cur.execute(
                "create table  IF NOT EXISTS students( birthday datetime, id int primary key, name char(100), room int, "
                "sex CHAR(1))"
            )
            logger.info("Tables are created")
            self.connection.commit()
        except Exception as ex:
            logger.error(f"Unexpected error with creating tables : {ex}")

    # метод для прерывания подключения к базе данных
    def close_connection(self):
        if self.connection.is_connected():
            self.cur.close()
            self.connection.close()
            logger.info("Connection closed")
