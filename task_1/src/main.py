import click
from db_loader import DBLoader
from sql_script_executor import SQLScriptExecutor
from sql.sql_scripts import SQL_script_1, SQL_script_2, SQL_script_3, SQL_script_0

SQL_scripts = [SQL_script_0, SQL_script_1, SQL_script_2, SQL_script_3]
db_loader = DBLoader()


@click.command()
@click.option('-t', '--tables_name', type=click.Choice(['students', 'rooms']), help='name of table')
@click.option('-p', '--path', help='path of the file')
@click.option('-s', '--sql_request', type=click.Choice(['0', '1', '2', '3', ]),
              help='''choose what sql script you want to receive:
              0 - The list of rooms and the number of students in each of them;
              1 - 5 rooms with the smallest average age of students;
              2 - 5 rooms with the biggest age difference of students;
              3 - List of rooms where students of different sexes live;''')
@click.option('-f', '--file_format', type=click.Choice(['xml', 'json']), help='choose formal (xml/json)')
def work(tables_name: str, path: str, sql_request: int, file_format: str) -> None:
    """
    Perform the specified operation based on user inputs.

    Parameters:
        tables_name (str): Name of the table.
        path (str): Path of the file.
        sql_request (int): SQL script to execute.
        file_format (str): Output format (xml/json).

    Returns:
        None
    """
    if tables_name and path:
        db_loader.insert_data(path, tables_name)
    elif tables_name or path:
        click.echo("Please enter table name AND file's path ")
    elif sql_request and file_format:
        script_to_use = SQL_scripts[int(sql_request)]
        script_to_file = SQLScriptExecutor()
        script_to_file.execute_script(script_to_use, file_format)
    elif sql_request or file_format:
        click.echo("Please enter number of SQL script AND format of file")


if __name__ == "__main__":
    work()
