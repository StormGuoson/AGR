import ast
import sys
import os
import subprocess


class LogParser(object):
    def __init__(self, log=None):
        if log:
            self.log = log
        else:
            self.log = sys.argv[1]

    def parser(self, *args):
        logs = []
        with open('result.txt', 'w'):
            pass
        res = open('result.txt', 'a')
        if os.path.isfile(self.log):
            logs.append(self.log)
        else:
            files = os.listdir(self.log)
            logs = [os.path.join(self.log, x) for x in files]
        for log in logs:
            print(log)
            with open(log, 'rb') as f:
                lines = f.readlines()
                for line in lines:
                    try:
                        line = line.decode()
                        if (' asr finish' in line and 'm_isRunning' not in line) or (
                                'Final result' in line and 'results_recognition' not in line):
                            print(line)
                            line = ast.literal_eval(line[line.find('{'):line.rfind('}') + 1])
                            text = line['result']['word'][0]
                            corpus = str(line['corpus_no'])
                            sn = line['sn']
                            # print(fnl)
                    except Exception:
                        pass
        res.flush()
        res.close()

    @staticmethod
    def check(line, *args):
        for a in args[0]:
            if a not in line:
                return False
        return True


if __name__ == '__main__':
    # lp = LogParser()
    # lp.parser('asr finish')
    sp = subprocess.Popen('cat %s' % sys.argv[1], stdout=subprocess.PIPE, shell=True)
    for line in iter(sp.stdout.readline, ''):
        if b'name : wp.data' in line:
            line = line.decode()
            print('wakeup')
        elif b'finalResult' in line:
            try:
                line = line.decode()
                line = ast.literal_eval(line[line.find('{'):line.rfind('}') + 1])
                print(line['results_recognition'][0])
            except Exception:
                print(line)
