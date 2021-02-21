# global count
ch = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w',
      'x', 'y', 'z', ]


def super_replacer(s: str, n=0):
    ss = ""
    for i in range(len(s)):
        ss += ch[(ch.index(s[i]) + n + 26) % 26]
    return ss

n = int(input("请输入相位:"))
s = input("请输入需要加密的原文:")
print(super_replacer(s,n))
