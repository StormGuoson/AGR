#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
#
"""
Module:Analyse Thread CPU&MEM and Plot

__author__ = "sunyujuan(sunyujuan@baidu.com)"
Date:    18/04/10
"""
import argparse
import os
import sys
from imp import reload

import matplotlib.pyplot as plt

reload(sys)
sys.setdefaultencoding('utf-8')


class MyThread(object):
    """
    MyThread class
    """

    def __init__(self, info_dir, thread_list):
        self.cur_dir = info_dir
        self.thread_list = thread_list

        if not os.path.isdir(self.cur_dir):
            print("%s is not found!")

        for file_name in os.listdir(self.cur_dir):
            if file_name.startswith("so"):
                self.so_file = os.path.join(self.cur_dir, file_name)

    def get_thread_data(self):
        """
        get threads cpu&mem
        :return: thread_data
        """
        thread_data = []
        for i in range(len(self.thread_list)):
            tmp_thread_data = {}
            tmp_data1 = []
            tmp_data2 = []
            if pattern == '0':
                tmp_data3 = []
                tmp_thread_data[self.thread_list[i] + '_mem_rss'] = tmp_data3
            tmp_thread_data[self.thread_list[i] + '_cpu'] = tmp_data1
            tmp_thread_data[self.thread_list[i] + '_mem'] = tmp_data2
            thread_data.append(tmp_thread_data)

        if os.path.exists(self.so_file):
            with open(self.so_file) as f:
                lines = f.readlines()
                for line in lines:
                    for i in range(len(self.thread_list)):
                        if line.find(self.thread_list[i]) != -1:
                            if pattern == '0':
                                current_cpu = line.strip().split()[5].strip('%')
                                current_mem = float(line.strip().split()[7].strip('K')) / 1024.0
                                current_mem_RSS = float(line.strip().split()[8].strip('K')) / 1024.0
                                thread_data[i][self.thread_list[i] + '_mem_rss'].append(current_mem_RSS)

                            else:
                                current_cpu = line.strip().split()[8]
                                current_mem = line.strip().split()[9]
                            thread_data[i][self.thread_list[i] + '_cpu'].append(current_cpu)
                            thread_data[i][self.thread_list[i] + '_mem'].append(current_mem)
                        else:
                            continue

        return thread_data

    def save_result(self, filename, content):
        """
        save
        :param filename:output file name
        :param content:saved content
        :return:null
        """
        with open(filename, "a+") as f:
            f.write(content)

    def calculate_avg(self, data):
        """
        calculate average cpu&mem
        :param data: all data
        :return: avg_data
        """
        avg_data = {}
        index = dirs.index(self.cur_dir)
        res_file_name = result_dir + '/per_result%s.txt' % str(index)
        if os.path.exists(res_file_name):
            os.remove(res_file_name)

        for i in range(len(data)):
            count = 0
            size = 0
            min = float(data[i][self.thread_list[i] + '_cpu'][0])
            max = float(data[i][self.thread_list[i] + '_cpu'][0])
            avg = 0
            for cpu_data in data[i][self.thread_list[i] + '_cpu']:
                count += float(cpu_data)
                size += 1
                if float(cpu_data) < min:
                    min = float(cpu_data)
                if float(cpu_data) > max:
                    max = float(cpu_data)

            if size != 0:
                avg = count / size

            avg_data[self.thread_list[i] + '_cpu'] = [avg, min, max]
            # print(self.thread_list[i] + '_cpu' + ':' + 'avg = ' + str(avg)
            #       + '   min = ' + str(min) + '   max = ' + str(max) + '\n')
            self.save_result(res_file_name, self.thread_list[i] + '_cpu' + ':' + 'avg = '
                             + str(avg) + '   min = ' + str(min) + '   max = ' + str(max) + '\n')
            count = 0
            size = 0
            min = float(data[i][self.thread_list[i] + '_mem'][0])
            max = float(data[i][self.thread_list[i] + '_mem'][0])
            avg = 0
            for mem_data in data[i][self.thread_list[i] + '_mem']:
                count += float(mem_data)
                size += 1
                if float(mem_data) < min:
                    min = float(mem_data)
                if float(mem_data) > max:
                    max = float(mem_data)

            if size != 0:
                avg = count / size

            avg_data[self.thread_list[i] + '_mem'] = [avg, min, max]
            # print(self.thread_list[i] + '_mem' + ':' + 'avg = ' + str(avg)
            #       + '   min = ' + str(min) + '   max = ' + str(max) + '\n')
            self.save_result(res_file_name, self.thread_list[i] + '_mem' + ':'
                             + 'avg = ' + str(avg) + '   min = ' + str(min) + '   max = ' + str(max) + '\n')
            # RSS 
            if pattern == '0':
                count = 0
                size = 0
                min = float(data[i][self.thread_list[i] + '_mem_rss'][0])
                max = float(data[i][self.thread_list[i] + '_mem_rss'][0])
                avg = 0
                for mem_rss_data in data[i][self.thread_list[i] + '_mem_rss']:
                    count += float(mem_rss_data)
                    size += 1
                    if float(mem_rss_data) < min:
                        min = float(mem_rss_data)
                    if float(mem_rss_data) > max:
                        max = float(mem_rss_data)

                if size != 0:
                    avg = count / size

                avg_data[self.thread_list[i] + '_mem_rss'] = [avg, min, max]
                # print(self.thread_list[i] + '_mem_rss' + ':' + 'avg = ' + str(avg)
                #       + '   min = ' + str(min) + '   max = ' + str(max) + '\n')
                self.save_result(res_file_name, self.thread_list[i] + '_mem_rss' + ':'
                                 + 'avg = ' + str(avg) + '   min = ' + str(min) + '   max = ' + str(max) + '\n')

        return avg_data

    def plot_performance(self, data, avg_data):
        """
        plot
        :param data: all data
        :param avg_data: average data
        :return: null
        """
        if pattern == '0':
            for i in range(len(self.thread_list)):
                cpu_data = data[i][self.thread_list[i] + '_cpu']
                mem_data = data[i][self.thread_list[i] + '_mem']
                mem_rss_data = data[i][self.thread_list[i] + '_mem_rss']
                plt.plot(cpu_data, label=self.thread_list[i] + '_cpu')
                plt.plot(mem_data, label=self.thread_list[i] + '_mem_vss')
                plt.plot(mem_rss_data, label=self.thread_list[i] + '_mem_rss')
                info = 'cpu=' + str(round(avg_data[self.thread_list[i] + '_cpu'][0], 2)) \
                       + '  mem_vss=' + str(round(avg_data[self.thread_list[i] + '_mem'][0], 2)) \
                       + '  mem_rss=' + str(round(avg_data[self.thread_list[i] + '_mem_rss'][0], 2))
                plt.text(0, cpu_data[0], info)
            # plt.legend(loc=0, numpoints=1)
            # leg = plt.gca().get_legend()
            # ltext = leg.get_texts()
            # plt.setp(ltext, fontsize='small')
            # plt.title(self.result_dir + 'report')
            # plt.xlabel('x')
            # plt.ylabel('% / ')
            # plt.grid()
            # # plt.show()
            # picture_name = self.result_dir + '/report.jpg'
            # plt.savefig(picture_name)

        else:
            for i in range(len(self.thread_list)):
                cpu_data = data[i][self.thread_list[i] + '_cpu']
                mem_data = data[i][self.thread_list[i] + '_mem']
                plt.plot(cpu_data, label=self.thread_list[i] + '_cpu')
                plt.plot(mem_data, label=self.thread_list[i] + '_mem')
                info = 'cpu=' + str(round(avg_data[self.thread_list[i] + '_cpu'][0], 2)) \
                       + '  mem=' + str(round(avg_data[self.thread_list[i] + '_mem'][0], 2))
                plt.text(0, cpu_data[0], info)
        plt.legend(loc=0, numpoints=1)
        leg = plt.gca().get_legend()
        ltext = leg.get_texts()
        plt.setp(ltext, fontsize='small')
        index = dirs.index(self.cur_dir)
        plt.title(titles[index + 1])
        plt.xlabel('x')
        plt.ylabel('%')
        plt.grid()
        # plt.show()
        picture_name = result_dir + '/report%s.jpg' % str(index)
        plt.savefig(picture_name)
        plt.close()

    def get(self):
        """
        start analyse
        :return: True or False
        """
        try:
            data = self.get_thread_data()
            avg_data = self.calculate_avg(data)
            self.plot_performance(data, avg_data)
        except Exception as e:
            print("Exception: %s" % str(e))
            return False
        return True


