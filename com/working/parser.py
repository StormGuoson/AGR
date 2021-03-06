# -*- coding: utf-8-*-
import os
import re
import sys


class MainSearch(object):
    """
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
        return self

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


def start():
    path = sys.argv[1]
    if os.path.isfile(path):
        p(path)
    else:
        main = MainSearch(path, '[\S\s]*')
        log = main.start().get_files()
        for l in log:
            if l.endswith('.DS_Store'):
                continue
            print(l)
            p(l)
            print('')


def p(log):
    count_push_data = duration_data = duration_tmp_result = duration_result = 0.0
    with open(log, 'r') as f:
        for line in f.readlines():
            if 'calling extend_c_decoder_push_data' in line:
                count_push_data += 1
            elif 'called  extend_c_decoder_push_data' in line:
                duration_data += float(line[line.find('cost ') + 5:line.rfind('ms')])
            elif 'called  extend_c_decoder_get_tmp_result' in line:
                duration_tmp_result += float(line[line.find('cost ') + 5:line.rfind('ms')])
            elif 'called  extend_c_decoder_get_result' in line:
                duration_result += float(line[line.find('cost ') + 5:line.rfind('ms')])
        print(count_push_data * 160.0 / (duration_data + duration_tmp_result + duration_result))
        print('push_data总数 ：%d' % count_push_data)
        print('push_data耗时 ：%d' % duration_data)
        print('tmp_result耗时：%d' % duration_tmp_result)
        print('result耗时    ：%d' % duration_result)


if __name__ == '__main__':
    start()
