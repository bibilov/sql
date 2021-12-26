import sqlite3 as sql
import pandas as pd

# Задача 1
con = sql.connect('works.sqlite')
cursor = con.cursor()
cursor.execute('drop table if exists works')
cursor.execute('create table if not exists works (ID INTEGER PRIMARY KEY AUTOINCREMENT, salary INTEGER, \
    educationType TEXT, jobTitle TEXT, qualification TEXT, gender TEXT, dateModify TEXT, \
    skills TEXT, otherInfo TEXT)')
# print(cursor.execute("pragma table_info(works)").fetchall())

df = pd.read_csv('works.csv')
df.to_sql('works', con, if_exists="append", index=False)
#print(cursor.execute("select * from works limit 5").fetchall())  +++++++++++++++++++++++++

# Задача 2
# Сейчас размер файла составляет 6.3MB
cursor.execute('create index salary_index on works (salary)')
# Размер файла увеличился до 6.6MB

# Задача 3
# 32683
print(cursor.execute("select count(*) from works").fetchone()[0])

# Задача 4
# Количество мужчин
# 13386
print(cursor.execute("select count(*) from works where gender = 'Мужской'").fetchall()[0][0])
# Количество женщин
# 17910
print(cursor.execute("select count(*) from works where gender = 'Женский'").fetchall()[0][0])

# Задача 5
# У скольки записей заполнены скиллы
# 8972
print(cursor.execute('select count(*) from works where skills not null').fetchall()[0][0])

# Задача 6
# Получить заполненные скиллы
print(cursor.execute('SELECT skills FROM works where skills not null').fetchall())

# Задача 7
# Вывести зарплату только у тех, у кого в скилах есть Python
print(cursor.execute('SELECT salary FROM works where skills LIKE "%Python%"').fetchall())