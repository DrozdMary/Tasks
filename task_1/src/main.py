import click
from db_loader import DBLoader
from sql_script_executor import SQLScriptExecutor

# Список комнат и количество студентов в каждой из них
SQL_script_0 = """select
    rooms.id,
rooms.name as room_name,
count(students.id) as students_in_room
from rooms
left join students
on rooms.id = students.room
group by rooms.id, rooms.name"""

# 5 комнат, где самый маленький средний возраст студентов
SQL_script_1 = """SELECT
    rooms.id,
rooms.name as room_name,
    CAST(avg((YEAR(CURRENT_DATE) - YEAR(students.birthday))) AS SIGNED) AS avg_students_age
FROM students
right join rooms on students.room=rooms.id
group by rooms.name
order by avg_students_age
limit 5
"""

# 5 комнат с самой большой разницей в возрасте студентов
SQL_script_2 = """SELECT
    rooms.id,
 rooms.name AS room_name,
 (max(YEAR(CURRENT_DATE) - YEAR(students.birthday))-min(YEAR(CURRENT_DATE) - YEAR(students.birthday))) AS diff_of_age
from rooms
left join students on rooms.id = students.room
group by rooms.name
order by diff_of_age desc
limit 5
"""

# Список комнат где живут разнополые студенты
SQL_script_3 = """SELECT rooms.id, rooms.name AS room_name
FROM rooms
left JOIN students ON rooms.id = students.room
GROUP BY rooms.id, rooms.name
HAVING COUNT(DISTINCT students.sex) > 1;
"""
SQL_scripts = [SQL_script_0, SQL_script_1, SQL_script_2, SQL_script_3]


@click.command()
@click.option('-t', '--tables_name', type=click.Choice(['students', 'rooms']), help='name of table')
@click.option('-s', '--sql_request', type=click.Choice(['0', '1', '2', '3', ]),
              help='''choose what sql script you want to receive:
              0 - The list of rooms and the number of students in each of them;
              1 - 5 rooms with the smallest average age of students;
              2 - 5 rooms with the biggest age difference of students;
              3 - List of rooms where students of different sexes live;''')
@click.option('-f', '--file_format', type=click.Choice(['xml', 'json']), help='choose formal (xml/json)')
def work(tables_name, sql_request, file_format):
    db_loader = DBLoader()
    if tables_name == 'students' or tables_name == 'rooms':
        print('ok')
        db_loader.insert_data(f'../files/{tables_name}.json')

    if sql_request and file_format:
        print(SQL_scripts[int(sql_request)])
        script_to_use = SQL_scripts[int(sql_request)]
        script_to_file = SQLScriptExecutor()
        script_to_file.execute_script(script_to_use, file_format)


if __name__ == "__main__":
    work()

