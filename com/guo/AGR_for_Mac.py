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
    except Exception as e1:
        print(repr(e1))
    L.release()


def _as(_text, _sn):
    print(_text + '\t' + _sn)
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
    p = sys.argv[0].split('/')
    with open('/%s/%s/..wakeup' % (p[1], p[2]), 'a') as f:
        f.write(ACTIVE_DEVICES[int(no)] + '\n')
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
is_save_log = False
stop_self = False
restart_self = False
SAVE_RESULTS = r'~/Desktop/res.log'
SAVE_AUDIO = r'~/Desktop/audio'
td = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

ACTIVE_DEVICES = []  # 激活的设备
CURRENT_MODULE = ''  # 当前模式
mods = []
logs = []

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
MOD_AINEMO_1L_DEMO = '小度在家1L-demo'
MOD_AINEMO_1C = '小度在家1C'
MOD_KUANYANG = '宽洋'
MOD_esp32 = 'esp32'
MOD_DRIVER = '车机'

MOD_LIST = [MOD_AINEMO_LAUNCHER,
            MOD_AINEMO_DEMO,
            MOD_CW_LAUNCHER,
            MOD_CW_DEMO,
            MOD_HUAWEI_LAUNCHER,
            MOD_HUAWEI_DEMO,
            MOD_CW_BOX,
            MOD_Max,
            MOD_XIAODUBOX,
            MOD_XGP,
            MOD_CW_BOX_DEMO,
            MOD_AINEMO_1S,
            MOD_AINEMO_1L_DEMO,
            MOD_AINEMO_1C,
            MOD_KUANYANG,
            MOD_esp32,
            MOD_DRIVER]

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
            self.module_cw_box(_line, no)
        elif _module == MOD_CW_BOX_DEMO:
            self.module_cw_show_demo(_line, no)
        elif _module == MOD_XGP:
            self.module_xgp(_line, no)
        elif _module == MOD_XIAODUBOX:
            self.module_xdbox(_line, no)
        elif _module == MOD_Max:
            self.module_max(_line, no)
        elif _module == MOD_AINEMO_1S:
            self.module_ainemo_1s(_line, no)
        elif _module == MOD_AINEMO_1L_DEMO:
            self.module_ainemo_1l_demo(_line, no)
        elif _module == MOD_AINEMO_1C:
            self.module_ainemo_1c(_line, no)
        elif _module == MOD_KUANYANG:
            self.module_ky(_line, no)
        elif _module == MOD_esp32:
            self.module_ep(_line, no)
        elif _module == MOD_DRIVER:
            self.module_driver(_line, no)

    @staticmethod
    def module_driver(line, no):
        if line.find("----final_result") != -1:
            # print(line)
            rec_result = line.split(':')
            # print(rec_result[0])
            # print(rec_result[1])
            # print(rec_result[2])
            res = rec_result[7]
            # sids = rec_result[2].split(' ')
            sid = ""
            # print(sid)
            text = res
            sn = sid
            res_final = text + ',' + sn
            DATA['text' + no] = text
            DATA['sn' + no] = sn
            auto_set(DATA['text' + no], DATA['sn' + no])

    @staticmethod
    def module_ep(line, no):
        if 'wakeup trigger status' in line:
            write_wakeup(no)
        elif 'asr result' in line and 'corpus_no' in line:
            line = ast.literal_eval(line[line.find('{'):line.rfind('}') + 1])
            text = line['result']['word'][0]
            sn = line['sn']
            corpus = str(line['corpus_no'])
            DATA['text' + no] = text
            DATA['sn' + no] = sn + "_" + corpus
            auto_set(DATA['text' + no], DATA['sn' + no])

    @staticmethod
    def module_ky(line, no):
        if u'唤醒成功' in line:
            write_wakeup(no)
        elif '\"type\":\"FINAL\"' in line:
            line = ast.literal_eval(line[line.find('{'):line.rfind('}') + 1])
            text = line['directive']['payload']['text']
            DATA['text' + no] = text
            DATA['sn' + no] = line['directive']['header']['dialogRequestId']
            auto_set(text, DATA['sn' + no])

    @staticmethod
    def module_ainemo_1c(line, no):
        if 'wakeup_time' in line and 'wp.data' in line and 'WakeUpEngine' in line:
            write_wakeup(no)
        elif line.find('final_result') != -1 and line.find('results_recognition') != -1:
            line = ast.literal_eval(line[line.find('{'):line.rfind('}') + 1])
            text = line['results_recognition'][0]
            sn = line['origin_result']['sn']
            corpus = str(line['origin_result']['corpus_no'])
            DATA['sn' + no] = sn + "_" + corpus
            DATA['text' + no] = text
            auto_set(text, sn)

    @staticmethod
    def module_ainemo_1l_demo(line, no):
        if 'wakeup_time' in line and 'SpeechCallback' in line:
            write_wakeup(no)
        elif 'finalResult' in line:
            line = ast.literal_eval(line[line.find('{'):])
            text = line['results_recognition'][0]
            corpus = str(line['origin_result']['corpus_no'])
            sn = line['origin_result']['sn']
            DATA['text' + no] = text
            DATA['sn' + no] = sn + '_' + corpus
            auto_set(DATA['text' + no], DATA['sn' + no])

    # 小度在家1S
    @staticmethod
    def module_ainemo_1s(line, no):
        if 'asr_reject' in line and 'state' in line and 'asr_result':
            line = ast.literal_eval(line[line.find('{'):line.rfind('}') + 1])
            reject = line['asr_reject']
            if reject == 0:
                reject = 'True'
            else:
                reject = 'False'
            state = line['state']
            DATA['sn' + no] = '&%s&%s' % (reject, state)
        if 'wakeup_time' in line and 'result' in line:
            write_wakeup(no)
        elif 'final_result' in line and 'results_recognition' in line and (
                'finalResult' in line or 'SpeechCallback' in line):
            if u'极客' in line:
                return
            if not DATA['sn' + no]:
                DATA['sn' + no] = ''
            line = ast.literal_eval(line[line.find('{'):line.rfind('}') + 1])
            DATA['text' + no] = line['results_recognition'][0]
            DATA['sn' + no] = line['origin_result']['sn'] + '_' + str(line['origin_result']['corpus_no']) + DATA[
                'sn' + no]
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
        if 'wakeup_time' in line and 'result' in line:
            write_wakeup(no)
        elif 'final_result' in line and 'AsrEngine' in line and 'asrEventListener' in line:
            # print(line[:-1])
            line = ast.literal_eval(line[line.find('{'):line.rfind('}') + 1])
            DATA['text' + no] = line['results_recognition'][0]
            DATA['sn' + no] = line['origin_result']['sn'] + '_' + str(line['origin_result']['corpus_no'])
            auto_set(DATA['text' + no], DATA['sn' + no])

    # 华为产品包 识别
    @staticmethod
    def module_huawei_launcher(line, no):
        if line.find('SpeechCallback') != -1 and line.find('wakeup_time') != -1:
            write_wakeup(no)
        elif line.find(u'SpeechCallback') != -1 and line.find('final_result') != -1 and line.find('corpus') != -1:
            # print line
            line = ast.literal_eval(line[line.find('{'):])
            DATA['text' + no] = line['best_result']
            DATA['sn' + no] = line['origin_result']['sn'] + '_' + str(line['origin_result']['corpus_no'])
            auto_set(DATA['text' + no], DATA['sn' + no])

    # 小鱼识别
    @staticmethod
    def module_ainemo(line, no):
        if 'asr_reject' in line and 'state' in line and 'asr_result':
            line = ast.literal_eval(line[line.find('{'):line.rfind('}') + 1])
            reject = line['asr_reject']
            if reject == 0:
                reject = 'True'
            else:
                reject = 'False'
            state = line['state']
            DATA['sn' + no] = '&%s&%s' % (reject, state)
        if 'wakeup_time' in line and 'SpeechCallback' in line:
            write_wakeup(no)
        elif 'final_result' in line and 'results_recognition' in line and (
                'finalResult' in line or 'SpeechCallback' in line):
            if u'极客' in line:
                return
            if not DATA['sn' + no]:
                DATA['sn' + no] = ''
            line = ast.literal_eval(line[line.find('{'):line.rfind('}') + 1])
            DATA['text' + no] = line['results_recognition'][0]
            DATA['sn' + no] = line['origin_result']['sn'] + '_' + str(line['origin_result']['corpus_no']) + DATA[
                'sn' + no]
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

    # 创维box
    @staticmethod
    def module_cw_box(line, no):
        if line.find("wakeup_time") != -1 and line.find("result") != -1:
            write_wakeup(no)
        # elif line.find('final_result') != -1 and line.find('finalResult') != -1:
        elif line.find('final_result') != -1 and ('SpeechCallback' in line or 'finalResult' in line):
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
        if line.find('wakeup_time') != -1 and line.find('SpeechCallback') != -1:
            write_wakeup(no)
        elif line.find('Final result') != -1:
            line = ast.literal_eval(line[line.find('{'):])
            text = line['results_recognition'][0]
            corpus = str(line['origin_result']['corpus_no'])
            sn = str(line['origin_result']['sn'])
            DATA['text' + no] = text
            DATA['sn' + no] = sn + "_" + corpus
            auto_set(DATA['text' + no], DATA['sn' + no])

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
            line = ast.literal_eval(line[line.find('{'):line.rfind('}') + 1])
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
    cm = mods[int(no)]
    while not stdout_reader.eof() or not stderr_reader.eof():
        if stop_self or restart_self:
            break
        while not stdout_queue.empty():
            line = stdout_queue.get().decode("utf-8", errors="ignore")
            try:
                if is_save_log:
                    logs[int(no)].write(line)
                mod.main_doing(line, cm, no)
            except Exception as e1:
                print('\033[1;31m错误: ' + repr(e1) + '\033[0m')
                # frame.txt_log.write(repr(e))
        while not stderr_queue.empty():
            line = stderr_queue.get().decode('utf-8')
            if 'has been replaced' in line or 'EOF' in line:
                continue
            print('\033[1;31m错误: 设备-' + ACTIVE_DEVICES[int(no)] + str(line) + '\033[0m')
            stop_self = True
            break
        # Sleep a bit before asking the readers again.
        time.sleep(.1)
    if is_save_log:
        logs[int(no)].close()
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

    def __init__(self, no):
        threading.Thread.__init__(self)
        self.no = no
        self.start()

    def run(self):
        global DATA, CURRENT_MODULE
        DATA = {}
        # _start_d = get_device_list()[CURRENT_DEVICE]
        _d = ACTIVE_DEVICES[self.no]
        CURRENT_MODULE = mods[self.no]
        if CURRENT_MODULE == MOD_XIAODUBOX:
            consume('ssh root@%s tail -F /tmp/speechsdk.log' % _d, str(self.no))
        elif CURRENT_MODULE == MOD_XGP:
            consume('adb -s %s shell tail -F /tmp/speechsdk.log' % _d, str(self.no))
        elif CURRENT_MODULE == MOD_esp32:
            consume('tail -F %s' % sys.argv[self.no + 1], str(self.no))
        else:
            os.popen('adb -s %s logcat -c' % _d).close()
            consume("adb -s %s logcat -v time" % _d, str(self.no))