def save2html():
    pic_dirs = ''
    for i in range(len(dirs)):
        pic_dirs += format_img('report%s.jpg' % str(i))

    with open(os.path.join(result_dir, 'report.html'), 'w') as f:
        f.write(body(format_table(), pic_dirs))


def mix_txt_results():
    format_lists = []
    ress = []
    l = len(dirs)
    for i in range(l):
        with open(os.path.join(result_dir, 'per_result%s.txt' % str(i))) as f:
            tmp = []
            lines = f.readlines()
            for line in lines:
                single = [line[line.find('avg = ') + 6:line.find('   min')],
                          line[line.find('min = ') + 6:line.find('   max')],
                          line[line.find('max = ') + 6:-1]]
                tmp.append(single)
            ress.append(tmp)
    if pattern == '0':
        y = len(THREAD_LIST) * 3
    else:
        y = len(THREAD_LIST) * 2
    for i in range(y):
        tmp = []
        for n in range(l):
            tmp += ress[n][i]
        format_lists.append(tmp)
    return format_lists


def format_table_titles():
    res = '''<th rowspan=2>NAME</th>
    '''
    for i in range(len(dirs)):
        res += '''<th colspan=3>%s</th>
        ''' % titles[i + 1]
    return res


def get_table_name(i):
    total = []
    if pattern == '0':
        for t in THREAD_LIST:
            total.append('<td>%s_cpu</td>' % t)
            total.append('<td>%s_mem</td>' % t)
            total.append('<td>%s_mem_rss</td>' % t)
    else:
        for t in THREAD_LIST:
            total.append('<td>%s_cpu</td>' % t)
            total.append('<td>%s_mem</td>' % t)
    return total[i]


