import sys
import xlrd

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


class Main(object):
    def __init__(self):
        opt = webdriver.FirefoxOptions()
        # opt.add_argument('--headless')
        self.d = webdriver.Firefox(options=opt, service_log_path=None)
        self.d.get('http://bailing.audio.baidu-int.com:8081/index.php/tools/common/index?flag=1')
        self.d.find_element_by_id('username').send_keys('v_guoyuqiang')
        self.d.find_element_by_id('password').send_keys('v_guoyuqiang')
        self.d.find_element_by_id('emailLogin').click()

    def set_answer(self, ans):
        while True:
            try:
                self.d.find_element_by_id('werform-recognize_answer').send_keys(ans)
                break
            except NoSuchElementException:
                pass
        return self

    def set_result(self, res):
        self.d.find_element_by_id('werform-recognize_result').send_keys(res)
        return self

    def start_cal(self):
        self.d.find_elements_by_class_name('btn.btn-primary')[0].click()


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
                    res += e + '\n'
                result_map['%s>%s' % (sheet_name, title)] = res
    return result_map


if __name__ == '__main__':
    file = sys.argv[1]
    m = Main()
    for k, v in read_xl().items():
        if k == 'answer':
            m.set_answer(v)
        else:
            m.set_result(v)
            m.start_cal()
            break
