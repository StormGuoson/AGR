import pymysql


def show(_csr, is_format=True, title=None):
    _csr = [list(e) for e in _csr]
    if title is not None:
        titles = []
        for t in title:
            titles.append(t[0])
        _csr.insert(0, titles)
    # 格式化输出
    if is_format:
        cols = len(_csr[0])
        rows = len(_csr)
        for col in range(cols):
            max_len = -1
            for row in range(rows):
                if _csr[row][col] is not None:
                    length = len(str(_csr[row][col]))
                    if length > max_len:
                        max_len = length
            for row in range(rows):
                if _csr[row][col] is None:
                    length = 4
                    _csr[row][col] = 'None'
                else:
                    length = len(str(_csr[row][col]))
                space = ' ' * (max_len - length)
                _csr[row][col] = str(_csr[row][col]) + space

    for c in _csr:
        print(c)


if __name__ == '__main__':
    db = pymysql.Connect('localhost', 'root', 'baidu@123', 'learnsql')
    csr = db.cursor()
    sql = """select * from employee"""
    try:
        csr.execute(sql)
        print('done')
        res = csr.fetchall()
        show(res)
        db.commit()
    except Exception as e:
        print('error')
        print(repr(e))
        db.rollback()
