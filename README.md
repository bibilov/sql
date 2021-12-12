# Реляционные БД

## SQLite

[SQLite](https://sqlite.org) не является клиент-серверной СУБД, она работает на уровне библиотек как файловое хранилище с реляционной БД и возможностью SQL-запросов.

В Питоне она поддерживается встреоенной библиотекой [sqlite3](https://docs.python.org/3/library/sqlite3.html).

Кроме того, доступен [клиент](https://sqlite.org/cli.html), куда можно писать SQL-запросы вне python-кода. Еще с базой можно взаимодействовать через GUI в плпгинах для современных браузерах.

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
