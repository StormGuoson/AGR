# -*- coding: utf-8-*-
import csv
import os
import re
import sys
from time import time

import xlrd
import xlwt
from xlutils.copy import copy

SELF_NAME = os.path.basename(sys.argv[0]).split(".")[0]


class MainSearch(object):
    _start = 0
    _end = 0
    _min = _max = -1

    def __init__(self, path, name, only=False, mode=1):
        """
                searching specific files
                :param path:root path
                :param name:file searched
                :param only:stop searching after find 1 file
                :param mode:searching order > 0 or 1,0 is hor,1 is ver
                :return:
        """
        self.mode = mode
        self.only = only
        self.name = name
        self.path = path
        self._result_paths = []

    def _search_files(self):

        _paths = [os.path.join(self.path, x) for x in os.listdir(self.path)]
        while len(_paths) != 0:
            _f = _paths.pop(0)
            if os.path.isfile(_f):
                size = os.path.getsize(_f)
                if self._min != -1 and self._max != -1:
                    if size < self._min or size > self._max:
                        continue
                elif self._min != -1:
                    if size < self._min:
                        continue
                elif self._max != -1:
                    if size > self._max:
                        continue
                is_match = re.match(self.name, os.path.split(_f)[1])
                if is_match:
                    self._result_paths.append(_f)
                    if self.only:
                        break
                        # if self.name == os.path.split(_f)[1]:
                        #     self._result_paths.append(_f)
                        # elif self.name.startswith('*') and self.name.endswith('*') and os.path.split(_f)[1].find(
                        #         self.name[1:-1]) != -1:
                        #     self._result_paths.append(_f)
                        # elif self.name.startswith('*') and os.path.split(_f)[1].endswith(self.name[1:]):
                        #     self._result_paths.append(_f)
                        # elif self.name.endswith('*') and os.path.split(_f)[1].startswith(self.name[:-1]):
                        #     self._result_paths.append(_f)
                        # if self.only:
                        #     break
            elif os.path.isdir(_f):
                if self.mode == 0:
                    for p in os.listdir(_f):
                        _paths.append(os.path.join(_f, p))
                else:
                    self.path = _f
                    self._search_files()

    def set_min(self, i):
        self._min = i
        return self

    def set_max(self, i):
        self._max = i
        return self

    def start(self):
        self._start = time()
        self._search_files()
        self._end = time()

    def take_time(self):
        return self._end - self._start

    def get_paths(self):
        return self._result_paths

    def set_paths(self, ls):
        self._result_paths = ls
        return self

    def searching_time(self):
        return int((self._end - self._start) * 1000) / 1000.0

    def removes(self):
        for _f in self._result_paths:
            os.remove(_f)
        self._end = time()

    def together(self, path):
        """
        :param path: put them all in here
        :return:
        """
        for f in self._result_paths:
            if not os.path.exists(path):
                os.makedirs(path)
            os.rename(f, path + os.path.split(f)[1])
        self._end = time()

    def rename(self, f, t):
        for fi in self._result_paths:
            p = fi[:fi.rfind('/') + 1]
            n = os.path.split(fi)[1]
            is_fit = re.search(f, n)
            if is_fit:
                f = is_fit.group()
                if f == t:
                    continue
                os.chdir(os.path.split(fi)[0])
                try:
                    os.rename(fi, p + n.replace(f, t))
                except WindowsError:
                    print(fi)


def save_memory(filename, content):
    mp = filename[:filename.rfind(os.sep)]
    if not os.path.exists(mp):
        os.makedirs(mp)
    with open(filename, "a+") as f:
        f.write(content + '\n')


def foo1(_paths):
    result = ''
    need = False
    num = _min = _max = ''
    code = 'utf-8'
    for p in _paths:
        abs_path = str(p)
        # result = result.replace('result', 'working').replace('TextGrid', 'txt')
        # continue
        # with open(p) as c:
        #     data = c.read()
        #     code = chardet.detect(data)['encoding']
        #     # if code == 'UTF-16':
        #     #     code = 'utf-16-be'
        #     # if code == 'ascii':
        #     #     code = 'utf-8'
        #     print code
        with open(p) as f:
            for line in f.readlines():
                if line.find('intervals') != -1 and line.find('[') != -1:
                    num = int(line[line.find('[') + 1:line.find(']')])
                    if num % 2 == 0:
                        num = num / 2
                        if num < 10:
                            num = '00000' + str(num)
                        elif num < 100:
                            num = '0000' + str(num)
                        else:
                            num = '000' + str(num)
                        # print num
                        need = True
                    else:
                        need = False
                elif need:
                    if line.find('xmin') != -1:
                        _min = line[line.find('=') + 2: -1]
                        # print _min
                    elif line.find('xmax') != -1:
                        _max = line[line.find('=') + 2: -1]
                        # print _max
                    elif line.find('text') != -1:
                        text = line[line.find(r'"') + 1: line.rfind(r'"')]
                        # print text
                        # text = num + " " + str(_min) + "-" + str(_max) + ' ' + text

                        _min = str(int(float(_min) * 16000))
                        _max = str(int(float(_max) * 16000))
                        _num = (int(num) + 1) / 2
                        if _num < 10:
                            _num = '00000' + str(_num)
                        elif _num < 100:
                            _num = '0000' + str(_num)
                        else:
                            _num = '000' + str(_num)

                        if text == u'小度小度' or text == u'小维小维':
                            tmp_path = abs_path[abs_path.find('\\') + 1:abs_path.rfind('.')]
                            # result = tmp_path + '\t' + _num + '\t' + _min + '\t' + _max + '\t'
                            result = '\t'
                        else:
                            result += _min + '-' + _max + '\t' + text
                            print(result)
                            save_memory(abs_path.replace('TextGrid', 'txt'), result)
                            result = ''
                            # save_memory(result, text)
                            # print result


def foo3(_paths):
    for p in _paths:
        abs_path = str(p)
        with open(abs_path) as f:
            for line in f.readlines():
                # path = 'd:\\qiefen\\' + line.split(' ')[0] + '.txt'
                # num = line.split(' ')[1]
                # start = line.split(' ')[2]
                # end = line.split(' ')[3]
                # text = line.split(' ')[4]
                # result = num + ' ' + start + '-' + end + ' ' + text
                # save_memory(path, result)
                if len(line) > 3:
                    save_memory(abs_path.replace('rec', 'final'), line)


def add_title(_paths):
    for p in _paths:
        oldWb = xlrd.open_workbook(p)
        oldWbS = oldWb.sheet_by_index(0)
        newWb = copy(oldWb)
        newWs = newWb.get_sheet(0)
        inserColNo = 0
        newWs.write(0, inserColNo, "项目名称")
        for i in range(1, oldWbS.nrows):
            newWs.write(i, inserColNo, os.path.basename(p)[:-5])

        for rowIndex in range(inserColNo, oldWbS.nrows):
            for colIndex in range(oldWbS.ncols):
                newWs.write(rowIndex, colIndex + 1, oldWbS.cell(rowIndex, colIndex).value)
        newWb.save(p.replace('xlsx', 'xls'))
        # newWb.save(p)


if __name__ == '__main__':
    _path = r'/Users/baidu/Desktop/导流Vmall项目'
    main = MainSearch(_path, u'[\S\s]+.xlsx')
    main.start()
    add_title(main.get_paths())
