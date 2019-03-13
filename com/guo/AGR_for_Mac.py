# -*- coding: utf-8-*-
import ast
import os
import queue
import subprocess
import sys
import threading
import time

import psutil as psutil
from pykeyboard import PyKeyboard

k = PyKeyboard()
Queue = queue
L = threading.Lock()


def set_clipboard_text(_t):
    p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
    p.stdin.write(_t.encode('utf-8'))
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
        t.save_memory(SAVE_RESULTS, msg + '\r')

    for d in range(len(ACTIVE_DEVICES)):
        d = str(d)
        DATA['text' + d] = DATA['sn' + d] = ''


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


only_wakeup = False
write_rec = False
stop_self = False
restart_self = False
SAVE_RESULTS = r'~/Desktop/res.log'
SAVE_AUDIO = r'~/Desktop/audio'
td = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

ACTIVE_DEVICES = []  # 激活的设备
DEVICES_ORDERED = []  # 设备的连接顺序
CURRENT_MODULE = ''  # 当前模式
ACTIVE_MODULES = [-1, -1, -1, -1, -1]  # 各设备的模式

MOD_AINEMO_LAUNCHER = '小度在家'
MOD_AINEMO_DEMO = '小度在家demo'
MOD_CW_LAUNCHER = '小维AI'
MOD_CW_DEMO = '创维demo'
MOD_HUAWEI_LAUNCHER = '华为'
MOD_HUAWEI_DEMO = '华为demo'
MOD_CW_BOX = '创维盒子'
MOD_Max = 'Max'
MOD_XIAODUBOX = '小度音箱'
MOD_XGP = '小钢炮'
MOD_CW_BOX_DEMO = '创维盒子demo'
MOD_AINEMO_1S = '小度在家1S'

DATA = {}


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
        elif _module == MOD_CW_BOX:
            self.module_cw_show(_line, no)
        elif _module == MOD_CW_BOX_DEMO:
            self.module_cw_show_demo(_line, no)
        elif _module == MOD_XGP:
            self.module_xgp(_line, no)
        elif _module == MOD_XIAODUBOX:
            self.module_xdbox(_line, no)
        elif _module == MOD_Max:
            self.module_max(_line, no)
        elif _module == MOD_AINEMO_1S:
            self.module_AINEMO_1S(_line, no)

    # 小度在家1S
    @staticmethod
    def module_AINEMO_1S(line, no):
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
            #         target=lambda: os.popen('adb -s %s shell input tap 300 300' %
            #         ACTIVE_DEVICES[int(no)]).close()).start()

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

    def __init__(self, fd, q):
        assert isinstance(q, Queue.Queue)
        assert callable(fd.readline)
        threading.Thread.__init__(self)
        self._fd = fd
        self._queue = q

    def run(self):
        """The body of the tread: read lines and put them on the queue."""
        for line in iter(self._fd.readline, ''):
            self._queue.put(line)

    def eof(self):
        """Check whether there is no more content to expect."""
        return not self.is_alive() and self._queue.empty()


def consume(command, no):
    """
    Example of how to consume standard output and standard error of
    a subprocess asynchronously without risk on deadlocking.
    """
    print(command)
    global L, stop_self
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
        if stop_self or restart_self:
            break
        while not stdout_queue.empty():
            line = stdout_queue.get().decode("utf-8", errors="ignore")
            try:
                mod.main_doing(line, CURRENT_MODULE, no)
            except Exception as e1:
                print('\033[1;31m错误: ' + repr(e1) + '\033[0m')
                # frame.txt_log.write(repr(e))
        while not stderr_queue.empty():
            line = stderr_queue.get().decode('utf-8')
            if 'has been replaced' in line or 'EOF' in line:
                # print(str(line))
                continue
            print('\033[1;31m错误: 设备-' + ACTIVE_DEVICES[int(no)] + str(line) + '\033[0m')
            stop_self = True
            break
        # Sleep a bit before asking the readers again.
        time.sleep(.1)
    process.kill()
    if no == '0':
        if stop_self:
            time.sleep(.5)
            t.kill_self()
        elif restart_self:
            print('\n\033[1;31m=======停止=======\033[0m')
            time.sleep(.3)
            start_main()
    # Let's be tidy and join the threads we've started.
    # stdout_reader.join()
    # stderr_reader.join()
    # Close subprocess' file descriptors.
    # process.stdout.close()
    # process.stderr.close()

    # process.kill()
    # kill_self()


