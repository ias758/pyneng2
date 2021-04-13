# -*- coding: utf-8 -*-
"""
Задание 12.3

Создать функцию print_ip_table, которая отображает таблицу доступных
и недоступных IP-адресов.

Функция ожидает как аргументы два списка:
* список доступных IP-адресов
* список недоступных IP-адресов

Результат работы функции - вывод на стандартный поток вывода таблицы вида:

Reachable    Unreachable
-----------  -------------
10.1.1.1     10.1.1.7
10.1.1.2     10.1.1.8
             10.1.1.9

"""
from tabulate import tabulate
from task_12_1 import ping_ip_addresses
addresses = ['8.8.8.8', '255.254.252.1', '10.110.1.1']

def print_ip_table(address):
    table = {'Reachable':ping_ip_addresses(address)[0],'Unreachable':ping_ip_addresses(address)[1]}
    print(tabulate(table, headers = 'keys'))


if __name__ == "__main__":
    print_ip_table(addresses)
