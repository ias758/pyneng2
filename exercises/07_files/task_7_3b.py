# -*- coding: utf-8 -*-
"""
Задание 7.3b

Сделать копию скрипта задания 7.3a.

Переделать скрипт:
- Запросить у пользователя ввод номера VLAN.
- Выводить информацию только по указанному VLAN.

Пример работы скрипта:

Enter VLAN number: 10
10       0a1b.1c80.7000      Gi0/4
10       01ab.c5d0.70d0      Gi0/8

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""
vl = input('Введите влан:')
a = []
out = '{:8} {:15} {:>8}'
with open ('CAM_table.txt') as table:
    for line in table:
        line = line.lstrip()
        if line != '' and line[0].isdigit():
            a.append([j for j in line.strip().split()])
            a.sort()
        else: continue
    for vlan,mac,_,port in a:
        if vlan == vl:
            print (out.format(vlan,mac,port))
