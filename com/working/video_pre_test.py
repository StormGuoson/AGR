# -*- coding: utf-8-*-
import ast
import os
import subprocess
import sys
import time

DATA = ''


def cat_log():
    path = sys.argv[1]
    log = subprocess.Popen('cat %s/*.txt' % path, shell=True, stdout=subprocess.PIPE)
    for line in iter(log.stdout.readline, ''):
        try:
            line = line.decode()
            if line == '':
                return
            find_data(line)
        except UnicodeDecodeError:
            pass


def find_data(line):
    global DATA
    if 'CALLBACK = wp.data' in line:
        DATA = line.split()[1]
    elif 'CALLBACK = asr.partialfirst_package' in line:
        if len(DATA.split()) != 1:
            return
        DATA += ' ' + line.split()[1]
    elif 'CALLBACK = asr.end' in line:
        if len(DATA.split()) != 2:
            return
        DATA += ' ' + line.split()[1]
    elif 'CALLBACK = asr.partialfinal_result' in line:
        if len(DATA.split()) != 4:
            return
        d = ' ' + line.split()[1]
        res = DATA.split()
        b = res[:-1]
        a = ' ' + res[-1]
        DATA = str(b).replace('[', '').replace(']', '').replace('\'', '').replace(',', '') + d + a
    elif 'CALLBACK = asr.tts-result' in line:
        if len(DATA.split()) != 5:
            return
        d = ' ' + line.split()[1]
        res = DATA.split()
        b = res[:-1]
        a = ' ' + res[-1]
        DATA = str(b).replace('[', '').replace(']', '').replace('\'', '').replace(',', '') + d + a
        print(DATA)
    elif 'Final result' in line:
        if len(DATA.split()) != 3:
            return
        line = ast.literal_eval(line[line.find('{'):])
        text = line['results_recognition'][0]
        DATA += ' ' + text


def format_time(t):
    global dur_time, first
    timeArray = time.strptime(t, "%H:%M:%S.%f")
    timeStamp = time.mktime(timeArray)
    if first:
        dur_time = timeStamp - dur_time
        first = False
    final = timeStamp - dur_time
    print(final)
    timeArray = time.localtime(final)
    otherStyleTime = time.strftime("%H:%M:%S.%f", timeArray)
    return otherStyleTime


if __name__ == '__main__':
    first = True
    print('wakeup       first_word   asr.end      asr.finish   tts          result')
    cat_log()
    # dur_time = sys.argv[2]
    # dur_time = '02.165'
    # ta = time.strptime(dur_time, "%S.%f")
    # dur_time = time.mktime(ta)
    # print(dur_time)
    # t = format_time('22:03:18.274')
    # print(t)
