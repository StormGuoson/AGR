import ast
import sys
import os


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
                        line = line.decode('utf-8')
                        if self.check(line, args):
                        # if 'final_result' in line and 'results_recognition' in line and 'finalResult' in line:
                            print(line)
                            line = ast.literal_eval(line[line.find('{'):line.rfind('}') + 1])
                            text = line['results_recognition'][0]
                            corpus = str(line['origin_result']['corpus_no'])
                            sn = line['origin_result']['sn']
                            fnl = '%s_%s_%s' % (text, sn, corpus)
                            res.write(fnl + '\n')
                            # print(fnl)
                    except UnicodeDecodeError:
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
    lp = LogParser()
    lp.parser('asrEventListener', 'AsrEngine', 'final_result')
