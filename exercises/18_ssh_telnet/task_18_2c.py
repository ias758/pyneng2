# -*- coding: utf-8 -*-
"""
Задание 18.2c

Скопировать функцию send_config_commands из задания 18.2b и переделать ее таким образом:

Если при выполнении команды возникла ошибка, спросить пользователя надо ли выполнять
остальные команды.

Варианты ответа [y]/n:
* y - выполнять остальные команды. Это значение по умолчанию,
  поэтому нажатие любой комбинации воспринимается как y
* n или no - не выполнять остальные команды

Функция send_config_commands по-прежнему должна возвращать кортеж из двух словарей:
* первый словарь с выводом команд, которые выполнились без ошибки
* второй словарь с выводом команд, которые выполнились с ошибками

Оба словаря в формате
* ключ - команда
* значение - вывод с выполнением команд

Проверить работу функции можно на одном устройстве.

Пример работы функции:

In [11]: result = send_config_commands(r1, commands)
Подключаюсь к 192.168.100.1...
Команда "logging 0255.255.1" выполнилась с ошибкой "Invalid input detected at '^' marker." на устройстве 192.168.100.1
Продолжать выполнять команды? [y]/n: y
Команда "logging" выполнилась с ошибкой "Incomplete command." на устройстве 192.168.100.1
Продолжать выполнять команды? [y]/n: n

In [12]: pprint(result)
({},
 {'logging': 'config term\n'
             'Enter configuration commands, one per line.  End with CNTL/Z.\n'
             'R1(config)#logging\n'
             '% Incomplete command.\n'
             '\n'
             'R1(config)#',
  'logging 0255.255.1': 'config term\n'
                        'Enter configuration commands, one per line.  End with '
                        'CNTL/Z.\n'
                        'R1(config)#logging 0255.255.1\n'
                        '                   ^\n'
                        "% Invalid input detected at '^' marker.\n"
                        '\n'
                        'R1(config)#'})

"""

# списки команд с ошибками и без:
commands_with_errors = ['logging 0255.255.1', 'logging', 'a']
correct_commands = ['interface f0/22', 'description Test_Script_2']

commands = commands_with_errors + correct_commands

import re
import yaml

from netmiko import (
    ConnectHandler,
    NetmikoAuthenticationException,
    NetmikoTimeoutException,
    )


def break_if_no(i):
    
    while True:
        answer = input('Продолжать выполнять команды? y/n: ')
        
        if answer.lower() in ('n', 'no'):
           return False
        elif answer.lower()in ('y','yes'):
            return True
        else:
            continue


def send_config_commands(dev, commands, log = True):
    
    try:
        regex = r'% (?P<err>.+)'
        correct_commands = {}
        incorrect_commands = {}
        errmsg = 'Команда {} выполнилась с ошибкой {} на устройстве {}'

        if log:
            print(f"Подключение к {dev['host']}... ")

        with ConnectHandler(**dev) as ssh:
            ssh.enable()

            for command in commands:
                result = ssh.send_config_set(command, exit_config_mode=False)
                error = re.search(regex, result)

                if error:
                    print(errmsg.format(command, error.group('err'), ssh.host))
                    incorrect_commands[command] = result
                    if break_if_no(command) is False:
                        break
                           
                else:
                    correct_commands[command] = result
                    
            ssh.exit_config_mode()
        result = (incorrect_commands, correct_commands)
        return result
    
    except (NetmikoAuthenticationException, NetmikoTimeoutException ) as error:
        print(error)
        
    

if __name__ == "__main__":
    #commands = ['interface f0/22', 'description Test_Script_2']
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)

    for dev in devices:
        print(send_config_commands(dev, commands))
