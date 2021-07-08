# -*- coding: utf-8 -*-
"""
Задание 17.3a

Создать функцию generate_topology_from_cdp, которая обрабатывает вывод
команды show cdp neighbor из нескольких файлов и записывает итоговую
топологию в один словарь.

Функция generate_topology_from_cdp должна быть создана с параметрами:
* list_of_files - список файлов из которых надо считать вывод команды sh cdp neighbor
* save_to_filename - имя файла в формате YAML, в который сохранится топология.
 * значение по умолчанию - None. По умолчанию, топология не сохраняется в файл
 * топология сохраняется только, если save_to_filename как аргумент указано имя файла

Функция должна возвращать словарь, который описывает соединения между устройствами,
независимо от того сохраняется ли топология в файл.

Структура словаря должна быть такой:
{'R4': {'Fa 0/1': {'R5': 'Fa 0/1'},
        'Fa 0/2': {'R6': 'Fa 0/0'}},
 'R5': {'Fa 0/1': {'R4': 'Fa 0/1'}},
 'R6': {'Fa 0/0': {'R4': 'Fa 0/2'}}}

Интерфейсы должны быть записаны с пробелом. То есть, так Fa 0/0, а не так Fa0/0.

Проверить работу функции generate_topology_from_cdp на списке файлов:
* sh_cdp_n_sw1.txt
* sh_cdp_n_r1.txt
* sh_cdp_n_r2.txt
* sh_cdp_n_r3.txt
* sh_cdp_n_r4.txt
* sh_cdp_n_r5.txt
* sh_cdp_n_r6.txt

Проверить работу параметра save_to_filename и записать итоговый словарь
в файл topology.yaml. Он понадобится в следующем задании.

"""
import re
import glob
import yaml


def parse_sh_cdp_neighbors(filename):
# Обработка одного файла

    result = {}
    regex = re.compile(r'(?P<r_dev>\S+) + (?P<l_intfs>\S+ \d+/\d+).+ (?P<r_intfs>\S+ \d+/\d+)')

    with open(filename, 'r') as data:

        data = data.read()
        l_dev = re.search(r'(\S+)>', data).group(1)
        result[l_dev] = {}

        for match in regex.finditer(data):
            r_dev, l_intfs, r_intfs = match.group('r_dev', 'l_intfs', 'r_intfs')
            result[l_dev][l_intfs] = {r_dev: r_intfs}

    return result


def yaml_writer(filename, data):
# Запись в файл формат yaml
    with open(filename, 'w') as file:
        yaml.dump(data, file, default_flow_style=False)

    
def generate_topology_from_cdp(list_of_files, save_to_filename = None):
# Формирование словаря топологии
    result = {}

    for file in glob.glob('sh_cdp_n_*'):
        result.update(parse_sh_cdp_neighbors(file))

    if save_to_filename is not None:
        yaml_writer(save_to_filename, result)

    return result

        
if __name__ == '__main__':
    print(generate_topology_from_cdp(glob.glob('sh_cdp_n_*'), 'out_17_3a.yaml'))
