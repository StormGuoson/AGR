import itertools
import os
import subprocess
import sys
import time
import matplotlib.pyplot as plt
import numpy as np


def song_decoder(song):
    song = song.replace('WUB', ' ')
    while song.startswith(' '):
        song = song[1:]
    while song.endswith(' '):
        song = song[:-1]
    for s in range(len(song), 1, -1):
        if ' ' * s in song:
            song = song.replace(' ' * s, ' ')
    return song


def domain_name(url):
    url = url[url.find('//') + 2:]
    return url[:url.find('.')] if url.count('.') == 1 else url[url.find('.') + 1:url.rfind('.')]


def per(s):
    pass


def format_duration(seconds):
    # your code here
    years = str(seconds / (365 * 24 * 60 * 60))
    left = seconds % (365 * 24 * 60 * 60)
    days = str(left / (24 * 60 * 60))
    left = left % (24 * 60 * 60)
    hours = str(left / (60 * 60))
    left = left % (60 * 60)
    minutes = str(left / 60)
    seconds = str(left % 60)
    res = str('%s years and %s days and %s hours and %s minutes and %s seconds' % (
        years, days, hours, minutes, seconds)).replace('0 years and ', '').replace('0 days and ', '').replace(
        '0 hours and ', '').replace('0 minutes and ', '').replace('0 seconds', '')
    res = res.strip()
    if res.endswith(','):
        res = res[:-1]
    res = res.replace('1 years', '1 year').replace('1 days', '1 day').replace('1 hours', '1 hour').replace('1 minutes',
                                                                                                           '1 minute').replace(
        '1 seconds', '1 second')
    print(res.replace(' and', ',', res.count('and') - 1))


def move_zeros(array):
    zc = 0
    res = []
    for e in array:
        if (str(e) == '0') or (str(e) == '0.0'):
            zc += 1
        else:
            res.append(e)
    print(res)

    a = b = 0
    return res + [0] * zc


class A(object):

    @staticmethod
    def foo1(i):
        return i ** 2


def dirReduc(arr):
    point = [0, 0]
    res = []
    for a in arr:
        if a == 'NORTH':
            point[1] += 1
        elif a == 'SOUTH':
            point[1] -= 1
        elif a == 'EAST':
            point[0] += 1
        elif a == 'WEST':
            point[0] -= 1
    if point[0] > 0:
        res += ['EAST'] * point[0]
    elif point[0] < 0:
        res += ['WEST'] * point[0]
    if point[1] > 0:
        res += ['NORTH'] * point[1]
    elif point[1] < 0:
        res += ['SOUTH'] * point[1]
    print(point)
    return res


def permutations(iterable, r=None):
    pool = tuple(iterable)
    n = len(pool)
    r = n if r is None else r
    if r > n:
        return
    indices = list(range(n))
    cycles = list(range(n, n - r, -1))
    yield tuple(pool[i] for i in indices[:r])
    while n:
        for i in reversed(range(r)):
            cycles[i] -= 1
            if cycles[i] == 0:
                indices[i:] = indices[i + 1:] + indices[i:i + 1]
                cycles[i] = n - i
            else:
                j = cycles[i]
                indices[i], indices[-j] = indices[-j], indices[i]
                yield tuple(pool[i] for i in indices[:r])
                break
        else:
            return


class Calculator(object):
    @staticmethod
    def evaluate(string):
        r = string.split(' ')
        print(r)
        while len(r) != 1:
            for e in r:
                if e == '/' or e == '*':
                    m = r.index(e)
                    e2 = (r.pop(m + 1))
                    e1 = (r.pop(m - 1))
                    if e == '/':
                        r[r.index('/')] = float(e1) / float(e2)
                    else:
                        r[r.index('*')] = float(e1) * float(e2)
                    break
                elif e == '+' or e == '-':
                    if r.count('/') or r.count('*'):
                        continue
                    m = r.index(e)
                    e2 = (r.pop(m + 1))
                    e1 = (r.pop(m - 1))
                    if e == '+':
                        r[r.index('+')] = float(e1) + float(e2)
                    else:
                        r[r.index('-')] = float(e1) - float(e2)
                    break
            print(r)
        return r[0]


def out(n):
    res = itertools.permutations(['(', ')'] * n)
    res = set(res)
    word = []
    for e in res:
        isPass = True
        t = []
        for y in e:
            t.append(y)
            if t.count('(') < t.count(')'):
                isPass = False
                break
        if isPass:
            tmp = ''.join(e)
            word.append(tmp)

    return word


def judge(n, ap):
    if n < 100:
        return False
    if n in ap:
        return True
    if int(str(n)[1:]) == 0:
        return True
    for i in range(len(str(n)[:-1])):
        if str(n)[i] != str(n)[i + 1]:
            break
        if i == len(str(n)) - 2:
            return True

    for i in range(len(str(n)[:-1])):
        if str(n)[i] != '9':
            if str(int(str(n)[i]) + 1) != str(n)[i + 1]:
                break
            if i == len(str(n)) - 2:
                return True
        else:
            if str(n)[i + 1] != '0':
                break
            if i == len(str(n)) - 2:
                return True

    for i in range(len(str(n)[:-1])):
        if str(n)[i] != '0':
            if str(int(str(n)[i]) - 1) != str(n)[i + 1]:
                break
            if i == len(str(n)) - 2:
                return True
        else:
            if str(n)[i + 1] != '9':
                break
            if i == len(str(n)) - 2:
                return True

    for i, d in enumerate(range(len(str(n)) - 1, 0, -1)):
        if i >= d:
            return True
        if str(n)[i] != str(n)[d]:
            break
    return False


def is_interesting(number, awesome_phrases=[]):
    n = number
    ap = awesome_phrases
    if judge(n, ap):
        return 2
    if judge(n + 1, ap) or judge(n + 2, ap):
        return 1
    else:
        return 0


def twoSum(nums, target):
    for k1, v1 in enumerate(nums):
        for k2, v2 in enumerate(nums):
            if k1 == k2: continue
            if v1 + v2 > target: continue
            if v1 + v2 == target:
                return [k1, k2]


def reverse(x):
    res = int(str(x)[::-1]) if x > 0 else -int(str(x)[::-1][:-1])
    return res


class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


def addTwoNumbers(l1, l2):
    i1 = i2 = ''
    while l1.next:
        i1 += str(l1.val)
        l1 = l1.next
    while l2.next:
        i2 += str(l2.val)
        l2 = l2.next
    print(i1)
    print(i2)
    res = int(i1[::-1]) + int(i2[::-1])
    return list(int(x) for x in str(res)[::-1])


if __name__ == '__main__':
    x = np.array([1, 2, 3, 4, 5, 6])
    y = np.array([11, 12, 13, 14, 15, 16])
    plt.plot(x, y, 'red')
    plt.show()
