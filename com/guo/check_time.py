import subprocess
import time
import numpy

if __name__ == '__main__':
    sp = subprocess.Popen('adb logcat', stdout=subprocess.PIPE, shell=True)
    total_time = []
    start_time = end_time = 0
    count = 0
    for line in iter(sp.stdout.readline, ''):
        try:
            line = line.decode()
            if 'wp.data count' in line:
                print(line[:-1])
                start_time = time.time()
            elif '----CALLBACK = asr.finish' in line:
                count += 1
                print(line)
                end_time = time.time()
                dur = end_time - start_time
                total_time.append(dur)
                print(dur)
                print('\033[1;31mcount:%d, avg is %fs\033[0m\n' % (count, numpy.mean(total_time)))
        except UnicodeDecodeError:
            pass
