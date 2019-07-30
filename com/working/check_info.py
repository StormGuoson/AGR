import os
import subprocess
import sys
import threading
import time
from queue import Queue

import psutil


class AsynchronousFileReader(threading.Thread):
    """
    Helper class to implement asynchronous reading of a file
    in a separate thread. Pushes read lines on a queue to
    be consumed in another thread.
    """

    def __init__(self, fd, queue):
        assert callable(fd.readline)
        threading.Thread.__init__(self)
        self._fd = fd
        self._queue = queue

    def run(self):
        """The body of the tread: read lines and put them on the queue."""
        try:
            for line in iter(self._fd.readline, ''):
                self._queue.put(line)
        except ValueError:
            pass

    def eof(self):
        """Check whether there is no more content to expect."""
        return not self.is_alive() and self._queue.empty()


def consume(command):
    """
    Example of how to consume standard output and standard error of
    a subprocess asynchronously without risk on deadlocking.
    """
    # Launch the command as subprocess.
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               shell=True)
    # Launch the asynchronous readers of the process' stdout and stderr.
    stdout_queue = Queue()
    stdout_reader = AsynchronousFileReader(process.stdout, stdout_queue)
    stdout_reader.start()
    stderr_queue = Queue()
    stderr_reader = AsynchronousFileReader(process.stderr, stderr_queue)
    stderr_reader.start()
    # Check the queues if we received some output (until there is nothing more to get).
    # frame.txt_log.write(('No%s_' % str(int(no) + 1)) + ACTIVE_DEVICES[int(no)] + u' <<<开始>>>' + '\r')
    while not stdout_reader.eof() or not stderr_reader.eof():
        if is_finish:
            break
        while not stdout_queue.empty():
            line = stdout_queue.get().decode("utf-8", errors="ignore")
            check_by_logcat(line)
        while not stderr_queue.empty():
            line = stderr_queue.get().decode('utf-8')
            print(str(line))
            break
        # Sleep a bit before asking the readers again.
        try:
            time.sleep(.1)
        except KeyboardInterrupt:
            pass

    for k, v in data.items():
        print('%s\t%s' % (k, v))
    kill_self()
    return
    # Let's be tidy and join the threads we've started.
    # stdout_reader.join()
    # stderr_reader.join()
    # Close subprocess' file descriptors.
    # process.stdout.close()
    # process.stderr.close()
    # process.kill()


def kill_self():
    print('\n\033[1;31m=======确认完毕=======\033[0m')
    pids = psutil.pids()
    for pid in pids:
        if psutil.Process(pid).name() == 'Python':
            psutil.Process(pid).kill()


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


def check_by_logcat(line):
    global is_finish
    if None not in data.values():
        is_finish = True
        return
    if current_type == 'cwbox':
        if 'ASR SDK VERSION_NAME_QA:' in line:
            sdk_ver = line[line.find('VERSION_NAME_QA:') + 16:-1]
            data['sdk版本号'] = sdk_ver
    elif current_type == 'ainemo':
        if 'ASR SDK VERSION_NAME_QA:' in line:
            sdk_ver = line[line.find('VERSION_NAME_QA:') + 14:-1]
            data['sdk版本号'] = sdk_ver
        if 'asr.start param' in line:
            pid = line[line.find('pid":') + 5:]
            pid = pid[:pid.find(',')]
            data['pid'] = pid
            url = line[line.find('decoder-server.url":"') + 21:]
            url = url[:url.find('"')]
            data['url'] = url
        elif 'SdkConfigProvider-key' in line:
            key = line[line.find('SdkConfigProvider-key') + 22:-1]
            data['key'] = key
    elif current_type == 'cw':
        if 'ASR SDK VERSION_NAME_QA:' in line:
            sdk_ver = line[line.find('VERSION_NAME_QA:') + 16:-1]
            data['sdk版本号'] = sdk_ver
    elif current_type == 'cw-demo':
        if 'ASR SDK VERSION_NAME_QA:' in line:
            sdk_ver = line[line.find('VERSION_NAME_QA:') + 16:-1]
            data['sdk版本号'] = sdk_ver
    elif current_type == 'chuangmi':
        if 'ASR SDK VERSION_NAME_QA:' in line:
            sdk_ver = line[line.find('VERSION_NAME_QA:') + 16:-1]
            data['sdk版本号'] = sdk_ver

    if 'SHA1' in line:
        if data['唤醒引擎版本'] is None:
            line = line[line.find('SHA1: ') + 6:line.find('at') - 1]
            data['唤醒引擎版本'] = line
        elif data['VAD引擎版本号'] is None:
            line = line[line.find('SHA1: ') + 6:line.find('at') - 1]
            data['VAD引擎版本号'] = line


