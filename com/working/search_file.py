# -*- coding: utf-8-*-
import csv
import os
import re
import sys
from time import time

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


def foo4(path):
    for p in path:
        abs_path = str(p)
        abs_dir = abs_path[:abs_path.rfind('\\')]
        name = abs_path[abs_path.rfind('\\') + 1:]
        os.rename(abs_path, abs_dir + '\\wz_3m_fengchun_' + name)


def change_csv(paths):
    with open('result.csv', 'wb') as out:
        writer = csv.writer(out, dialect='excel')
        for p in paths:
            if 'result.csv' in p or SELF_NAME in p:
                continue
            reader = csv.reader(open(p))
            writer.writerows(reader)


def foo5(path):
    for p in path:
        with open(p) as fi:
            pi = str(p)
            name = pi.split('\\')[-1]
            finalPath = pi[:pi.rfind('\\') + 1] + 'final\\' + name
            index = 0
            tmp = ''
            resultMSG = ''
            item = 1
            isFindWake = False
            for line in fi:
                if line.find('item [1]') != -1:
                    item = 1
                elif line.find('item [2]') != -1:
                    item = 2
                index += 1
                # if index <= 14:
                #     continue
                if item == 11:
                    if line.find('xmin =') != -1:
                        if not isFindWake:
                            tmp = line[12:-2] + '\t'
                        else:
                            tmp += line[12:-2] + '\t'
                    elif line.find('xmax =') != -1:
                        tmp += line[12:-2] + '\t'
                    elif line.find('text =') != -1:
                        if line.find(r'""') != -1:
                            tt = tmp.split('\t')[:-3]
                            tmp = ''
                            for t in tt:
                                tmp += t + '\t'
                            continue
                        else:
                            if line.find(u'小度小度') != -1:
                                isFindWake = True
                            else:
                                tmp += line[12:]
                                resultMSG += pi + '\t' + tmp
                                isFindWake = False
                elif item == 2:
                    if line.find('xmin =') != -1:
                        tmp = line[12:-2] + '\t'
                    elif line.find('xmax =') != -1:
                        tmp += line[12:-2] + '\t'
                    elif line.find('text =') != -1:
                        if line.find(r'""') != -1:
                            tmp = ''
                            continue
                        else:
                            tmp += line[12:]
                            resultMSG += tmp
            # save_memory(finalPath, resultMSG)
            print(resultMSG)


def foo7(path):
    for p in path:
        finalMsg = ''
        missFinal = False
        with open(p, 'r') as f:
            line = f.readlines()[0]
            line = line.replace(u'、', u'、\n').replace(u'，', u'，\n').replace(u'。', u'。\n').replace(u'！', u'！\n').replace(
                u'？', u'？\n')
            lines = line.split('\n')
            lengh = 0
            oneline = ''
            for li in lines:
                # print li
                oneline += li
                lengh += len(li)
                if lengh > 35:
                    finalMsg += oneline[:-len(li)] + '\n'
                    oneline = li
                    lengh = len(li)
            finalMsg += oneline
            print(finalMsg)
        with open(p, 'w') as f:
            f.write(finalMsg)


def foo8(paths):
    for p in paths:
        result_path = str(p).replace('_.TextGrid', '_result.txt').replace('.TextGrid', '_result.txt')
        time_path = str(p).replace('_.TextGrid', '_time.txt').replace('.TextGrid', '_time.txt')
        finalMsg = ''
        finalTime = ''
        tmpTime = ''
        try:
            with open(p, 'r') as f:
                lines = f.readlines()[14:]
                for line in lines:
                    if 'xmin' in line:
                        tmpTime += line[line.find('xmin') + 7:-1] + ' '
                    elif 'xmax' in line:
                        tmpTime += line[line.find('xmax') + 7:-1]
                    elif 'text' in line:
                        text = line[line.find('\"') + 1:line.rfind('\"')]
                        if text == '':
                            tmpTime = ''
                        elif text == '小度小度':
                            tmpTime += ' '
                        else:
                            finalMsg += text + '\n'
                            finalTime += tmpTime + '\n'
                            tmpTime = ''
            save_memory(result_path, finalMsg)
            save_memory(time_path, finalTime)
        except UnicodeDecodeError as e:
            print('code error ' + str(p))
            # pass


