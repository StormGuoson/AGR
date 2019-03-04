import os
import subprocess
import threading
import time
from queue import Queue


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
        for line in iter(self._fd.readline, ''):
            self._queue.put(line)

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
    # Sleep a bit before asking the readers again.
    try:
        time.sleep(.1)
    except KeyboardInterrupt:
        pass
    # Let's be tidy and join the threads we've started.
    stdout_reader.join()
    stderr_reader.join()
    # Close subprocess' file descriptors.
    process.stdout.close()
    process.stderr.close()
    process.kill()


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
        for k, v in data.items():
            print('%s\t%s' % (k, v))
        return
    if 'ASR SDK VERSION_NAME' in line:
        sdk_ver = line[line.rfind(':') + 2:-1]
        print(sdk_ver)
        data['sdk版本号'] = sdk_ver
    elif 'SHA1' in line:
        if data['唤醒引擎版本'] is None:
            pass
        elif data['VAD引擎版本号'] is None:
            pass


def check_by_m():
    sys_info = os.popen('adb shell getprop | grep display')
    data['系统版本号'] = sys_info.readlines()[0]
    sys_info.close()
    lib = os.popen('adb shell md5sum system/lib/libbdSPILAudioProc.so')
    data['信号库md5'] = lib.readlines()[0].split()[0]
    lib.close()
    wp = os.popen('adb shell md5sum /data/data/com.baidu.speech.demo/lib/lib_esis_wp.pkg.so')
    data['唤醒资源md5'] = wp.readlines()[0].split()[0]
    wp.close()
    vad = os.popen('adb shell md5sum /data/data/com.baidu.speech.demo/lib/libesis_vad.pkg.so')
    data['VAD资源md5'] = vad.readlines()[0].split()[0]
    vad.close()


if __name__ == '__main__':
    print('收集信息中...')
    data = {
        'sdk版本号': None,
        '系统版本号': None,
        '信号库md5': None,
        '唤醒引擎版本': None,
        '唤醒资源md5': None,
        'VAD引擎版本号': None,
        'VAD资源md5': None
    }
    is_finish = False
    devs = get_device_list()
    print(devs[0])
    consume('adb -s %s logcat' % devs[0])
