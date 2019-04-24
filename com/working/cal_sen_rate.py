import os

import xlrd
import sys


class Main(object):
    def __init__(self):
        self.ans = 'ans.txt'
        self.res = 'res.txt'
        self.cal_acu = {}

    def set_answer(self, ans):
        with open(self.ans, 'w', encoding='gbk')as f:
            index = 1
            for line in ans[:-1].split('\n'):
                msg = (str(index) + '\t' + line + '\n')
                f.write(msg)
                index += 1
        return self

    def set_result(self, res):
        with open(self.res, 'w', encoding='gbk') as f:
            index = 1
            for line in res[:-1].split('\n'):
                msg = (str(index) + '\t' + line + '\n')
                f.write(msg)
                index += 1
        return self

    def cal_rate(self, key_name, l):
        os.system('./wer %s %s fnl.txt' % (self.ans, self.res))
        with open('fnl.txt', 'r', encoding='gbk') as f:
            lines = f.readlines()
            CHARACTOR_ACU = lines[-2:-1][0].split()[1]
            UTTERANCE_ACU = lines[-1:][0].split()[1]
            print(key_name + '---' + str(l) + '句')
            print(CHARACTOR_ACU)
            print(UTTERANCE_ACU + '\n')


def read_xl():
    workbook = xlrd.open_workbook(file)
    names = workbook.sheet_names()
    sen_len = 0
    ans = ''
    result_map = {}
    for sheet_name in names:
        if 'm' in sheet_name or '识别' in sheet_name or 'asr' in sheet_name.lower():
            sheet = workbook.sheet_by_name(sheet_name)
            # 获取query数量
            if sen_len == 0:
                cols = sheet.col_values(2, 1)
                for e in cols:
                    if e == '':
                        break
                    sen_len += 1
            # 获取原始query
            if ans == '':
                cols = sheet.col_values(1, 1, sen_len + 1)
                for e in cols:
                    ans += e + '\n'
                result_map['answer'] = ans
            # 获取列数
            if True:
                rows = sheet.row_values(1, 2)
                row_len = len(rows)
            # 获取识别结果
            for r in range(row_len):
                res = ''
                if r % 2 == 1:
                    continue
                cols = sheet.col_values(2 + r, 0, sen_len + 1)
                title = cols[0]
                for e in cols[1:]:
                    if str(e).strip() == '':
                        continue
                    res += e + '\n'
                result_map['%s>%s' % (sheet_name, title)] = res[:-1]
    return result_map


def write_xl():
    pass


if __name__ == '__main__':
    file = sys.argv[1]
    m = Main()
    for k, v in read_xl().items():
        if k == 'answer':
            m.set_answer(v)
        else:
            m.set_result(v)
            m.cal_rate(k, len(v.split('\n')))
        #     m.start_cal()
        #     break
    os.system('rm ans.txt')
    os.system('rm res.txt')
    os.system('rm fnl.txt')
