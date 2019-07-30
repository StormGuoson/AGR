import subprocess
import sys

if __name__ == '__main__':
    data = 0
    sp = subprocess.Popen('adb -s %s logcat' % sys.argv[1], stdout=subprocess.PIPE, shell=True)
    for line in iter(sp.stdout.readline, ''):
        if b'CALLBACK' in line and b'zljasr':
            line = line.decode('utf-8')
            if 'wp.data' in line:
                print('唤醒成功')
                data = 1
            elif 'CALLBACK = asr.partialfirst_package' in line:
                if data == 1:
                    data += 1
            elif 'CALLBACK = asr.end' in line:
                if data == 2:
                    data += 1
            elif 'CALLBACK = asr.partialfinal_result' in line:
                if data == 4:
                    print('通过')
                data = 0
            elif ('final_result' in line and 'CALLBACK' in line) or 'finalResult' in line:
                if data == 3:
                    data += 1
