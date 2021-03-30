# -*- coding: utf-8 -*-
"""
Задание 9.3a

Сделать копию функции get_int_vlan_map из задания 9.3.

Дополнить функцию: добавить поддержку конфигурации, когда настройка access-порта
выглядит так:
    interface FastEthernet0/20
        switchport mode access
        duplex auto

То есть, порт находится в VLAN 1

В таком случае, в словарь портов должна добавляться информация, что порт в VLAN 1
Пример словаря:
    {'FastEthernet0/12': 10,
     'FastEthernet0/14': 11,
     'FastEthernet0/20': 1 }

У функции должен быть один параметр config_filename, который ожидает
как аргумент имя конфигурационного файла.

Проверить работу функции на примере файла config_sw2.txt

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""
def get_int_vlan_map(config_filename):
    port_access = {}
    port_trunk = {}
    with open(config_filename) as file:
        for line in file:
            line.strip()
            if line.startswith('interface') and 'interface Vlan' not in line:
                intfs = line.split()[1]
                port_access.setdefault(intfs,1)
            elif 'access vlan' in line:
                port_access[intfs] = int(line.split()[-1])
            elif 'allowed vlan' in line:
                port_trunk[intfs] = [int(i) for i in line.rsplit()[-1].split(',')]
    for keys in list(port_access.keys()):
        if keys in list(port_trunk.keys()):
            port_access.pop(keys)
    return port_access, port_trunk    
print(get_int_vlan_map('config_sw2.txt'))
