# -*- coding: utf-8-*-
import ast
import os
import queue
import subprocess
import threading
import time

import psutil as psutil
from pykeyboard import PyKeyboard

k = PyKeyboard()
Queue = queue
L = threading.Lock()


def set_clipboard_text(t):
    p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
    p.stdin.write(t.encode('utf-8'))
    p.stdin.close()
    p.communicate()


def paste():
    k.press_key('Command')
    k.tap_key('v')
    time.sleep(0.03)
    k.release_key('Command')


def click(n):
    time.sleep(.03)
    k.tap_key(n)
    time.sleep(.03)


def auto_set(_text, _sn):
    global L
    if only_wakeup:
        return
    L.acquire()
    try:
        _as(_text, _sn)
    except Exception as e:
        print(repr(e))
    L.release()


def _as(_text, _sn):
    print(_text + '\r')
    print(_sn + '\r')
    for d in range(len(ACTIVE_DEVICES)):
        d = str(d)
        if ('text' + d) not in DATA:
            return
        if DATA['text' + d] == '':
            return
    for s in range(len(ACTIVE_DEVICES)):
        s = str(s)
        set_clipboard_text(DATA['text' + s])
        paste()
        time.sleep(0.03)
        click('Tab')
        time.sleep(0.03)
        set_clipboard_text(DATA['sn' + s])
        time.sleep(0.03)
        paste()
        time.sleep(0.03)
        if int(s) == len(ACTIVE_DEVICES) - 1:
            click('Return')
            time.sleep(0.03)
        else:
            click('Tab')
            time.sleep(0.03)
        # for e in range(len(ACTIVE_DEVICES)):
        #     k.press_key('Shift')
        #     click("Tab")
        #     k.release_key('Shift')
        #     time.sleep(0.03)
        #     if int(e) != len(ACTIVE_DEVICES) - 1:
        #         k.press_key('Shift')
        #         click("Tab")
        #         k.release_key('Shift')
        #         time.sleep(0.03)
    if write_rec:
        msg = ''
        for s in range(len(ACTIVE_DEVICES)):
            msg += DATA['text' + str(s)] + '\t' + DATA['sn' + str(s)]
            if s + 1 != len(ACTIVE_DEVICES):
                msg += '\t'
        save_memory(SAVE_RESULTS, msg + '\r')

    for d in range(len(ACTIVE_DEVICES)):
        d = str(d)
        DATA['text' + d] = DATA['sn' + d] = ''


only_wakeup = False
write_rec = False
SAVE_RESULTS = r'~/Desktop/res.log'
SAVE_AUDIO = r'~/Desktop/audio'
td = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

ACTIVE_DEVICES = []  # 激活的设备
DEVICES_ORDERED = []  # 设备的连接顺序
UNACTIVE_DEVICES = []  # 休眠的设备
CURRENT_MODULE = 0  # 当前模式
ACTIVE_MODULES = [-1, -1, -1, -1, -1]  # 各设备的模式

MOD_AINEMO_LAUNCHER = '小度在家'
MOD_AINEMO_DEMO = '小度在家demo'
MOD_CW_LAUNCHER = '小维AI'
MOD_CW_DEMO = '创维demo'
MOD_HUAWEI_LAUNCHER = '华为'
MOD_HUAWEI_DEMO = '华为demo'
MOD_CW_SHOW = '创维show'
MOD_Max = 'Max'
MOD_XIAODUBOX = '小度音箱'
MOD_XGP = '小钢炮'

MOD_CW_SHOW_DEMO = '创维show—demo'

DATA = {}


def select_mod(_index=-1):
    if _index == -1:
        return 11

    if _index == 0:
        return MOD_AINEMO_LAUNCHER
    if _index == 1:
        return MOD_AINEMO_DEMO
    if _index == 2:
        return MOD_CW_LAUNCHER
    if _index == 3:
        return MOD_CW_DEMO
    if _index == 4:
        return MOD_HUAWEI_LAUNCHER
    if _index == 5:
        return MOD_HUAWEI_DEMO
    if _index == 6:
        return MOD_CW_SHOW
    if _index == 7:
        return MOD_Max
    if _index == 8:
        return MOD_XIAODUBOX
    if _index == 9:
        return MOD_XGP
    if _index == 10:
        return MOD_CW_SHOW_DEMO