class Tools(object):

    def __init__(self):
        self.finish_count = 0

    @staticmethod
    def save_full_log(no):
        p = sys.argv[0].split('/')
        dev = ACTIVE_DEVICES[int(no)]
        log_path = '/%s/%s/Desktop/audio/%s/%s.txt' % (p[1], p[2], dev, dev)
        if not os.path.exists(log_path[:log_path.rfind('/')]):
            os.makedirs(log_path[:log_path.rfind('/')])
        f = open(log_path, 'a')
        return f

    def pull_audio(self, dir_name):
        global CURRENT_MODULE
        DATA.clear()
        self.finish_count = 0
        print('\033[1;36m音频导出中......\033[0m\n')
        dir_name = dir_name.split(' ')
        if len(dir_name) == 1:
            dir_name = 'audio'
        else:
            dir_name = dir_name[1]
        for i, dev in enumerate(ACTIVE_DEVICES):
            CURRENT_MODULE = mods[i]
            p = sys.argv[0].split('/')
            save_path = '/%s/%s/Desktop/audio/%s/%s' % (p[1], p[2], dev, dir_name)
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            if CURRENT_MODULE in (MOD_AINEMO_DEMO, MOD_AINEMO_LAUNCHER):
                from_path = '/data/log/'
            elif CURRENT_MODULE in (MOD_AINEMO_1S, MOD_AINEMO_1C, MOD_AINEMO_1L_DEMO):
                from_path = 'mnt/aud_rec/'
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
        for line in iter(sp.stdout.readline, ''):
            line = line.decode()[:-1]
            if 'No such file or directory' in line:
                print('\n\033[1;31m设备 %s 没有音频\033[0m' % dev)
                self.finish_count += 1
                break
            if line == '':
                self.finish_count += 1
                break
            print(line, end='\r')
        sp.kill()
        if self.finish_count == len(ACTIVE_DEVICES):
            print('\033[1;36m\n导出完毕\033[0m\n')

    @staticmethod
    def restart_app():
        global CURRENT_MODULE
        DATA.clear()
        activities = {
            MOD_CW_LAUNCHER: 'com.skyworth.lafite.srtnj.speechserver/'
                             'com.skyworth.lafite.srtnj.setting.SkyLafiteSettingHomeActivity',
            MOD_HUAWEI_LAUNCHER: 'com.baidu.launcher/com.baidu.duer.home.activity.HomeActivity',
            MOD_HUAWEI_DEMO: 'com.baidu.speech.demo/com.baidu.speech.demo.ActivityWakeupAndAsr',
            MOD_Max: 'com.baidu.muses.vera',
            MOD_AINEMO_LAUNCHER: 'vulture.app.home/vulture.app.home.HomeActivity',
            MOD_AINEMO_DEMO: 'com.baidu.speech.demo/com.baidu.speech.demo.ActivityMain',
            MOD_CW_BOX_DEMO: 'com.baidu.speech.demo/com.baidu.speech.demo.ActivityWakeupAndAsr',
            MOD_AINEMO_1S: 'com.baidu.launcher/com.baidu.duershow.launcher.home.ui.activity.HomeActivity',
            MOD_AINEMO_1L_DEMO: 'com.baidu.speech.demo/com.baidu.speech.demo.ActivityWPASREvent',
            MOD_AINEMO_1C: 'com.baidu.launcher/com.baidu.duershow.launcher.home.ui.activity.HomeActivity'
        }

        for i, dev in enumerate(ACTIVE_DEVICES):
            CURRENT_MODULE = mods[i]
            if CURRENT_MODULE in activities.keys():
                print('\033[1;36m重启APP\033[0m\n')
                if CURRENT_MODULE in (MOD_AINEMO_LAUNCHER,):
                    os.popen('adb -s %s shell rm data/log/*.raw' % dev).close()
                    os.popen('adb -s %s shell rm data/log/logcat.full_log.*' % dev).close()
                stop = 'adb -s %s shell am force-stop %s 2>/dev/null' % (dev, activities[CURRENT_MODULE].split('/')[0])
                start = 'adb -s %s shell am start %s 2>/dev/null' % (dev, activities[CURRENT_MODULE])
                os.popen(stop).close()
                os.popen(start).close()
            else:
                print('\n\033[1;31m该设备不支持\033[0m')

    @staticmethod
    def reboot_dev():
        global CURRENT_MODULE
        print('\033[1;36m设备重启\033[0m\n')
        for i, dev in enumerate(ACTIVE_DEVICES):
            CURRENT_MODULE = mods[i]
            if CURRENT_MODULE == MOD_XIAODUBOX:
                threading.Thread(target=lambda: os.popen('ssh root@%s reboot' % dev).close()).start()
            else:
                threading.Thread(target=lambda: os.popen('adb -s %s reboot' % dev).close()).start()

    @staticmethod
    def kill_self():
        print('\n\033[1;31m=======退出=======\033[0m')
        pids = psutil.pids()
        for pid in pids:
            if psutil.Process(pid).name() in sys.argv[0]:
                psutil.Process(pid).kill()

    @staticmethod
    def select_mod(_index=-1):
        if _index == -1:
            return len(MOD_LIST)
        _index = int(_index)
        if _index >= len(MOD_LIST) or _index < 0:
            raise IndexError
        return MOD_LIST[_index]

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
        global stop_self, only_wakeup, restart_self, is_save_log
        while not stop_self and not restart_self:
            cmd = input()
            if cmd == 'c':
                DATA.clear()
                print('\033[1;36m唤醒次数归零\033[0m\n')
            elif cmd == 'q':
                stop_self = True
            elif cmd == 's':
                restart_self = True
                DATA.clear()
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
            elif cmd == 'log':
                if is_save_log:
                    is_save_log = False
                    for log in logs:
                        log.close()
                    logs.clear()
                    print('\033[1;36m关闭抓取日志\033[0m\n')
                else:
                    is_save_log = True
                    for i in range(len(ACTIVE_DEVICES)):
                        logs.append(t.save_full_log(i))
                    print('\033[1;36m开始抓取日志\033[0m\n')


