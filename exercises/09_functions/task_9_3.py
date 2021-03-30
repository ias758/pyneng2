# -*- coding: utf-8 -*-
"""
Задание 9.3

Создать функцию get_int_vlan_map, которая обрабатывает конфигурационный
файл коммутатора и возвращает кортеж из двух словарей:
* словарь портов в режиме access, где ключи номера портов,
  а значения access VLAN (числа):
{'FastEthernet0/12': 10,
 'FastEthernet0/14': 11,
 'FastEthernet0/16': 17}

* словарь портов в режиме trunk, где ключи номера портов,
  а значения список разрешенных VLAN (список чисел):
{'FastEthernet0/1': [10, 20],
 'FastEthernet0/2': [11, 30],
 'FastEthernet0/4': [17]}

У функции должен быть один параметр config_filename, который ожидает как аргумент
имя конфигурационного файла.

Проверить работу функции на примере файла config_sw1.txt

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""
def get_int_vlan_map(config_filename):
    port_access = {}
    port_trunk = {}
    with open(config_filename) as file:
        for line in file:
            line.strip()
            if line.startswith('interface'):
                intfs = line.split()[1]
            elif 'access vlan' in line:
                port_access[intfs] = int(line.split()[-1])
            elif 'allowed vlan' in line:
                port_trunk[intfs] = [int(i) for i in line.rsplit()[-1].split(',')]
    return port_access, port_trunk    
print(get_int_vlan_map('config_sw1.txt'))
