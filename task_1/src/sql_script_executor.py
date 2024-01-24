import json
import mysql.connector
import xml.etree.ElementTree as ET
from db_connector import DBConnector
from logger import logger


class SQLScriptExecutor(DBConnector):
    """
     A class to execute SQL scripts and store the result in the specified format.
    """

    def execute_script(self, script: str, format_type: str) -> None:
        """
        Execute the provided SQL script and store the result in the specified format.

        Parameters:
            script (str): SQL script to execute.
            format_type (str): Format in which to store the result ("json" or "xml").
        """
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

    def to_json(self, data: list[dict]) -> list[dict]:
        """
        Convert the result set to a JSON format.

        Parameters:
            data (list[dict]): Result set to convert.

        Returns:
            list[dict]: Converted data in JSON format.
        """
        columns = [col[0] for col in self.cur.description]
        converted_data = [{columns[i]: item[i] for i in range(len(columns))} for item in data]
        return converted_data

    def to_xml(self, data: list[dict]) -> str:
        """
        Convert the result set to an XML format.

        Parameters:
            data (list[dict]): Result set to convert.

        Returns:
            str: Converted data in XML format.
        """
        root = ET.Element("data")
        columns = [col[0] for col in self.cur.description]
        for row in data:
            row_element = ET.SubElement(root, "row")
            for i in range(len(columns)):
                col_element = ET.SubElement(row_element, columns[i])
                col_element.text = str(row[i])
        return ET.tostring(root, encoding="unicode")
