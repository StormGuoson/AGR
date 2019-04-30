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
    """
            searching specific files
            :param path:root path
            :param name:file searched
            :param only:stop searching after find 1 file
            :param mode:searching order > 0 or 1,0 is hor,1 is ver
    """
    _min = _max = -1

    def __init__(self, path, name, only=False, mode=1):

        self.mode = mode
        self.only = only
        self.name = name
        self.path = path
        self._result_files = []

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
                    self._result_files.append(_f)
                    if self.only:
                        break
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
        self._search_files()
        for f in self._result_files:
            print(f)

    def get_files(self):
        return self._result_files

    def removes(self):
        for _f in self._result_files:
            os.remove(_f)

    def together(self, path):
        """
        :param path: put them all in here
        :return:
        """
        for f in self._result_files:
            if not os.path.exists(path):
                os.makedirs(path)
            os.rename(f, path + os.path.split(f)[1])

    def rename(self, before, after):
        for fi in self._result_files:
            p = fi[:fi.rfind(os.sep) + 1]
            n = os.path.split(fi)[1]
            is_fit = re.search(before, n)
            if is_fit:
                before = is_fit.group()
                if before == after:
                    continue
                # os.chdir(os.path.split(fi)[0])
                try:
                    os.rename(fi, p + n.replace(before, after))
                except WindowsError:
                    print(fi)


def save_memory(filename, content):
    mp = filename[:filename.rfind(os.sep)]
    if not os.path.exists(mp):
        os.makedirs(mp)
    with open(filename, "a+") as f:
        f.write(content + '\n')


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
    _path = r'/Users/baidu/Desktop/audio'
    main = MainSearch(_path, u'[\S]*3')
    main.start()