def get_device_list():
    device_sn_list = []
    m_file = os.popen("adb devices")
    for line in m_file.readlines():
        # line = line.encode('utf-8')
        if line.find("List of devices attached") != -1 or line.find('start') != -1 or line.find('daemon') != -1:
            continue
        elif len(line) > 5:
            device_sn_list.append(line.split("\t")[0])
    m_file.close()
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


class Tools(object):

    def __init__(self):
        self.finish_count = 0

    def pull_audio(self, dir_name):
        self.finish_count = 0
        print('\033[1;36m音频导出中......\033[0m\n')
        dir_name = dir_name.split(' ')
        if len(dir_name) == 1:
            dir_name = 'audio'
        else:
            dir_name = dir_name[1]
        for dev in ACTIVE_DEVICES:
            p = sys.argv[0].split('/')
            save_path = '/%s/%s/Desktop/audio/%s/%s' % (p[1], p[2], dev, dir_name)
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            if CURRENT_MODULE in (MOD_AINEMO_DEMO, MOD_AINEMO_LAUNCHER):
                from_path = '/data/log/'
            elif CURRENT_MODULE in (MOD_AINEMO_1S,):
                from_path = 'mnt/sdcard/aud_rec/'
            elif CURRENT_MODULE in (MOD_HUAWEI_DEMO, MOD_HUAWEI_LAUNCHER, MOD_CW_LAUNCHER, MOD_CW_DEMO):
                from_path = '/data/local/tmp/aud_rec/'
            elif CURRENT_MODULE in (MOD_CW_BOX, MOD_CW_BOX_DEMO, MOD_Max):
                from_path = '/data/local/aud_rec/'
            else:
                print('\n\033[1;31m该设备不支持\033[0m')
                return
            cmd = 'adb -s %s pull %s %s' % (dev, from_path, save_path)
            threading.Thread(target=self.__pull, args=(cmd, dev)).start()

    def __pull(self, cmd, dev):
        sp = subprocess.Popen(cmd, shell=True,
                              stdout=subprocess.PIPE)
        for line in iter(sp.stdout.readline, 'b'):
            if b'No such file or directory' in line:
                print('\n\033[1;31m设备 %s 没有音频\033[0m' % dev)
                self.finish_count += 1
                break
            if line == b'':
                self.finish_count += 1
                break
            print(line, end='\r')
        if self.finish_count == len(ACTIVE_DEVICES):
            print('\033[1;36m\n导出完毕\033[0m\n')

    @staticmethod
    def restart_app():
        activities = {
            MOD_HUAWEI_LAUNCHER: 'com.baidu.launcher/com.baidu.duer.home.activity.HomeActivity',
            MOD_HUAWEI_DEMO: 'com.baidu.speech.demo/com.baidu.speech.demo.ActivityWakeupAndAsr',
            MOD_Max: 'com.baidu.muses.vera',
            MOD_AINEMO_LAUNCHER: 'vulture.app.home/vulture.app.home.HomeActivity',
            MOD_AINEMO_DEMO: 'com.baidu.speech.demo/com.baidu.speech.demo.ActivityMain',
            MOD_CW_BOX: 'com.baidu.muses.vera/none',
            MOD_AINEMO_1S: 'com.baidu.launcher/com.baidu.duershow.launcher.home.ui.activity.HomeActivity'
        }
        if CURRENT_MODULE in activities.keys():
            print('\033[1;36m重启APP\033[0m\n')
            for dev in ACTIVE_DEVICES:
                stop = 'adb -s %s shell am force-stop %s 2>/dev/null' % (dev, activities[CURRENT_MODULE].split('/')[0])
                start = 'adb -s %s shell am start %s 2>/dev/null' % (dev, activities[CURRENT_MODULE])
                os.popen(stop).close()
                os.popen(start).close()
        else:
            print('\n\033[1;31m该设备不支持\033[0m')

    @staticmethod
    def reboot_dev():
        print('\033[1;36m设备重启\033[0m\n')
        for dev in ACTIVE_DEVICES:
            if CURRENT_MODULE == MOD_XIAODUBOX:
                threading.Thread(target=lambda: os.popen('ssh root@%s reboot' % dev).close()).start()
            else:
                threading.Thread(target=lambda: os.popen('adb -s %s reboot' % dev).close()).start()

    @staticmethod
    def kill_self():
        print('\n\033[1;31m=======退出=======\033[0m')
        pids = psutil.pids()
        for pid in pids:
            if psutil.Process(pid).name() == 'Python':
                psutil.Process(pid).kill()

    @staticmethod
    def select_mod(_index=-1):
        if _index == -1:
            return 12

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
            return MOD_CW_BOX
        if _index == 7:
            return MOD_Max
        if _index == 8:
            return MOD_XIAODUBOX
        if _index == 9:
            return MOD_XGP
        if _index == 10:
            return MOD_CW_BOX_DEMO
        if _index == 11:
            return MOD_AINEMO_1S

    def show_mods(self):
        for i in range(self.select_mod()):
            print('%d.%s' % (i, self.select_mod(i)))

    @staticmethod
    def save_memory(filename, _content):
        mp = str(filename[:filename.rfind('\\')])
        if not os.path.exists(mp):
            os.makedirs(mp)
        with open(filename, "a+") as f:
            f.write(_content)


