# -*- coding: utf-8-*-
import ast
import os
import subprocess
import sys
import time

DATA = DATA1 = ''


def cat_log():
    path = sys.argv[1]
    log = subprocess.Popen('cat %s/*.txt' % path, shell=True, stdout=subprocess.PIPE)
    for line in iter(log.stdout.readline, ''):
        try:
            line = line.decode()
            if line == '':
                return
            find_data_mult(line)
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
        print(DATA)

    elif 'CALLBACK = asr.tts-result' in line:
        if len(DATA.split()) != 5:
            return
        d = ' ' + line.split()[1]
        res = DATA.split()
        b = res[:-1]
        a = ' ' + res[-1]
        DATA = str(b).replace('[', '').replace(']', '').replace('\'', '').replace(',', '') + d + a
    elif ('final_result' in line and 'CALLBACK' in line) or 'finalResult' in line:
        if len(DATA.split()) != 3:
            return
        line = ast.literal_eval(line[line.find('{'):])
        text = line['results_recognition'][0]
        DATA += ' ' + text


def find_data_mult(line):
    global DATA, DATA1
    if 'CALLBACK = asr.end' in line:
        DATA = line.split()[1]

    elif 'CALLBACK = asr.partialfinal_result' in line:
        if len(DATA.split()) != 1:
            return
        DATA += ' ' + line.split()[1]
    elif 'CALLBACK = asr.tts-result' in line:
        if len(DATA.split()) != 2:
            return
        d = ' ' + line.split()[1]
        DATA += d + DATA1
        print(DATA)
    elif 'finalResult' in line:
        if len(DATA.split()) != 1:
            return
        line = ast.literal_eval(line[line.find('{'):])
        text = line['results_recognition'][0]
        DATA1 = ' ' + text


if __name__ == '__main__':
    first = True
    print('wakeup       first_word   asr.end      asr.finish   result')
    cat_log()