def show_mods():
    for i in range(select_mod()):
        print('%d.%s' % (i, select_mod(i)))


def write_wakeup(no):
    L.acquire()
    for d in range(len(ACTIVE_DEVICES)):
        d = str(d)
        DATA['text' + d] = DATA['sn' + d] = ''
    if ('wakeup_count' + no) in DATA:
        DATA['wakeup_count' + no] += 1
    else:
        DATA['wakeup_count' + no] = 1
    # if len(arg) > 0:
    #     txt.txt_log.write(
    #         str(ACTIVE_DEVICES[int(no)]) + u' 唤醒次数 ' + str(DATA['wakeup_count' + no]) + '_' + str(arg[0]) + '\r')
    #
    # elif ('wakeup_angle' + no) in DATA:
    #     txt.txt_log.write(str(ACTIVE_DEVICES[int(no)]) + u' 唤醒次数 ' + str(DATA['wakeup_count' + no]) + '_' + DATA[
    #         'wakeup_angle' + no] + '\r')
    # else:
    #     txt.txt_log.write(str(ACTIVE_DEVICES[int(no)]) + u' 唤醒次数 ' + str(DATA['wakeup_count' + no]) + '\r')
    print(ACTIVE_DEVICES[int(no)] + ' 唤醒次数: ' + str(DATA['wakeup_count' + no]))
    L.release()


