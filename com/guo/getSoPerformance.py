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
import os
import sys

import matplotlib.pyplot as plt


class MyThread(object):
    """
    MyThread class
    """

    def __init__(self, result_dir, thread_list):
        self.result_dir = result_dir
        self.thread_list = thread_list

        if not os.path.isdir(self.result_dir):
            print("%s is not found!")

        for file_name in os.listdir(self.result_dir):
            if file_name.startswith("so"):
                self.so_file = os.path.join(self.result_dir, file_name)

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
        res_file_name = self.result_dir + '/per_result.txt'
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
        # plt.title(self.result_dir + 'report')
        plt.xlabel('x')
        plt.ylabel('%')
        plt.grid()
        # plt.show()
        picture_name = self.result_dir + '/report.jpg'
        plt.savefig(picture_name)

    def get(self):
        """
        start analyse
        :return: True or False
        """
        try:
            data = self.get_thread_data()
            avg_data = self.calculate_avg(data)
            self.plot_performance(data, avg_data)
            self.save2html()
        except Exception as e:
            print("Exception: %s" % str(e))
            return False
        return True

    def save2html(self):
        pic_dir = 'report.jpg'

        with open(self.result_dir + '/per_result.txt', 'r') as f:
            results = f.readlines()

        with open(self.result_dir + '/report.html', 'w') as f:
            f.write(self.body(self.result_dir, self.format_result(results), pic_dir))

    def format_result(self, result):
        res = ''
        for line in result:
            single = [line[:line.find(':')],
                      line[line.find('avg = ') + 6:line.find('   min')],
                      line[line.find('min = ') + 6:line.find('   max')],
                      line[line.find('max = ') + 6:-1]]
            res += '''<tr>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
                    </tr>''' % (
                single[0], self.save_percent(single[1]), self.save_percent(single[2]),
                self.save_percent(single[3]))
        return res

    @staticmethod
    def save_percent(i):
        return str(round(float(i), 2)) + '%'

    @staticmethod
    def body(title, txt, img=None):
        r = '''
<!DOCTYPE html>
    <html>
        <head>
            <meta charset="utf-8">
            <title>%s</title>
        </head>
    <body>
        <table border="1" align="center" cellspacing="0" cellpadding="5">
            <caption>Monthly savings</caption>
            <tr>
                <th>NAME</th>
                <th>AVG</th>
                <th>MIN</th>
                <th>MAX</th>
            </tr>
            %s
        </table>
        <div align="center">
            <img src="%s" alt="main_img" width="640" height="480"> 
        </div>
    </body>
    </html>''' % (title, txt, img)
        return r


def main():
    for d in os.listdir(result_dir):
        if os.path.isdir(d):
            dirs.append(d)
    ds = sorted(dirs)
    for d in ds:
        print(d)
        thread = MyThread(d, THREAD_LIST)
        thread.get()
        # retcode = 0 if ret else 1
    sys.exit()


if __name__ == '__main__':
    """
        pattern:输入 0 或 1。（0为创维，1为华为）
    """
    if len(sys.argv) != 3:
        print("Usage: python getSoPerformance.py deviceIP 0/1(0为创维，1为华为)")
        sys.exit(1)
    dirs = []
    result_dir = sys.argv[1]
    deviceIP = sys.argv[1]
    pattern = sys.argv[2]
    THREAD_LIST = ["gsc_thread", "spil_cap"]
    main()
