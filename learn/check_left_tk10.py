import json
import sys
import threading
import time

from selenium import webdriver
import wx
import pygame


class Tools(object):
    def __init__(self):
        print('<<<init>>>')
        self.main_url = 'https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc&' \
                        'fs=哈尔滨,HBB&' \
                        'ts=北京,BJP&' \
                        'date=2019-02-10&' \
                        'flag=N,N,Y'
        self.final_tks = []
        self.origin_target_tks = []
        opt = webdriver.FirefoxOptions()
        # opt.add_argument('-headless')
        self.brw = webdriver.Firefox(options=opt)
        # with open('12306cookie.json', 'r') as f:
        #     cookie = json.loads(f.read())
        # print(cookie)
        # self.brw.get('https://kyfw.12306.cn/otn/login/init')
        # self.brw.delete_all_cookies()
        # time.sleep(1)
        # for c in cookie:
        #     self.brw.add_cookie(c)
        self.first_launch = True
        self.has_find_tks = False
        pygame.mixer.init()
        pygame.mixer.music.load("/Users/baidu/PycharmProjects/project/learn/dingdong.mp3")

    def _get_html(self):
        if self.first_launch:
            self.first_launch = False
            self.brw.get(self.main_url)
        else:
            self.brw.refresh()
        return self.brw.page_source
        # with open('tk.html', 'w') as f:
        #     f.write(brw.page_source)

    def parser_html(self):
        self.final_tks = []
        res = self._get_html()
        start = '<tbody id="queryLeftTable"><tr'
        end = '></tr></tbody>'
        if start not in res:
            return
        res = res[res.find(start):res.find(end)]
        # print(res)
        res = res.split('<tr id=')[1:]
        for r in res:
            # print(r)
            t = r[:r.find('</a>')]
            line = t[t.rfind('>') + 1:]
            t = r[r.find('cdz') + 5:]
            from_s = t[t.find('>') + 1:t.find('</')]
            t = t[t.find('>') + 1:]
            t = t[t.find('>') + 2:]
            to_s = t[t.find('>') + 1:t.find('<')]
            t = r[r.find('start-t'):]
            start_t = t[t.find('>') + 1:t.find('<')]
            t = r[r.find('color999'):]
            end_t = t[t.find('>') + 1:t.find('<')]
            t = r[r.find('class=\"ls\"'):]
            duration = t[t.find('strong') + 7:t.find('</strong')]
            kind_left = t.split('width="46" align="center">')[1:]
            kind_tks = []
            for l in kind_left:
                t = l[:l.find('<')]
                if t == '':
                    t = l[l.find('>'):]
                    t = t[1:t.find('<')]
                kind_tks.append(t)
            self.final_tks.append([line, from_s, to_s, start_t, end_t, duration, kind_tks])

    def get_tk(self, lines=None, duration=1000):
        self.parser_html()
        target_tks = []
        if lines is None:
            for t in self.final_tks:
                if self.format_duration(t[5]) <= duration:
                    target_tks.append(t)
        else:
            for li in lines:
                for t in self.final_tks:
                    if li == t[0] and self.format_duration(t[5]) <= duration:
                        target_tks.append(t)
        return target_tks

    def _auto_check_tks(self, lines=None, duration=1000, ft=2):
        refresh_time = 1
        while not self.has_find_tks:
            print('已监控%d次' % refresh_time)
            target_tks = self.get_tk(lines, duration)
            if not self.origin_target_tks:
                self.origin_target_tks = target_tks
            for i1, s in enumerate(target_tks):
                print(s)
                if s not in self.origin_target_tks:
                    cur_tag_left = s[6]
                    ogn_tag_left = self.origin_target_tks[i1][6]
                    for i2, e in enumerate(ogn_tag_left):
                        if e == '无' and cur_tag_left[i2] != '无':
                            index = self.final_tks.index(target_tks[i1])
                            print('%s 线路有票》》》》》》》》》》》' % s[0])
                            self.has_find_tks = True
                            loop_time = 0
                            threading.Thread(target=self.auto_fire, args=(index,)).start()
                            while loop_time < 10:
                                pygame.mixer.music.play()
                                loop_time += 1
                                time.sleep(4)
            print('=============================================================================')
            print('')
            refresh_time += 1
            time.sleep(ft)

    def auto_check_tks(self, lines=None, duration=1000, ft=2):
        try:
            self._auto_check_tks(lines, duration, ft)
        except KeyboardInterrupt:
            pass

    def auto_fire(self, index):
        from selenium.common.exceptions import NoSuchElementException
        time.sleep(1)
        # print(index)
        # self.brw.find_elements_by_class_name('btn72')[index].click()
        # time.sleep(.5)
        while True:
            try:
                self.brw.find_elements_by_class_name('login-hd-account')[0].click()
                time.sleep(.5)
                self.brw.find_element_by_id('J-userName').send_keys('15350732361')
                self.brw.find_element_by_id('J-password').send_keys('137669LYR')
                break
            except Exception:
                pass

        # while self.brw.current_url == self.main_url:
        #     time.sleep(.5)
        while True:
            try:
                self.brw.find_element_by_id('normalPassenger_0').click()
                self.brw.find_element_by_id('normalPassenger_1').click()
                return
            except NoSuchElementException:
                pass
        # self.brw.find_element_by_id('submitOrder_id').click()

    def is_element_exists(self, e):
        from selenium.common.exceptions import NoSuchElementException
        try:
            self.brw.find_element_by_id(e)
            return True
        except NoSuchElementException:
            return False

    @staticmethod
    def format_duration(d):
        d = str(d).split(':')
        return float(d[0] + str(float(d[1]) / 60.0)[1:])


class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, '铁路余票监控', size=(800, 600))
        self.Centre()


class MyApp(wx.App):
    def OnInit(self):
        MyFrame().Show(True)
        return True

    def OnExit(self):
        sys.exit()


if __name__ == '__main__':
    t = Tools()
    t.auto_check_tks(duration=12)