def show_help():
    os.system('clear')
    mhelp = '''选好设备类型、设备连接顺序后可进行导音频、重启等操作,在终端中输入指令后按回车键即可。
    如果要使用模式15（esp32），需要在工具运行前传入参数，操作为：打开终端，将工具拖入，然后依次将日志文件拖入即可。
    
    输入 w        :切换唤醒/识别模式
    输入 c        :归零唤醒次数
    输入 reboot   :重启设备
    输入 restart  :重启APP
    输入 q        :退出程序
    输入 s        :停止当前模式并回到选择界面
    输入 log      :开始/关闭抓取日志，保存到~/Desktop/audio/deviceSN/deviceSN.txt。文件为续写，不会覆盖
    输入 p [name] :导音频至'~/Desktop/audio/deviceSN/name'下，'deviceSN'为设备号，name缺省值为'audio'
    
百度Hi：郭玉强
\033[1;36m按回车键继续\033[0m
    '''
    print(mhelp)
    input()
    os.system('clear')
    start_main()


def single_mod(mod):
    global CURRENT_MODULE
    CURRENT_MODULE = t.select_mod(mod)
    print('\033[1;34m当前模式：' + CURRENT_MODULE + '\033[0m')
    if CURRENT_MODULE == MOD_esp32:
        if len(sys.argv) == 1:
            raise ValueError
        for ag in sys.argv[1:]:
            ACTIVE_DEVICES.append(ag)
    elif CURRENT_MODULE != MOD_XIAODUBOX:
        dev = get_device_list()
        print(dev)
        if len(dev) == 1:
            order = '0'
        else:
            order = input('\033[1;36m请输入设备连接顺序,以空格区分(0为起始)\033[0m\n').split(' ')
        for o in order:
            ACTIVE_DEVICES.append(dev[int(o)])
    else:
        ips = input('\033[1;36m顺序输入设备ip，以逗号分割\033[0m\n')
        dev = ips.split(',')
        order = [i for i in range(len(dev))]
        for o in order:
            ACTIVE_DEVICES.append(dev[int(o)])
    for i in range(len(ACTIVE_DEVICES)):
        mods.append(CURRENT_MODULE)
    for i in range(len(ACTIVE_DEVICES)):
        ThreadLogcat(i)
    InputWatcher()


