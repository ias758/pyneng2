# -*- coding: utf-8 -*-
"""
Задание 12.1

Создать функцию ping_ip_addresses, которая проверяет пингуются ли IP-адреса.

Функция ожидает как аргумент список IP-адресов.

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для проверки доступности IP-адреса, используйте команду ping.

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""
import subprocess

addresses = ['8.8.8.8', '255.254.252.1', '10.110.1.1']


def ping_ip_addresses(address):
    reachable = []
    unreachable = []
    for ip in address:
        reply = subprocess.run(['ping', '-n', '3', ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if reply.returncode == 0:
            reachable.append(ip)
        else:
            unreachable.append(ip)
    return [reachable, unreachable]


if __name__ == "__main__":
    print(ping_ip_addresses(addresses))   
