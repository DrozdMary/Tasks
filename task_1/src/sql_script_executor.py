import json
from db_connector import DBConnector
import mysql.connector
import xml.etree.ElementTree as ET
from logger import logger


class SQLScriptExecutor(DBConnector):

    # метод отправки запроса к бд и загрузки данных в отдельный файл разных форматов на выбор
    def execute_script(self, script, format_type):
        try:
            self.cur.execute(script)
            result_of_script = self.cur.fetchall()
            self.close_connection()
            if format_type.lower() == "json":
                converted_data = self.to_json(result_of_script)
                file = open("../created_files/result_set.json", "w+")
                json.dump(converted_data, file, indent=3)
                logger.info("Data has been stored in the 'result_set.json' file. ")
            elif format_type.lower() == "xml":
                converted_data = self.to_xml(result_of_script)
                file = open("../created_files/result_set.xml", "w+")
                file.write(converted_data)
                logger.info("Data has been stored in the 'result_set.xml' file. ")
            else:
                logger.error("Invalid format. Please use 'json' or 'xml'. ")
        except mysql.connector.Error as err:
            logger.error(f"MySQL Error: {err}")

    # метод преобразования данных в формат JSON для загрузки в файл
    def to_json(self, data):
        columns = [col[0] for col in self.cur.description]
        converted_data = []
        for item in data:
            row = dict()
            for i in range(len(columns)):
                row[columns[i]] = item[i]
            converted_data.append(row)
        return converted_data

    # метод преобразования данных в формат XML для загрузки в файл
    def to_xml(self, data):
        root = ET.Element("data")
        columns = [col[0] for col in self.cur.description]
        for row in data:
            row_element = ET.SubElement(root, "row")

            for i in range(len(columns)):
                col_element = ET.SubElement(row_element, columns[i])
                col_element.text = str(row[i])
        return ET.tostring(root, encoding="unicode")
