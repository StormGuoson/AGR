import os


def foo(s):
    res = 0
    for i, v in enumerate(s[::-1]):
        res += (ord(v.lower()) - 96) * 26 ** i
    print(res)


def rec(s):
    length = len(s)
    if length == 1:
        return ord(s) - 96
    return 26 ** (length - 1) * rec(s[1:])


def foo1(string):
    res = 0
    d = {}
    for i, v in enumerate('0123456789'):
        d[v] = i
    for i, v in enumerate(string[::-1]):
        res += d[v] * 10 ** i
    return res


def water(num):
    for i in range(num):
        i = str(i)
        res = 0
        for i2 in i:
            res += int(i2) ** 3
        if res == int(i):
            print(res)


def foo2(string):
    # return string[::-1]
    # res = []
    # string = list(string)
    # while len(string) > 0:
    #     res.append(string.pop())
    # return ''.join(res)
    res = ''
    for v in string:
        res = v + res
    return res


def k(x):
    return len(x)


if __name__ == '__main__':
    res = os.popen('ls').readlines()
    for r in res:
        print(r[:-1], end='')
