# -*- coding: utf-8-*-
import os
import sys
import threading
import time

import uiautomator2 as at
import subprocess


def get_device_list():
    device_sn_list = []
    m_file = os.popen("adb devices")
    for line in m_file.readlines():
        if line.find("List of devices attached") != -1 or line.find('start') != -1 or line.find('daemon') != -1:
            continue
        elif len(line) > 5:
            device_sn_list.append(line.split("\t")[0])
    m_file.close()
    return device_sn_list


def add_devices():
    for d1 in get_device_list():
        if style == 'native':
            pass
        else:
            devices[d1] = at.connect_usb(d1)


def tail_file():
    p = sys.argv[0].split('/')
    sp = subprocess.Popen('tail -f -n 0 /%s/%s/..wakeup' % (p[1], p[2]), stdout=subprocess.PIPE, shell=True)
    for line in iter(sp.stdout.readline, ''):
        threading.Thread(target=do, args=(line,)).start()


def do(line):
    try:
        line = line.decode()
        if style == 'native':
            cmd = 'adb -s %s shell input tap 100 100' % line[:-1]
            os.popen(cmd)
            print(cmd)
        else:
            time.sleep(.3)
            devices[line[:-1]].click(100, 100)
    except UnicodeDecodeError:
        pass


def start():
    print('\33[5;33m开始监听\33[0m')
    for d in get_device_list():
        print(d)
    add_devices()
    tail_file()


if __name__ == '__main__':
    devices = {}
    style = ''
    if len(sys.argv) > 1:
        style = 'native'
    start()