def static_check(t):
    os.popen('adb root').close()
    os.popen('adb remount').close()
    if t == 'cwbox':
        sys_info = os.popen('adb shell getprop | grep display')
        t = sys_info.readlines()[1]
        t = t[t.find(']: [') + 4:t.rfind(']')]
        data['系统版本号'] = t
        sys_info.close()
        lib = os.popen('adb shell md5sum system/lib/libbdSPILAudioProc.so')
        data['信号库md5'] = lib.readlines()[0].split()[0]
        lib.close()
        lib = os.popen('adb shell md5sum system/lib/libbd_audio_vdev.so')
        data['音频库md5'] = lib.readlines()[0].split()[0]
        lib.close()
        wp = os.popen('adb shell md5sum /data/data/com.baidu.muses.vera/files/speechres/lib_esis_wp.pkg.so')
        data['唤醒资源md5'] = wp.readlines()[0].split()[0]
        wp.close()
        vad = os.popen('adb shell md5sum /data/data/com.baidu.muses.vera/files/speechres/libesis_vad.pkg.so')
        data['VAD资源md5'] = vad.readlines()[0].split()[0]
        vad.close()
    elif t == 'cw':
        sys_info = os.popen('adb shell getprop | grep display')
        t = sys_info.readlines()[0]
        t = t[t.find(']: [') + 4:t.rfind(']')]
        data['系统版本号'] = t
        sys_info.close()
        lib = os.popen('adb shell md5sum system/lib/libbdSPILAudioProc.so')
        data['信号库md5'] = lib.readlines()[0].split()[0]
        lib.close()
        lib = os.popen('adb shell md5sum system/lib/libbd_audio_vdev_4_2.so')
        data['音频库md5'] = lib.readlines()[0].split()[0]
        lib.close()
        wp = os.popen(
            'adb shell md5sum /data/data/com.skyworth.lafite.srtnj.speechserver/files/speechres/lib_esis_wp.pkg.so')
        data['唤醒资源md5'] = wp.readlines()[0].split()[0]
        wp.close()
        vad = os.popen(
            'adb shell md5sum /data/data/com.skyworth.lafite.srtnj.speechserver/files/speechres/libesis_vad.pkg.so')
        data['VAD资源md5'] = vad.readlines()[0].split()[0]
        vad.close()
    elif t == 'cw-demo':
        sys_info = os.popen('adb shell getprop | grep display')
        t = sys_info.readlines()[0]
        t = t[t.find(']: [') + 4:t.rfind(']')]
        data['系统版本号'] = t
        sys_info.close()
        lib = os.popen('adb shell md5sum system/lib/libbdSPILAudioProc.so')
        data['信号库md5'] = lib.readlines()[0].split()[0]
        lib.close()
        lib = os.popen('adb shell md5sum system/lib/libbd_audio_vdev_4_2.so')
        data['音频库md5'] = lib.readlines()[0].split()[0]
        lib.close()
        wp = os.popen(
            'adb shell md5sum /data/data/com.baidu.speech.demo/lib/lib_esis_wp.pkg.so')
        data['唤醒资源md5'] = wp.readlines()[0].split()[0]
        wp.close()
        vad = os.popen(
            'adb shell md5sum /data/data/com.baidu.speech.demo/lib/libesis_vad.pkg.so')
        data['VAD资源md5'] = vad.readlines()[0].split()[0]
        vad.close()
    elif t == 'ainemo':
        lib = os.popen('adb shell md5sum vendor/lib/libbdSPILAudioProc.so')
        lib1 = lib.readlines()[0].split()[0]
        data['信号库md5'] = lib1
        lib.close()
        lib = os.popen('adb shell md5sum vendor/lib/libbd_audio_vdev.so')
        data['音频库md5'] = lib.readlines()[0].split()[0]
        lib.close()
        sys_info = os.popen('adb shell getprop | grep display')
        t = sys_info.readlines()[0]
        t = t[t.find(']: [') + 4:t.rfind(']')]
        data['系统版本号'] = t
        sys_info.close()
        wp = os.popen('adb shell md5sum /data/data/com.baidu.launcher/files/speechres/lib_esis_wp.pkg.so')
        # wp = os.popen('adb shell md5sum data/data/com.baidu.speech.demo/lib/lib_esis_wp.pkg.so')
        data['唤醒资源md5'] = wp.readlines()[0].split()[0]
        wp.close()
        vad = os.popen('adb shell md5sum /data/data/com.baidu.launcher/files/speechres/libesis_vad.pkg.so')
        # vad = os.popen('adb shell md5sum data/data/com.baidu.speech.demo/lib/libesis_vad.pkg.so')
        data['VAD资源md5'] = vad.readlines()[0].split()[0]
        vad.close()
    elif t == 'chuangmi':
        sys_info = os.popen('adb shell getprop | grep display')
        t = sys_info.readlines()[0]
        t = t[t.find(']: [') + 4:t.rfind(']')]
        data['系统版本号'] = t
        sys_info.close()

        lib = os.popen('adb shell md5sum system/lib/libbdSPILAudioProc.so')
        data['信号库md5'] = lib.readlines()[0].split()[0]
        lib.close()

        lib = os.popen('adb shell md5sum system/lib/libbd_audio_vdev.so')
        data['音频库md5'] = lib.readlines()[0].split()[0]
        lib.close()

        wp = os.popen(
            'adb shell md5sum /data/local/esis_xiaodu_wak.pkg')
        data['唤醒资源md5'] = wp.readlines()[0].split()[0]
        wp.close()

        vad = os.popen(
            'adb shell md5sum /data/local/esis_xiaodu_vad.pkg')
        data['VAD资源md5'] = vad.readlines()[0].split()[0]
        vad.close()

        vad = os.popen(
            'adb shell md5sum /system/lib/libbdAudProxy.so')
        data['下沉库'] = vad.readlines()[0].split()[0]
        vad.close()

        vad = os.popen(
            'adb shell md5sum /system/lib/libaudrpc_spil.so')
        data['RPC'] = vad.readlines()[0].split()[0]
        vad.close()