def multi_mod(ms):
    pm = ''

    for m in ms:
        pm += t.select_mod(m) + '、'
    print('\033[1;34m当前模式：' + pm[:-1] + '\033[0m')
    dev = get_device_list()
    print(dev)
    order = input('\033[1;36m请输入设备连接顺序,以空格区分(0为起始)\033[0m\n').split(' ')
    if len(order) != len(ms):
        raise ValueError
    for o in order:
        ACTIVE_DEVICES.append(dev[int(o)])
    for mod in pm.split('、'):
        mods.append(mod)
    for i in range(len(ACTIVE_DEVICES)):
        ThreadLogcat(i)
    InputWatcher()


def start_main():
    global only_wakeup, CURRENT_MODULE, stop_self, restart_self, is_save_log
    ACTIVE_DEVICES.clear()
    logs.clear()
    mods.clear()
    stop_self = restart_self = False
    only_wakeup = is_save_log = False
    t.show_mods()
    print('\033[1;33m输入 h 查看帮助\033[0m')
    try:
        mod = input('\033[1;36m请选择设备类型：\033[0m')
        if mod == 'h':
            show_help()
        elif mod == 'q':
            t.kill_self()
        elif len(mod.split()) == 1:
            single_mod(mod)
        else:
            multi_mod(mod.split())
    except (ValueError, IndexError):
        os.system('clear')
        print('\033[1;31m错误:输入不合法！！！重新输入 \033[0m')
        start_main()


if __name__ == '__main__':
    t = Tools()
    try:
        os.system('clear')
        start_main()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(repr(e))
