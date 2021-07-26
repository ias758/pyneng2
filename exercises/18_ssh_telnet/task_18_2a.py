# -*- coding: utf-8 -*-
"""
Задание 18.2a

Скопировать функцию send_config_commands из задания 18.2 и добавить параметр log,
который контролирует будет ли выводится на стандартный поток вывода информация о том
к какому устройству выполняется подключение.
По умолчанию, результат должен выводиться.

Пример работы функции:

In [13]: result = send_config_commands(r1, commands)
Подключаюсь к 192.168.100.1...

In [14]: result = send_config_commands(r1, commands, log=False)

In [15]:

Скрипт должен отправлять список команд commands на все устройства
из файла devices.yaml с помощью функции send_config_commands.
"""
import yaml

from netmiko import (
    ConnectHandler,
    NetmikoAuthenticationException,
    NetmikoTimeoutException,
    )



def send_config_commands(dev, commands, log = True):
    
    try:
        if log:
            print(f"Подключение к {dev['host']}... ")

        with ConnectHandler(**dev) as ssh:
            ssh.enable()
            result = ssh.send_config_set(commands)

        return result
    
    except (NetmikoAuthenticationException, NetmikoTimeoutException ) as error:
        print(error)
        
    

if __name__ == "__main__":
    commands = ['interface f0/22', 'description Test_Script']
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)

    for dev in devices:
        print(send_config_commands(dev, commands))
