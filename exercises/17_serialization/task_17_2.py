# -*- coding: utf-8 -*-
"""
Задание 17.2

В этом задании нужно:
* взять содержимое нескольких файлов с выводом команды sh version
* распарсить вывод команды с помощью регулярных выражений
  и получить информацию об устройстве
* записать полученную информацию в файл в CSV формате

Для выполнения задания нужно создать две функции.

Функция parse_sh_version:
* ожидает как аргумент вывод команды sh version одной строкой (не имя файла)
* обрабатывает вывод, с помощью регулярных выражений
* возвращает кортеж из трёх элементов:
 * ios - в формате "12.4(5)T"
 * image - в формате "flash:c2800-advipservicesk9-mz.124-5.T.bin"
 * uptime - в формате "5 days, 3 hours, 3 minutes"

У функции write_inventory_to_csv должно быть два параметра:
 * data_filenames - ожидает как аргумент список имен файлов с выводом sh version
 * csv_filename - ожидает как аргумент имя файла (например, routers_inventory.csv),
   в который будет записана информация в формате CSV
* функция записывает содержимое в файл, в формате CSV и ничего не возвращает


Функция write_inventory_to_csv должна делать следующее:
* обработать информацию из каждого файла с выводом sh version:
 * sh_version_r1.txt, sh_version_r2.txt, sh_version_r3.txt
* с помощью функции parse_sh_version, из каждого вывода должна быть получена
  информация ios, image, uptime
* из имени файла нужно получить имя хоста
* после этого вся информация должна быть записана в CSV файл

В файле routers_inventory.csv должны быть такие столбцы (именно в этом порядке):
* hostname, ios, image, uptime

В скрипте, с помощью модуля glob, создан список файлов, имя которых начинается
на sh_vers. Вы можете раскомментировать строку print(sh_version_files),
чтобы посмотреть содержимое списка.

Кроме того, создан список заголовков (headers), который должен быть записан в CSV.
"""

import glob

sh_version_files = glob.glob("sh_vers*")
# print(sh_version_files)

headers = ["hostname", "ios", "image", "uptime"]
def write_inventory_to_csv(data_filenames, csv_filename):
    ios = r'.+ Version (\d+\.\S+),'
    image = r'System .+ \"(\S+)\"'
    uptime = r'router uptime is (.+)\n'
    data2 = []
    for file in sh_version_files:
        host = re.search(r'version_(\S+).txt$', file)
        with open(file) as f:
            data = dict.fromkeys(headers)
            for line in f:
                match_ios = re.search(ios, line)
                match_image = re.search(image, line)
                match_uptime = re.search(uptime, line)
                data['hostname'] = host.group(1)
                if match_ios:
                    data['ios'] = match_ios.group(1)
                elif match_image:
                    data['image'] = match_image.group(1)
                elif match_uptime:
                    data['uptime'] = match_uptime.group(1)
            data2.append(data)
    with open(csv_filename,'w') as dst:
        writer = csv.DictWriter(dst, fieldnames = headers)
        writer.writeheader()
        for d in data2:
            writer.writerow(d)
                    
if __name__ == "__main__":
    write_inventory_to_csv(sh_version_files, 'out_17_2.csv' )

#Answer
'''
import re
import csv
import glob


def parse_sh_version(sh_ver_output):
    regex = (
        "Cisco IOS .*? Version (?P<ios>\S+), .*"
        "uptime is (?P<uptime>[\w, ]+)\n.*"
        'image file is "(?P<image>\S+)".*'
    )
    match = re.search(regex, sh_ver_output, re.DOTALL,)
    if match:
        return match.group("ios", "image", "uptime")


def write_inventory_to_csv(data_filenames, csv_filename):
    headers = ["hostname", "ios", "image", "uptime"]
    with open(csv_filename, "w") as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        for filename in data_filenames:
            hostname = re.search("sh_version_(\S+).txt", filename).group(1)
            with open(filename) as f:
                parsed_data = parse_sh_version(f.read())
                if parsed_data:
                    writer.writerow([hostname] + list(parsed_data))


if __name__ == "__main__":
    sh_version_files = glob.glob("sh_vers*")
    write_inventory_to_csv(sh_version_files, "routers_inventory.csv")
'''
'''
#Эмиль редактор
import glob
import re
import csv


sh_version_files = glob.glob("sh_vers*") # файлы с выводом команд
#print(sh_version_files) 

HEADERS = ["hostname", "ios", "image", "uptime"] # заголовки для таблицы
IOS = r'.+ Version (\d+\.\S+),'   
IMAGE = r'System .+ \"(\S+)\"'
UPTIME = r'router uptime is (.+)\n'
HOST = r'version_(\S+).txt$'


def parsing_from_file(filename): 
# Функция парсит из файла данные регулярками и возвращает словарь    

    with open(filename) as file:
        data = {}     # Создаем словарь с ключами заголовков
        for line in file:# Перебираем строки в файле, проверяем регулярки
            match_ios = re.search(IOS, line)
            match_image = re.search(IMAGE, line)
            match_uptime = re.search(UPTIME, line)
            match_hostname = re.search(HOST, filename)
            
            if match_ios:
                data['ios'] = match_ios.group(1) # Наполняем пустой словарь
            elif match_image:
                data['image'] = match_image.group(1)
            elif match_uptime:
                data['uptime'] = match_uptime.group(1)
            data['hostname'] = match_hostname.group(1)

    return data # Возвращает словарь


def writing_in_csv(data, csv_filename):
# Функция принимает список словарей и возвращает файл в формате csv
    with open(csv_filename, 'w') as result:
        writer = csv.DictWriter(result, fieldnames = HEADERS) # словарь в запись csv
        writer.writeheader()   # пишем заголовки 

        for d in data:         # заполняем таблицу
            writer.writerow(d)


def write_inventory_to_csv(data_filenames, csv_filename):
# Функция принимает на вход файлы txt возвращает сводный файл в формате csv
    data_out = []

    for filename in sh_version_files:  # Перебираем файлы
        data_out.append(parsing_from_file(filename)) # Собираем список словарей
    writing_in_csv(data_out, csv_filename)

                   
if __name__ == '__main__':
    write_inventory_to_csv(sh_version_files, 'out_17_2.csv' )
'''