def foo9(paths):
    finalMsg = ''
    for p in paths:
        with open(p, 'r') as f:
            lines = f.readlines()
            for line in lines:
                after = line.split()
                for a in after[1:]:
                    finalMsg += after[0] + ' ' + a + '\n'
    #             if len(line) > 4:
    #                 finalMsg += line
    save_memory('./spk2utt.txt', finalMsg)
    # print(finalMsg)


def format_name(paths):
    for p in paths:
        old_name = p[p.rfind(os.sep) + 1:]
        new_name = old_name
        if len(old_name) == 5:
            new_name = '00' + old_name
        elif len(old_name) == 6:
            new_name = '0' + old_name
        if old_name != new_name:
            new_path = os.path.join(os.path.dirname(p), new_name)
            os.rename(p, new_path)


def put_here(paths):
    # 创建指令词路径
    for d in order_spell_lists:
        cur_dir = os.path.join(result_path, d)
        os.makedirs(cur_dir)

    t_dir = ''
    index = 0
    for p in paths:
        cur_dir = os.path.dirname(p)
        last_dir = cur_dir[cur_dir.rfind(os.sep) + 1:]  # 上一级目录
        if t_dir != last_dir:
            index = 0
        t_dir = last_dir
        result_dir = os.path.join(result_path, order_spell_lists[index])  # 结果存放目录
        txt_dir = os.path.join(result_dir, order_spell_lists[index] + '.txt')  # 保存结果的文本路径
        aud_dir = os.path.join(result_dir, (order_spell_lists[index] + '-' + last_dir + '.pcm'))  # 音频结果路径
        aud_name = aud_dir[aud_dir.rfind(os.sep) + 1:]  # 音频结果名
        save_memory(txt_dir, '%s:%s:10' % (aud_name, order_cn_lists[index]))
        os.rename(p, aud_dir)

        index += 1


order_cn_lists = ('播放列表', '循环播放', '查看歌词', '打开音乐', '打开导航',
                  '回到首页', '加入收藏', '屏幕亮一点', '屏幕暗一点', '上一页',
                  '下一页', '回主页', '打开车窗', '关闭车窗', '温度降低',
                  '温度升高', '声音大一点', '声音小一点', '小度小度', '你好哈弗',
                  '返回', '随机播放', '顺序播放', '单曲循环', '躲避拥堵',
                  '导航声音大一点', '导航声音小一点', '退出')
order_spell_lists = ('bofangliebiao', 'xunhuanbofang', 'chankangeci', 'dakaiyinyue', 'dakaidaohang',
                     'huidaoshouye', 'jiarushoucang', 'pingmuliangyidian', 'pingmuanyidian', 'shangyiye',
                     'xiayiye', 'huizhuye', 'dakaichechuang', 'guanbichechuang', 'jiangdiwendu',
                     'wendushenggao', 'shengyindayidian', 'shengyinxiaoyidian', 'xiaoduxiaodu', 'nihaohafu',
                     'fanhui', 'suijibofang', 'shunxubofang', 'danquxunhuan', 'duobiyongdu',
                     'daohangshengyindayidian', 'daohangshengyinxiaoyidian', 'tuichu')

if __name__ == '__main__':
    result_path = '/Users/baidu/Desktop/result'
    _path = r'/Users/baidu/Downloads/2019-2-26'
    main = MainSearch(_path, u'[\S\s]+.pcm')

    main.start()
    format_name(main.get_paths())

    main.start()
    path = main.get_paths()
    path = sorted(path)
    put_here(path)
