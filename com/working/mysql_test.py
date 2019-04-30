import pymysql
from selenium import webdriver


class ExeSql(object):
    def __init__(self, lh='localhost', u='root', p='baidu@123', db='learnsql', search_limit=None):
        self.db = pymysql.Connect(lh, u, p, db)
        self.csr = self.db.cursor()
        self.search_limit = search_limit

    def exe(self, s, is_show=False, b1=True, b2=True):
        try:
            self.db.begin()
            self.csr.execute(s)
            if is_show:
                self.__show(b1, b2)
            self.db.commit()
        except Exception as e1:
            print(repr(e1))
            self.db.rollback()

    def show_tbl(self, table_name):
        self.exe('select * from %s' % table_name, True)

    def __show(self, is_show_desc, is_format):
        if self.search_limit:
            fetch = self.csr.fetchmany(self.search_limit)
        else:
            fetch = self.csr.fetchall()
        title = self.csr.description
        if not fetch:
            print('done')
            return
        fetch = [list(e) for e in fetch]
        if is_show_desc:
            titles = []
            for t in title:
                titles.append(t[0])
            fetch.insert(0, titles)
        # 格式化输出
        if is_format:
            cols = len(fetch[0])
            rows = len(fetch)
            for col in range(cols):
                max_len = -1
                for row in range(rows):
                    if fetch[row][col] is not None:
                        length = len(str(fetch[row][col]))
                        if length > max_len:
                            max_len = length
                for row in range(rows):
                    if fetch[row][col] is None:
                        length = 4
                        fetch[row][col] = 'None'
                    else:
                        length = len(str(fetch[row][col]))
                    space = ' ' * (max_len - length)
                    fetch[row][col] = str(fetch[row][col]) + space

        for i, c in enumerate(fetch):
            if i == 0 and is_show_desc:
                print('\33[7m%s\33[0m' % c)
            else:
                print(c)


class FindUrl(object):
    def __init__(self, url=None):
        opt = webdriver.FirefoxOptions()
        # opt.add_argument('-headless')
        self.d = webdriver.Firefox(options=opt)

    def _get(self, url):
        self.d.get(url)

    def fetch(self, url, start=1, end=None):
        self._get(url)
        content = self.d.find_elements_by_class_name('content')
        author = \
            self.d.find_elements_by_class_name('author clearfix')
        print(author)


if __name__ == '__main__':
    msg = '''
    select * from customer
    '''
    m_url = 'https://www.qiushibaike.com/text/page/1'

    # sql = ExeSql()
    web = FindUrl()
    web.fetch(m_url)
    # sql.exe(msg, True)
