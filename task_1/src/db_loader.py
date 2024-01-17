from db_connector import DBConnector
import mysql.connector
import json
from logger import logger


class DBLoader(DBConnector):

    # статический метод для изъятия данных из json файлов (возвращает список словарей с данными)
    @staticmethod
    def read_json(path_json_file):
        with open(path_json_file, "r") as js_file:
            data_from_json_file = json.load(js_file)
            return data_from_json_file

    def insert_data(self, path_json_file, table_name):
        data = self.read_json(path_json_file)
        # получение списка атрибутов заполняемой таблицы
        first_item = data[0]
        columns = list(first_item.keys())
        logger.info(
            f"Inserting data into table '{table_name}' with columns: {columns}"
        )
        # форма для вставления значений в SQL запрос
        placeholders = ", ".join(["%s"] * len(columns))
        # последовательное добавления каждой записи в таблицу
        try:
            for items in data:
                values = [items[column] for column in columns]
                sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
                self.cur.execute(sql, values)
                self.connection.commit()
            logger.info(f"Inserted data into {table_name} successfully.")
            self.add_index()
            self.close_connection()
        except mysql.connector.Error as err:
            logger.error(f"MySQL Error: {err}")

    # добавление индексов
    def add_index(self):
        try:
            self.cur.execute('CREATE INDEX idx_rooms_id ON rooms (id)')
            self.cur.execute('CREATE INDEX idx_students_room ON students(room)')
            logger.info("Indexes are created")
            self.connection.commit()
        except Exception as ex:
            logger.error(f"Unexpected error with creating indexes : {ex}")