def select_type(t):
    global data
    print('收集信息中...')
    devs = get_device_list()
    print(devs[0])

    if t == 'cwbox' or t == 'cw' or t == 'cw-demo':
        data = {
            'sdk版本号': None,
            '系统版本号': None,
            '信号库md5': None,
            '音频库md5': None,
            '唤醒引擎版本': None,
            '唤醒资源md5': None,
            'VAD引擎版本号': None,
            'VAD资源md5': None
        }
    elif t == 'ainemo':
        data = {
            'sdk版本号': None,
            '系统版本号': None,
            '信号库md5': None,
            '音频库md5': None,
            '唤醒引擎版本': None,
            '唤醒资源md5': None,
            'VAD引擎版本号': None,
            'VAD资源md5': None,
            'pid': None,
            'url': None,
            'key': None
        }
    elif t == 'chuangmi':
        data = {
            'sdk版本号': None,
            '系统版本号': None,
            '信号库md5': None,
            '音频库md5': None,
            '下沉库': None,
            'RPC': None,
            '唤醒引擎版本': None,
            '唤醒资源md5': None,
            'VAD引擎版本号': None,
            'VAD资源md5': None
        }
    static_check(t)
    os.popen('adb logcat -c')
    consume('adb -s %s logcat -v time' % devs[0])


if __name__ == '__main__':
    data = {}
    current_type = 'ainemo'
    is_finish = False
    select_type(current_type)
