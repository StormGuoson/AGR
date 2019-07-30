import os
import re
import sys


class MainSearch(object):
    """
            searching specific files
            author: guoyuqiang
            :param path:root path
            :param name:filename searched
            :param only:stop searching after find 1 file
            :param mdir:file or dir,true is file
            :param mode:searching order > 0 or 1,0 is hor,1 is ver
    """
    _min = _max = -1

    def __init__(self, path=None, name='[\S\s]*', only=False, mdir=False, mode=1):

        self.mode = mode
        self.only = only
        self.name = name
        self.path = path
        self.mdir = mdir
        self._result_files = []

    def _search_files(self):

        _paths = [os.path.join(self.path, x) for x in os.listdir(self.path)]
        while len(_paths) != 0:
            _f = _paths.pop(0)
            if self.mdir:
                if os.path.isdir(_f):
                    self._result_files.append(_f)
                    for p in os.listdir(_f):
                        p = os.path.join(_f, p)
                        if os.path.isdir(p):
                            _paths.append(p)
                            self._result_files.append(p)
            else:
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

    def set_name(self, name):
        self.name = name

    def set_max(self, i):
        self._max = i
        return self

    def set_path(self, path):
        self.path = path

    def start(self):
        self._result_files.clear()
        self._search_files()

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


def foo(paths):
    index = 0
    answer = rec = ''
    for path in paths:
        if index == 0:
            answer = path
            index = 1
        else:
            index = 0
            rec = path
            print(answer + '---' + rec)
            # os.system('./wer-lnx %s %s fnl.txt' % (answer, rec))
            # with open('fnl.txt', 'r') as f:
            #     lines = f.readlines()
            #     CHARACTOR_ACU = lines[-2:-1][0].split()[1]
            #     UTTERANCE_ACU = lines[-1:][0].split()[1]
            #     print(CHARACTOR_ACU + '---' + UTTERANCE_ACU)


def add(paths):
    ans = 'anjing_total ans.txt'
    rec = 'anjing_total_rec.txt'
    max_ans = max_rec = 0
    f_ans = open(ans, 'w')
    f_rec = open(rec, 'w')
    for p in paths:
        with open(p, 'r') as f:
            lines = f.readlines()
            last_line = lines[-1].split('.')[0]
            if 'ans' in p:
                for line in lines:
                    num = line[:line.find('.')]
                    f_ans.write(line.replace(num, str(int(num) + max_ans)))
                max_ans += int(last_line)
            else:
                for line in lines:
                    num = line[:line.find('.')]
                    f_rec.write(line.replace(num, str(int(num) + max_rec)))
                max_rec = max_ans

    f_ans.close()
    f_rec.close()


if __name__ == '__main__':
    main = MainSearch(sys.argv[1], 'anjing[\S\s]*.txt')
    main.start()
    fs = main.get_files()
    fs.sort()
    add(fs)