class MODULE(object):
    def __init__(self):
        pass

    def main_doing(self, _line, _module, no):
        if _module == MOD_CW_DEMO:
            self.module_chuangwei_demo(_line, no)
        elif _module == MOD_CW_LAUNCHER:
            self.module_chuangwei_launcher(_line, no)
        elif _module == MOD_HUAWEI_LAUNCHER:
            self.module_huawei_launcher(_line, no)
        elif _module == MOD_AINEMO_LAUNCHER:
            self.module_ainemo(_line, no)
        elif _module == MOD_AINEMO_DEMO:
            self.module_ainemo_demo(_line, no)
        elif _module == MOD_HUAWEI_DEMO:
            self.module_huawei2(_line, no)
        elif _module == MOD_CW_SHOW:
            self.module_cw_show(_line, no)
        elif _module == MOD_CW_SHOW_DEMO:
            self.module_cw_show_demo(_line, no)
        elif _module == MOD_XGP:
            self.module_xgp(_line, no)
        elif _module == MOD_XIAODUBOX:
            self.module_xdbox(_line, no)
        elif _module == MOD_Max:
            self.module_max(_line, no)

    # 创维demo识别
    @staticmethod
    def module_chuangwei_demo(line, no):
        # if line.find('wakeup_time') != -1:
        #     write_wakeup( no)
        # if line.find("ASREngine") != -1 and line.find('origin_result') != -1 and line.find('corpus_no') != -1:
        #     line = ast.literal_eval(line[line.find('{'):])
        #     corpus = str(line['origin_result']['corpus_no'])
        #     DATA['sn' + no] = corpus
        # elif line.find('--final') != -1:
        #     text = line[line.find('final: ') + 7: -1]
        #     DATA['text' + no] = text
        #     auto_set(text, DATA['sn' + no])
        # elif line.find('wakeup_time') != -1 and line.find('result') != -1:
        #     write_wakeup(no)
        if line.find('final_result') != -1 and line.find('sn') != -1:
            line = ast.literal_eval(line[line.find('{'):])
            text = line['results_recognition'][0]
            sn = line['origin_result']['sn']
            corpus = str(line['origin_result']['corpus_no'])
            DATA['sn' + no] = sn + "_" + corpus
            DATA['text' + no] = text
            auto_set(text, sn)

    # 创维launcher识别
    @staticmethod
    def module_chuangwei_launcher(line, no):
        if line.find('wakeup_time') != -1:
            write_wakeup(no)
        elif line.find("BDSHttpRequestMaker") != -1 and line.find("response") != -1 and line.find(
                'sn') != -1 and line.find('result') != -1:
            line = line[line.find('{'):line.rfind('}') + 1]
            line = ast.literal_eval(line)
            sn = line["sn"]
            corpus = str(line['corpus_no'])
            if 'osn' not in DATA:
                DATA['osn'] = ''
            if sn != DATA['osn']:
                DATA['osn'] = sn
                DATA['sn' + no] = sn + '_' + corpus
                print(sn)
        elif line.find("onFinalReconnition") != -1:
            text = line[line.rfind(':') + 2:line.find('type') - 1]
            # DATA['sn'] += '_' + str(DATA['wakeup_angle'])
            DATA['text' + no] = text
            print(DATA['text' + no])
            print('')
            auto_set(DATA['text' + no], DATA['sn' + no])

    # 华为产品包 识别
    @staticmethod
    def module_huawei_launcher(line, no):
        if line.find('SpeechCallback') != -1 and line.find('wakeup_time') != -1:
            write_wakeup(no)
            # if debug_mode:
            #     threading.Thread(target=lambda: time.sleep(.5)).start()
            #     threading.Thread(
            #         target=lambda: os.popen('adb -s %s shell input tap 300 300' % ACTIVE_DEVICES[int(no)]).close()).start()

        elif line.find(u'SpeechCallback') != -1 and line.find('final_result') != -1 and line.find('corpus') != -1:
            # print line
            line = ast.literal_eval(line[line.find('{'):])
            DATA['text' + no] = line['best_result']
            DATA['sn' + no] = line['origin_result']['sn'] + '_' + str(line['origin_result']['corpus_no'])
            auto_set(DATA['text' + no], DATA['sn' + no])

    # 小鱼识别
    @staticmethod
    def module_ainemo(line, no):
        if line.find('wakeup_time') != -1 and line.find('SpeechCallback') != -1:
            write_wakeup(no)
            if only_wakeup:
                os.popen('adb -s %s shell input tap 400 400' % ACTIVE_DEVICES[int(no)]).close()
        elif line.find("SpeechCallback") != -1 and line.find("final") != -1:
            line = line[line.find('{'):]
            line = ast.literal_eval(line)
            text = line['best_result']
            sn = line['origin_result']['sn']
            corpus = str(line['origin_result']['corpus_no'])
            DATA['sn' + no] = sn + '_' + corpus
            DATA['text' + no] = text
            auto_set(DATA['text' + no], DATA['sn' + no])

    @staticmethod
    def module_ainemo_demo(line, no):
        if line.find('wakeup_time') != -1 and line.find('result') != -1:
            write_wakeup(no)
        # elif line.find("DCS-AsrEngine") != -1 and line.find('logid') != -1:
        #     logid = line[line.find('logid') + 8:line.find('client_ip') - 3]
        #     print logid
        #     DATA['sn' + no] = logid
        elif line.find('final') != -1:
            line = ast.literal_eval(line[line.find('{'):])
            text = line['results_recognition'][0]
            sn = line['origin_result']['sn']
            corpus = str(line['origin_result']['corpus_no'])
            DATA['text' + no] = text
            DATA['sn' + no] = sn + '_' + corpus
            auto_set(DATA['text' + no], DATA['sn' + no])

    # 华为demo
    @staticmethod
    def module_huawei2(line, no):
        if line.find('wakeup_time') != -1 and line.find('result') != -1:
            write_wakeup(no)
        elif line.find('Final result:') != -1:
            line = ast.literal_eval(line[line.find('{'):])
            DATA['text' + no] = line['results_recognition'][0]
            DATA['sn' + no] = line['origin_result']['sn'] + '_' + str(line['origin_result']['corpus_no'])
            auto_set(DATA['text' + no], DATA['sn' + no])

    # 创维show
    @staticmethod
    def module_cw_show(line, no):
        if line.find("wakeup_time") != -1 and line.find("result") != -1:
            write_wakeup(no)
        elif line.find('final_result') != -1 and line.find('SpeechCallback') != -1:
            line = ast.literal_eval(line[line.find('{'):])
            text = line['results_recognition'][0]
            corpus = str(line['origin_result']['corpus_no'])
            sn = line['origin_result']['sn']
            DATA['text' + no] = text
            DATA['sn' + no] = sn + '_' + corpus
            auto_set(DATA['text' + no], DATA['sn' + no])

    @staticmethod
    def module_cw_show_demo(line, no):
        # if line.find('BDSHttpRequestMaker') != -1 and line.find('corpus_no') != -1 and line.find('response') != -1:
        #     line = line[line.find('{'):line.rfind('}') + 1]
        #     line = ast.literal_eval(line)
        #     sn = line["sn"]
        #     corpus = str(line['corpus_no'])
        #     if 'osn' not in DATA:
        #         DATA['osn'] = ''
        #     if sn != DATA['osn']:
        #         DATA['osn'] = sn
        #         DATA['sn' + no] = sn + '_' + corpus
        if line.find("EventManagerAsr") != -1 and line.find("final") != -1:
            line = ast.literal_eval(line[line.find('{'):])
            text = line['best_result']
            sn = line['origin_result']['sn']
            corpus = str(line['origin_result']['corpus_no'])
            DATA['text' + no] = text
            DATA['sn' + no] = sn + '_' + corpus
            auto_set(DATA['text' + no], DATA['sn' + no])
        elif line.find('wakeup_time') != -1 and line.find('SpeechCallback') != -1:
            write_wakeup(no)
        elif line.find('qyq_plugin') != -1 and line.find('FINAL') != -1:
            line = ast.literal_eval(line[line.find('{'):line.rfind('}') + 1])
            text = line['payload']['text']
            DATA['text' + no] = text
            auto_set(DATA['text' + no], DATA['sn' + no])
        elif line.find("BDSHttpRequestMaker") != -1 and line.find('corpus_no') != -1:
            line = line[line.find('{'):]
            line = ast.literal_eval(line)
            sn = line['sn']
            corpus_no = str(line['corpus_no'])
            if 'osn' not in DATA:
                DATA['osn'] = ''
            if sn != DATA['osn']:
                DATA['osn'] = sn
                DATA['sn' + no] = sn + '_' + corpus_no

    def module_xgp(self, line, no):
        self.module_xdbox(line, no)

    @staticmethod
    def module_xdbox(line, no):
        # 小钢炮
        if 'wakeup trigger' in line:
            write_wakeup(no)
        elif 'kwd_detect' in line:
            write_wakeup(no)
        elif ('Final result' in line and 'results_recognition' in line) or 'result=asr' in line:
            line = ast.literal_eval(line[line.find('{'):line.rfind('}') + 1])
            text = line['results_recognition'][0]
            corpus = str(line['origin_result']['corpus_no'])
            sn = line['origin_result']['sn']
            DATA['text' + no] = text
            DATA['sn' + no] = sn + '_' + corpus
            auto_set(DATA['text' + no], DATA['sn' + no])
        elif 'asr finish' in line or ('Final result' in line and 'results_recognition' not in line):
            line = ast.literal_eval(line[line.find('{'):])
            text = line['result']['word'][0]
            corpus = str(line['corpus_no'])
            sn = line['sn']
            DATA['text' + no] = text
            DATA['sn' + no] = sn + "_" + corpus
            auto_set(DATA['text' + no], DATA['sn' + no])

        # audio:
        # if line.find('kwd_detect') != -1:
        #     write_wakeup(no)
        # elif line.find('Final result') != -1:
        #     line = ast.literal_eval(line[line.find('{'):])
        #     text = line['result']['word'][0]
        #     corpus = str(line['corpus_no'])
        #     sn = str(line['sn'])
        #     DATA['text' + no] = text
        #     DATA['sn' + no] = sn + "_" + corpus
        #     auto_set(DATA['text' + no], DATA['sn' + no])
        # 度秘
        # if 'wakeup trigger' in line:
        #     write_wakeup(no)
        # elif 'finish content' in line:
        #     line = ast.literal_eval(line[line.find('{'):])
        #     text = line['result']['word'][0]
        #     corpus = str(line['corpus_no'])
        #     sn = line['sn']
        #     DATA['text' + no] = text
        #     DATA['sn' + no] = sn + '_' + corpus
        #     auto_set(DATA['text' + no], DATA['sn' + no])

    @staticmethod
    def module_max(line, no):
        if 'wakeup_time' in line and 'Activity04WakeupAndASR' in line:
            write_wakeup(no)
        elif u'SpeechCallback' in line and 'final_result' in line:
            line = ast.literal_eval(line[line.find('{'):])
            text = line['results_recognition'][0]
            corpus = line['origin_result']['corpus_no']
            sn = line['origin_result']['sn']
            DATA['text' + no] = text
            DATA['sn' + no] = sn + '_' + str(corpus)
            auto_set(DATA['text' + no], DATA['sn' + no])


