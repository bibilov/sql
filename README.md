# Реляционные БД

## SQLite

[SQLite](https://sqlite.org) не является клиент-серверной СУБД, она работает на уровне библиотек как файловое хранилище с реляционной БД и возможностью SQL-запросов.

В Питоне она поддерживается встроенной библиотекой [sqlite3](https://docs.python.org/3/library/sqlite3.html).

Кроме того, доступен [клиент](https://sqlite.org/cli.html), куда можно писать SQL-запросы вне python-кода. Еще с базой можно взаимодействовать через GUI в плагинах для современных браузерах.

```
bibilov@osgiliath:~/dz-sql$ sqlite3 my.db
SQLite version 3.22.0 2018-01-22 18:45:57
Enter ".help" for usage hints.
sqlite> .exit
```

Отметим, что у каждой СУБД синтаксис особенно в части команд управления может отличаться, в частности, в sqlite3 команды начинаются с `.`. Например, `.exit`. 

Все база данных представляет один файл, что может быть удобно в некоторых случаях. Например, мобильное приложение может хранить большое количество информации в локальной БД, не имея сложной клиент-серверной архитектуры внутри себя. Вы можете поискать sqlite-базы в своем телефоне.

Так как CSV &mdash; это по сути таблица, то предусмотрен легкий импорт из CSV:

```
bibilov@osgiliath:~/dz-sql$ sqlite3 works.sqlite
SQLite version 3.22.0 2018-01-22 18:45:57
Enter ".help" for usage hints.
sqlite> .mode csv
sqlite> .import works.csv works
```

Файлы, как мы видим, почти не отличаются по размерам.

```
bibilov@osgiliath:~/dz-sql$ ls -ls
total 12148
5744 -rw-rw-r-- 1 bibilov bibilov 5880909 Dec 12 15:32 works.csv
6404 -rw-r--r-- 1 bibilov bibilov 6557696 Dec 12 15:33 works.sqlite
```

Импорт по умолчанию не отличается тонким анализом типов полей, а также добавлением первичных ключей и индексов:

```
sqlite> .schema works
CREATE TABLE works(
  "salary" TEXT,
  "educationType" TEXT,
  "jobTitle" TEXT,
  "qualification" TEXT,
  "gender" TEXT,
  "dateModify" TEXT,
  "skills" TEXT,
  "otherInfo" TEXT
);

```

Количество строк в таблице:

```
sqlite> select count(*) from works;
32683
```

Можно включить замеры времени в запросах:

```
sqlite> .timer ON
sqlite> select count(*) from works;
32683
Run Time: real 0.003 user 0.000000 sys 0.002572
```

## Работа из Python

```python
import sqlite3 


con = sqlite3.connect('works.sqlite')
res = con.execute('select count(*) from works;') # Вернется итератор.
list(res)
```

```
[(32683,)]
```

Корсор или соединение, как правило, возвращают просто кортежи:

```python
res = con.execute('select * from works limit 3')

for r in res:
    print(r)
```

```
('60000', 'Высшее', 'Специалист пресс-службы', 'Магистр', 'Мужской', '2021-04-01', '<p>Аналитическое&nbsp;мышление,&nbsp;<span class="s6"><span class="bumpedFont15">ответственность, </span></span><span class="s6"><span class="bumpedFont15">стабильность психологического состояния и настроения.&nbsp;</span></span></p>', '')
('85000', 'Высшее', 'менеджер проектов', '', 'Мужской', '2021-04-01', '', '')
('15000', 'Среднее профессиональное', '....', '', 'Женский', '2021-06-01', '', '')
```

Это иногда бывает неудобно. Можно сделать обертку для получения словарей.

```python
from pprint import pprint

def dict_factory(cursor, row): 
    # обертка для преобразования 
    # полученной строки. (взята из документации)
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


con.row_factory = dict_factory

res = con.execute('select * from works limit 3')

pprint(list(res))
```

```python
[{'dateModify': '2021-04-01',
  'educationType': 'Высшее',
  'gender': 'Мужской',
  'jobTitle': 'Специалист пресс-службы',
  'otherInfo': '',
  'qualification': 'Магистр',
  'salary': '60000',
  'skills': '<p>Аналитическое&nbsp;мышление,&nbsp;<span class="s6"><span '
            'class="bumpedFont15">ответственность, </span></span><span '
            'class="s6"><span class="bumpedFont15">стабильность '
            'психологического состояния и настроения.&nbsp;</span></span></p>'},
 {'dateModify': '2021-04-01',
  'educationType': 'Высшее',
  'gender': 'Мужской',
  'jobTitle': 'менеджер проектов',
  'otherInfo': '',
  'qualification': '',
  'salary': '85000',
  'skills': ''},
 {'dateModify': '2021-06-01',
  'educationType': 'Среднее профессиональное',
  'gender': 'Женский',
  'jobTitle': '....',
  'otherInfo': '',
  'qualification': '',
  'salary': '15000',
  'skills': ''}]
```

### Задания

Повторим pandas-исследования. По возможности всю предобработку данных доверьте SQL. 

В скрипте на Питоне:

1. Создайте и заполните таблицу запросами, создайте техническое поле `ID` c параметрами `INTEGER PRIMARY KEY AUTOINCREMENT`.
2. Добавьте индекс на поле `salary`. Изменится ли после этого размер файла? На сколько?
3. Выведите количество записей.
4. Выведите количество мужчин и женщин.
5. У скольки записей заполены skills?
6. Получить заполненные скиллы.
7. Вывести зарплату только у тех, у кого в скилах есть Python.
8. Построить перцентили и разброс по з/п у мужчин и женщин.
9. Построить графики распределения по з/п мужчин и женщин (а также в зависимости от высшего образования).

## ДЗ

### Пробуем нормализовать базу данных и немного почистить поля.

Выделим отдельные сущности:

* Создайте отдельную таблицу с гендером, заполните ее значениями, сделайте на нее внешний ключ из таблицы `works`.
* Отдельная таблица для образования.
* Отдельная таблица для `jobTitle`. Попытайтесь свести все разнообразие к небольшому количеству должностей.
* Отдельная таблица для `qualification`. Попытайтесь свести все разнообразие к небольшому количеству специальностей.

### Скилы и `otherInfo`

Эти поля крайне засорены HTML-разметкой. Например, самое длинное описание скилов занимает 11Кб.

```
<span class="bloko-tag bloko-tag_inline bloko-tag_countable Bloko-TagList-Tag" data-tag-id="1518" data-qa="bloko-tag_inline"><span class="bloko-tag__layout-slim"><span class="bloko-tag__section bloko-tag__section_stretched" title="Активные продажи"><span class="bloko-tag__section-text Bloko-TagList-Text" data-qa="bloko-tag__text">Активные продажи</span>
```

* Очистите эти поля от HTML.
* Отдельная таблица для скилов. Попытайтесь свести все разнообразие к небольшому количеству.
* Отдельная таблица личных качеств на основе `otherInfo`. Попытайтесь свести все разнообразие к небольшому количеству прилагательных (используйте библиотеки для NLP): 
   * коммуникабелен, 
   * целеустремлен,
   * трудоголик,
   * ...
