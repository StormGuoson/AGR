import ast
import sys

if __name__ == '__main__':
    r = sys.argv[1]
    res = open('result.txt', 'w')
    with open(r, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line.find('final_result') != -1 and ('SpeechCallback' in line or 'finalResult' in line):
                line = ast.literal_eval(line[line.find('{'):line.rfind('}') + 1])
                text = line['results_recognition'][0]
                corpus = str(line['origin_result']['corpus_no'])
                sn = line['origin_result']['sn']
                fnl = '%s_%s_%s\n' % (text, sn, corpus)
                res.write(fnl)
                print(fnl)
    res.flush()
    res.close()
