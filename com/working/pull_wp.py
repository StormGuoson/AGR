import time
import os

if __name__ == '__main__':
    # time.sleep(3600 * 1.75)
    # devices = os.popen('adb devices | grep -vE "List|^$"|awk \'{print $1}\'').readlines()
    os.popen('adb -s 192.168')