class AsynchronousFileReader(threading.Thread):
    """
    Helper class to implement asynchronous reading of a file
    in a separate thread. Pushes read lines on a queue to
    be consumed in another thread.
    """

    def __init__(self, fd, queue):
        assert isinstance(queue, Queue.Queue)
        assert callable(fd.readline)
        threading.Thread.__init__(self)
        self._fd = fd
        self._queue = queue

    def run(self):
        """The body of the tread: read lines and put them on the queue."""
        for line in iter(self._fd.readline, ''):
            self._queue.put(line)

    def eof(self):
        """Check whether there is no more content to expect."""
        return not self.is_alive() and self._queue.empty()


def kill_self():
    print('\n\033[1;31m=======停止=======\033[0m')
    pids = psutil.pids()
    for pid in pids:
        if psutil.Process(pid).name() == 'Python':
            psutil.Process(pid).kill()


def consume(command, no):
    """
    Example of how to consume standard output and standard error of
    a subprocess asynchronously without risk on deadlocking.
    """
    print(command)
    global L
    time.sleep(float(no) / 10.0 * 3)
    td[int(no)] = time.time()
    # Launch the command as subprocess.
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               shell=True)
    # Launch the asynchronous readers of the process' stdout and stderr.
    stdout_queue = Queue.Queue()
    stdout_reader = AsynchronousFileReader(process.stdout, stdout_queue)
    stdout_reader.start()
    stderr_queue = Queue.Queue()
    stderr_reader = AsynchronousFileReader(process.stderr, stderr_queue)
    stderr_reader.start()
    # Check the queues if we received some output (until there is nothing more to get).
    # frame.txt_log.write(('No%s_' % str(int(no) + 1)) + ACTIVE_DEVICES[int(no)] + u' <<<开始>>>' + '\r')
    print(('No%s_' % str(int(no) + 1)) + ACTIVE_DEVICES[int(no)] + u' <<<开始>>>' + '\r')
    mod = MODULE()
    while not stdout_reader.eof() or not stderr_reader.eof():
        while not stdout_queue.empty():
            line = stdout_queue.get().decode("utf-8", errors="ignore")
            try:
                mod.main_doing(line, CURRENT_MODULE, no)
            except Exception as e:
                print('\033[1;31m错误: ' + repr(e) + '\033[0m')
                # frame.txt_log.write(repr(e))
        while not stderr_queue.empty():
            line = stderr_queue.get().decode('utf-8')
            if 'has been replaced' in line:
                print(repr(line))
                continue
            print('\033[1;31m错误: 设备-' + ACTIVE_DEVICES[int(no)] + repr(line) + '\033[0m')
            kill_self()
        # Sleep a bit before asking the readers again.
        try:
            time.sleep(.1)
        except KeyboardInterrupt:
            pass
    kill_self()
    # Let's be tidy and join the threads we've started.
    # stdout_reader.join()
    # stderr_reader.join()
    # Close subprocess' file descriptors.
    # process.stdout.close()
    # process.stderr.close()
    # process.kill()
    # kill_self()