def format_table_ele():
    total = '''<tr>'''
    for i in range(len(dirs)):
        total += '''<td align="center">均值</td>
        <td align="center">最小值</td>
        <td align="center">最大值</td>'''
    total += '''</tr>'''
    mtr = mix_txt_results()
    if pattern == '0':
        count = len(THREAD_LIST) * 3
    else:
        count = len(THREAD_LIST) * 2
    for i in range(count):
        total += '''<tr>
           '''
        total += get_table_name(i)
        for i2 in range(len(dirs) * 3):
            total += '''<td align="center">%s</td>
            ''' % save_percent(mtr[i][i2])
        total += '</tr>'
    return total


def format_table():
    if len(dirs) == 1:
        per = '40%'
    else:
        per = '85%'
    res = '''
    <div class="Column" align="center" >
    <table border="1" width=%s cellspacing="0" cellpadding="5">
        <tr>
            %s
        </tr>
        %s
    </table>
    </div>''' % (per, format_table_titles(), format_table_ele())

    return res + ''


def format_img(_dir):
    if len(dirs) == 1:
        per = '50%'
    else:
        per = '100%'
    return '<div class="Column" align="center"><img src="%s" alt="main_img" width=%s> </div>' % (_dir, per)


def save_percent(i):
    return str(round(float(i), 2))


def body(table, img):
    r = '''
    <!DOCTYPE html>
    <html>
        <head>
            <style>
                .Row
                    {
                        display: table;
                        width: %s; /*Optional*/
                        table-layout: fixed; /*Optional*/
                        border-spacing: 10px; /*Optional*/
                    }
                .Column
                    {
                        display: table-cell;
                    }
            </style>
            <meta charset="utf-8">
            <title>测试报告</title>
        </head>
    <body>
        <h1 align="center">%s</h1>
        <div class="Row">
        %s
        </div>
        <div class="Row">
        %s
        </div>
    </body>
    </html>''' % ('100%', titles[0], table, img)
    return r


def init_parse():
    parser = argparse.ArgumentParser(description='this is a description')
    parser.add_argument('-d', '--dir', help='测试文件夹主目录', required=True)
    parser.add_argument('-s', '--style', help='设备类型：0为创维,1为华为', required=True)
    parser.add_argument('-t', '--title', help='输入一个字符串,生成html标题', required=True)
    arg = parser.parse_args()
    return arg


def main():
    global dirs, result_dir
    # 将路径添加到dirs
    t = []
    for d in os.listdir(home_dir):
        d = os.path.join(home_dir, d)
        if os.path.isdir(d):
            t.append(d)
    dirs = sorted(t)
    # 创建结果路径
    result_dir = os.path.join(home_dir, 'result')
    if not os.path.exists(result_dir):
        os.mkdir(result_dir)
    # start
    for d in dirs:
        print(d)
        title = d[d.rfind(os.sep) + 1:].split('_')[1]
        titles.append(title)
        thread = MyThread(d, THREAD_LIST)
        thread.get()
        # retcode = 0 if ret else 1
    save2html()
    sys.exit()


if __name__ == '__main__':
    # 存放结果路径
    result_dir = ''
    # 文件信息存放路径
    dirs = []
    titles = []
    args = init_parse()
    home_dir = args.dir
    pattern = args.style
    titles.append(args.title)
    THREAD_LIST = ["spil_cap",'gsc_thread']
    main()
