import sys
import pandas as pd
from selenium import webdriver


class Main(object):
    def __init__(self):
        self.d = webdriver.Firefox()
        self.d.get('http://bailing.audio.baidu-int.com:8081/index.php/tools/common/index?flag=1')


if __name__ == '__main__':
    file = sys.argv[1]