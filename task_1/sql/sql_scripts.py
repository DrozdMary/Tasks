create_table_rooms = "create table  if not exists rooms ( id int not null, name varchar(50), primary key(id) )"
create_table_students = "create table  if not exists students( birthday datetime, id int primary key, name char(100), room int, sex char(1))"
create_idx_rooms_id = 'create index idx_rooms_id on rooms (id)'
create_idx_students_room = 'create index idx_students_room on students(room)'

SQL_script_0 = '''select
rooms.id, rooms.name as room_name,
count(students.id) as students_in_room
from rooms
left join students
on rooms.id = students.room
group by rooms.id, rooms.name'''

SQL_script_1 = '''select
rooms.id,rooms.name as room_name,
cast(avg((year(current_date) - year(students.birthday))) as signed) as avg_students_age
from students
right join rooms on students.room=rooms.id
group by rooms.name
order by avg_students_age
limit 5'''

SQL_script_2 = '''select
rooms.id,rooms.name as room_name,
(max(year(current_date) - year(students.birthday))-min(year(current_date) - year(students.birthday))) as diff_of_age
from rooms
left join students on rooms.id = students.room
group by rooms.name
order by diff_of_age desc
limit 5
'''
SQL_script_3 = '''select rooms.id, rooms.name as room_name
from rooms
left join students on rooms.id = students.room
group by rooms.id, rooms.name
having count(distinct students.sex) > 1; '''