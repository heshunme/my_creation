# imports
import re

# global vars
qn = 26

# global count
ch = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w',
      'x', 'y', 'z', ]
pin = ["de", "ni", "wo", "ta", "zai", "zhong", "shang", "xia", "shi", "bu", "mei", "zao", "wan", "tian", "ba", "ne",
       "shuo"]


# 的 人称代词 介词 肯定 否定 时间 语气词 常见动词


def super_replacer(s: str, n=0):
    ss = ""
    for i in range(len(s)):
        ss += ch[(ch.index(s[i]) + n + 26) % 26]
    '''
    for i in range(26):
        s = s.replace(ch[i], ch[(i + n + 26) % 26])
    '''
    return ss


def judge(s: str):
    total = 0
    for i in pin:
        total += len(re.findall(i, s))
    return total


def qiong_ju(s: str):
    totals = []
    for i in range(26):
        totals += [0]
    for i in range(26):
        totals[i] = judge(super_replacer(s, i))
    for i in range(qn):
        print(super_replacer(s, totals.index(max(totals))))
        totals[totals.index(max(totals))] = 0


encrypted = input("请输入密文:")
qiong_ju(encrypted)
