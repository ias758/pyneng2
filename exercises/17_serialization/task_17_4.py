# -*- coding: utf-8 -*-
"""
Задание 17.4

Создать функцию write_last_log_to_csv.

Аргументы функции:
* source_log - имя файла в формате csv, из которого читаются данные (mail_log.csv)
* output - имя файла в формате csv, в который будет записан результат

Функция ничего не возвращает.

Функция write_last_log_to_csv обрабатывает csv файл mail_log.csv.
В файле mail_log.csv находятся логи изменения имени пользователя. При этом, email
пользователь менять не может, только имя.

Функция write_last_log_to_csv должна отбирать из файла mail_log.csv только
самые свежие записи для каждого пользователя и записывать их в другой csv файл.
В файле output первой строкой должны быть заголовки столбцов,
такие же как в файле source_log.

Для части пользователей запись только одна и тогда в итоговый файл надо записать
только ее.
Для некоторых пользователей есть несколько записей с разными именами.
Например пользователь с email c3po@gmail.com несколько раз менял имя:
C=3PO,c3po@gmail.com,16/12/2019 17:10
C3PO,c3po@gmail.com,16/12/2019 17:15
C-3PO,c3po@gmail.com,16/12/2019 17:24

Из этих трех записей, в итоговый файл должна быть записана только одна - самая свежая:
C-3PO,c3po@gmail.com,16/12/2019 17:24

Для сравнения дат удобно использовать объекты datetime из модуля datetime.
Чтобы упростить работу с датами, создана функция convert_str_to_datetime - она
конвертирует строку с датой в формате 11/10/2019 14:05 в объект datetime.
Полученные объекты datetime можно сравнивать между собой.
Вторая функция convert_datetime_to_str делает обратную операцию - превращает
объект datetime в строку.

Функции convert_str_to_datetime и convert_datetime_to_str использовать не обязательно.

"""

import csv
import datetime


def convert_str_to_datetime(datetime_str):
    '''
    Конвертирует строку с датой в формате 11/10/2019 14:05 в объект datetime.
    '''
    return datetime.datetime.strptime(datetime_str, '%d/%m/%Y %H:%M')


def convert_datetime_to_str(datetime_obj):
    '''
    Конвертирует строку с датой в формате 11/10/2019 14:05 в объект datetime.
    '''
    return datetime.datetime.strftime(datetime_obj, '%d/%m/%Y %H:%M')


def read_csv_file(filename):
    '''
    Чтение файла csv
    '''
    with open(filename) as f:
        DATA = list(csv.reader(f))

    return DATA

        
def sort_date(data):
    '''
    Выбор данных из таблицы и изменение их формата
    '''
    return convert_str_to_datetime(data[2])


def write_csv(data, headers, filename):
    '''
    Запись в файл формат csv
    '''
    with open(filename, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        for row in data.values():
            writer.writerow(row)


def write_last_log_to_csv(source_log, output):
    '''
    Обработка файла
    '''
    RESULT = {}
    FILE = read_csv_file(source_log)
    HEADERS = FILE[0]
    SORTED_LIST = sorted(FILE[1:], key = sort_date)

    for NAME, MAIL, DATE in SORTED_LIST:
        RESULT[MAIL] = (NAME, MAIL, DATE)
    
    write_csv(RESULT, HEADERS, output)
    
    
if __name__ == '__main__':
    print(write_last_log_to_csv('mail_log.csv', '17_4_out.csv'))
