# -*- coding: utf-8 -*-
"""
Задание 7.2a

Сделать копию скрипта задания 7.2.

Дополнить скрипт: Скрипт не должен выводить на стандартрый поток вывода команды,
в которых содержатся слова из списка ignore.

При этом скрипт также не должен выводить строки, которые начинаются на !.

Проверить работу скрипта на конфигурационном файле config_sw1.txt.
Имя файла передается как аргумент скрипту.

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""
from sys import argv
ignore = ["duplex", "alias", "configuration"]
i = True
with open (argv[1]) as config:
    for line in config:
        if line.startswith('!'):
            continue
        else:
            for word in line.split():
                if word in ignore:
                    i = False
                    break
                else:
                    i = True
            if i is True:
                print(line.strip())