def save_memory(filename, _content):
    mp = str(filename[:filename.rfind('\\')])
    if not os.path.exists(mp):
        os.makedirs(mp)
    with open(filename.decode(), "a+") as f:
        f.write(_content)


def get_device_list():
    global UNACTIVE_DEVICES, DEVICES_ORDERED
    device_sn_list = []
    UNACTIVE_DEVICES = []
    m_file = os.popen("adb devices")
    for line in m_file.readlines():
        # line = line.encode('utf-8')
        if line.find("List of devices attached") != -1 or line.find('start') != -1 or line.find('daemon') != -1:
            continue
        elif len(line) > 5:
            device_sn_list.append(line.split("\t")[0])
            UNACTIVE_DEVICES.append(line.split("\t")[0])
    m_file.close()
    if len(device_sn_list) == 1:
        DEVICES_ORDERED.append(0)
    return device_sn_list


class ThreadLogcat(threading.Thread):
    fm = ''

    def __init__(self, dev):
        threading.Thread.__init__(self)
        self.dev = dev
        self.start()

    def run(self):
        global DATA
        DATA = {}
        # _start_d = get_device_list()[CURRENT_DEVICE]
        _d = ACTIVE_DEVICES[self.dev]
        if CURRENT_MODULE == MOD_XIAODUBOX:
            consume('ssh root@%s tail -F /tmp/speechsdk.log' % _d, str(self.dev))
        elif CURRENT_MODULE == MOD_XGP:
            consume('adb -s %s shell tail -F /tmp/speechsdk.log' % _d, str(self.dev))
        else:
            os.popen('adb -s %s logcat -c' % _d).close()
            consume("adb -s %s logcat -v time" % _d, str(self.dev))