class InputWatcher(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def run(self):
        global stop_self, only_wakeup, restart_self
        while not stop_self and not restart_self:
            cmd = input()
            if cmd == 'c':
                DATA.clear()
                print('\033[1;36m唤醒次数归零\033[0m\n')
            elif cmd == 'q':
                stop_self = True
            elif cmd == 's':
                restart_self = True
            elif cmd == 'restart':
                t.restart_app()
            elif cmd == 'reboot':
                restart_self = True
                t.reboot_dev()
            elif cmd.startswith('p'):
                t.pull_audio(cmd)
            elif cmd == 'w':
                if only_wakeup:
                    only_wakeup = False
                    print('\033[1;36m唤醒模式关闭\033[0m\n')

                else:
                    only_wakeup = True
                    print('\033[1;36m唤醒模式开启\033[0m\n')


def show_help():
    os.system('clear')
    mhelp = '''选好设备类型、设备连接顺序后可进行导音频、重启等操作,在终端中输入指令后按回车键即可
    
    输入 w        :切换唤醒/识别模式
    输入 c        :归零唤醒次数
    输入 reboot   :重启设备
    输入 restart  :重启APP
    输入 q        :退出程序
    输入 s        :停止logcat并回到选择界面
    输入 p [name] :导音频至'~/Desktop/audio/deviceSN/name'下，'deviceSN'为设备号，
                        name缺省值为'audio'，支持多台设备音频同时导出
    
百度Hi：郭玉强
\033[1;36m按回车键继续\033[0m
    '''
    print(mhelp)
    input()
    os.system('clear')
    start_main()


def start_main():
    global only_wakeup, CURRENT_MODULE, stop_self, restart_self
    ACTIVE_DEVICES.clear()
    stop_self = restart_self = False
    only_wakeup = False
    t.show_mods()
    print('输入 h 查看帮助')
    try:
        mod = input('\033[1;36m请选择设备类型：\033[0m')
        if mod == 'h':
            show_help()
        elif mod == 'q':
            t.kill_self()
        else:
            CURRENT_MODULE = t.select_mod(int(mod))
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
            InputWatcher()
    except (ValueError, IndexError):
        os.system('clear')
        print('\033[1;31m错误:输入不合法！！！重新输入 \033[0m')
        start_main()


if __name__ == '__main__':
    try:
        os.system('clear')
        t = Tools()
        start_main()
    except KeyboardInterrupt:
        stop_self = True
        # print('\n\033[1;31m=======退出=======\033[0m')
    except Exception as e:
        print(repr(e))
