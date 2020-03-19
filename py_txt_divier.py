# 全局变量
talk = ['请输入文件名（空行代表all.txt;若无后缀名则默认为.txt文件）:',
        '请输入分割数量:',
        '请输入分割模式（0:保留换行符 1:大小均匀版  默认为0 毁格式版本尚未开发完毕，估计也没用。。。）:']

modeDist = {'0': 'self.tidy()', '1': 'self.untidy()'}


def talker(n):
    print(talk[n])
    return input()


def file_name(fn):
    if fn == '':
        return 'all.txt'
    if fn.find('.') == -1:
        fn += '.txt'
        print(fn)
        return fn


def divide_num(num_str):
    try:
        if num_str == '':
            raise Exception
        return int(num_str)
    except Exception:
        print('输入有误，请重新开始。')


def divide_mode(mode):
    if mode == '1':
        return 1
    else:
        return 0

class Divide(object):
    def __init__(self, divide_file, num, mode):
        self.f = divide_file
        self.num = num
        self.total_length = len(str(self.num))

        self.read()
        self.run(mode)

    def read(self):
        self.content = self.f.read()
        self.f.close()

    def run(self,mode):
        eval(modeDist[mode])

    def make_file_names(self):
        self.file_names = [i+1 for i in range(self.num)]  # 20.3.19改
        s = fileName[0:fileName.find('.')]  # 获取文件名(不含后缀)
        s += '[%s]' # % str(selfnum).zfill(self.total_length)  # 添加序号  # 20.3.19改
        s += fileName[fileName.find('.'):len(fileName)]  # 添加后缀名
        self.file_names = list(map(lambda x: s % x ,self.file_names))  # 20.3.19改

    def tidy(self):
        lines = self.content.splitlines(keepends=True)
        line_count = len(lines)
        lines_per_file = line_count // self.num

        point = 1
        line_point = 0
        while point <= self.num:
            wfile = open(self.file_names[point], 'w', encoding='utf-8')
            start_line_point = line_point
            while line_point < start_line_point + lines_per_file and line_point < line_count:
                wfile.write(lines[line_point])
                line_point += 1
            wfile.close()
            del wfile
            point += 1

    def untidy(self):
        print('都说了没开发好试什么试？我崩了')
        exit()


fileName = file_name(talker(0))

divideNum = divide_num(talker(1))

divideMode = divide_mode(talker(2))

file = open(fileName, 'r')
Divide(file, divideNum, divideMode)
file.close()
