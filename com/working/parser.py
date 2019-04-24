import ast
import sys

if __name__ == '__main__':
    r = sys.argv[1]
    res = open('result.txt', 'w')
    with open(r, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if 'asr result' in line and 'corpus_no' in line:
                line = ast.literal_eval(line[line.find('{'):line.rfind('}') + 1])
                text = line['result']['word'][0]
                sn = line['sn']
                corpus = str(line['corpus_no'])
                res.write('%s_%s_%s\n' % (text, sn, corpus))
    res.flush()
    res.close()