class Tools(threading.Thread):
    pull = 0
    restart = 1
    reboot = 2

    def __init__(self, command):
        threading.Thread.__init__(self)
        self.command = command

    def run(self):
        if self.command == self.pull:
            self.__pull_audio()
        elif self.command == self.restart:
            self.__restart_app()
        elif self.command == self.__reboot_dev:
            self.__reboot_dev()

    def __pull_audio(self):
        pass

    def __restart_app(self):
        pass

    def __reboot_dev(self):
        pass


def start_app():
    global only_wakeup, CURRENT_MODULE
    only_wakeup = False
    show_mods()
    try:
        mod = input('\033[1;36m请选择设备类型：\033[0m')
        CURRENT_MODULE = select_mod(int(mod))
        print('\033[1;34m当前模式：' + CURRENT_MODULE + '\033[0m')
        if CURRENT_MODULE != MOD_XIAODUBOX:
            dev = get_device_list()
            print(dev)
            order = input('\033[1;36m请输入设备连接顺序,以空格区分(0为起始)\033[0m\n').split(' ')
        else:
            ips = input('\033[1;36m顺序输入设备ip，以逗号分割\033[0m\n')
            dev = ips.split(',')
            order = [i for i in range(len(dev))]
        for o in order:
            ACTIVE_DEVICES.append(dev[int(o)])
        for i in range(len(ACTIVE_DEVICES)):
            ThreadLogcat(i)
    except Exception:
        os.popen('clear').close()
        print('\033[1;31m错误:输入不合法！！！重新输入 \033[0m')
        start_app()


if __name__ == '__main__':
    try:
        start_app()
    except KeyboardInterrupt:
        print('\n\033[1;31m=======停止=======\033[0m')
