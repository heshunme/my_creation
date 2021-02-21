from tkinter import Tk, Message, Label, Listbox, Button, Frame, Canvas, Entry, StringVar
from time import sleep
from random import randint
from threading import Thread
from json import dump, load

version = '1.4'

errorDic = {'time_input_error': '时间输入有误',
            'count_input_errror': '笔数输入有误',
            'mode_selection_error': '模式选择有误',
            'set_canvas_error': '背景设置失败，请确认本软件的文件完整性，如若完整，请联系开发者',
            'quests_get_error': '获取题目数量失败',
            'windows_error': '创建窗口失败，请确认本软件的文件完整性，如若完整，请联系开发者',
            'pack_error': '数据保存时出错，请检查您的文件系统是否发生故障、磁盘（U盘）是否写保护或损坏',
            'deny': '您没有同意免责声明，无法使用本软件，请重新启动本软件并同意免责声明后正常使用',
            'ans_print_error': '答案输出窗口创建失败。请尝试重启本软件或联系开发者以解决此问题',
            'thread_error': '多线程启动失败，请确认本软件的文件完整性，如若完整，请联系开发者',
            'do_not_start_another_thread': '请不要在一次练习未完成时试图开启另一个练习',
            }
runList = ['self.run_mix()',
           'self.run_sum()']
# '''
iniDict = {'version': version,
           '最大数值': 100,
           '每两道题之间的间隔时长': 2,
           '上一次题数': 1,
           '上一次每笔时长(ms)': 1000,
           '上一次笔数': 0,
           '上一次模式': 0,
           }


def dump_json():
    f = open('珠心算练习工具配置文件.json', 'w', encoding='utf-8')
    dump(iniDict, f, ensure_ascii=False)
    f.close()


try:
    f = open('珠心算练习工具配置文件.json', 'r', encoding='utf-8')
    iniDict_temp = load(f)
    f.close()
    if iniDict_temp['version'] != version:
        dump_json()
    else:
        iniDict = iniDict_temp
except:
    dump_json()
print(iniDict)

max_num = iniDict['最大数值']  # 数的最大数值
period = iniDict['每两道题之间的间隔时长']  # 两道题之间的间隔时间
deny = True


def undeny():
    global deny
    deny = False
    windows.destroy()


def pred():
    global windows
    windows = Tk()
    windows.geometry('1200x500')
    windows.title('注意事项')
    s = '''欢迎使用 珠心算练习工具1.4
    本程序由 河瞬 使用Python编写 联系作者 邮箱：tianrunme@foxmail.com
    警告：更新本软件后  请  务 必 删 除  原配置文件，否则可能引发未知问题！
                                        免责声明
    1、一切本程序用户在下载并使用本程序是均被视为已经仔细阅读本条款并完全同意。
    2、因使用本程序而产生的一切可能的后果由使用者本人承担，本程序开发者对此不承担任何责任。
    3、本声明未涉及的问题请参考国家有关法律，当本声明与国家有关法律法规冲突时，以国家法律法规为准。
    4、本声明最终解释权由 河瞬 个人所有。'''
    message = Message(windows, text=s, font=('微软雅黑', 20), width=1200)
    message.pack()
    button = Button(windows, text='我已仔细阅读并完全同意以上声明', command=undeny)
    button.pack()
    button_quit = Button(windows, text='我不同意以上声明', command=windows.destroy)
    button_quit.pack()
    windows.mainloop()


class App(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.quests = iniDict['上一次题数']
        self.time = iniDict['上一次每笔时长(ms)'] / 1000
        self.count = iniDict['上一次笔数']
        self.mode = iniDict['上一次模式']
        self.ansList = []
        self.t = None
        self.pack()

        self.set_canvas()
        self.create_widgets()

    def _start(self):
        if self.t is None:
            self.t = Thread(target=self.start)
        if not self.t.is_alive():
            del self.t
            try:
                self.t = Thread(target=self.start)
                self.t.start()
            except:
                self.warn('thread_error')
        else:
            self.warn('do_not_start_another_thread')

    def start(self):
        if deny:
            self.warn('deny')
            return
        self.boo = True
        self.get_time()
        self.get_count()
        self.get_mode()
        self.get_quests()
        self.packer()
        count = 1
        if self.boo:
            while count <= self.quests:
                eval(runList[self.mode])
                self.label_num['text'] = '写答案'
                sleep(period)
                print('下一题')
                count += 1
        else:
            return

    def get_time(self):
        try:
            self.time = float(self.entry_time.get()) / 1000
        except:
            self.warn('time_input_error')

    def get_count(self):
        try:
            self.count = int(self.entry_count.get())
        except:
            self.warn('count_input_errror')

    def get_mode(self):
        """
        模式：0=加减混合  1=累加
        """
        try:
            self.mode = self.listbox_mode.curselection()[0]
        except:
            self.warn('mode_selection_error')

    def get_quests(self):
        try:
            self.quests = int(self.entry_quest.get())
        except:
            self.warn('quests_get_error')

    def set_canvas(self):
        try:
            self.canvas = Canvas(self, bg="#000000", width=1280, height=720, bd=0, highlightthickness=0)
            self.canvas.pack()
        except:
            self.warn('set_canvas_error')

    def create_widgets(self):
        try:
            # 大标题
            self.title = Label(self.canvas, text="珠心算练习工具", bg='#000000', fg='#66ccff', font=('微软雅黑', 30))
            self.title.pack(side='top')
            # 题目数量
            self.label_quest = Label(self.canvas, text="题目数量", bg='#000000', fg='red', font=('微软雅黑', 12))
            self.label_quest.pack(side='top')
            # 题目数量输入框
            self.entry_quest = Entry(self.canvas, bg='#000000', fg='#ffffff', bd=3, width=10)
            self.entry_quest.pack(side='top')
            self.entry_quest.insert(0, str(self.quests))

            # 间隔时间
            self.label_time = Label(self.canvas, text="每笔时间", bg='#000000', fg='red', font=('微软雅黑', 12))
            self.label_time.pack(side='left')
            # 间隔时间输入框
            self.entry_time = Entry(self.canvas, bg='#000000', fg='#ffffff', bd=3, width=10)
            self.entry_time.pack(side='left')
            self.entry_time.insert(0, str(self.time * 1000))

            # 笔数
            self.label_count = Label(self.canvas, text="笔数", bg='#000000', fg='red', font=('微软雅黑', 12))
            self.label_count.pack(side='left')
            # 笔数输入框
            self.entry_count = Entry(self.canvas, bg='#000000', fg='#ffffff', bd=3, width=10)
            self.entry_count.pack(side='left')
            self.entry_count.insert(0, str(self.count))

            # 模式
            self.label_mode = Label(self.canvas, text="模式选择", bg='#000000', fg='red', font=('微软雅黑', 12))
            self.label_mode.pack(side='left')
            # 模式选择框
            modes = StringVar()
            modes.set(("加减混合", "累加"))
            self.listbox_mode = Listbox(self.canvas, bg='#000000', fg='#ffffff', bd=2, listvariable=modes, height=2)
            self.listbox_mode.pack(side='left')

            # 开始按钮
            self.button_start = Button(self.canvas, text='开始', bg='#666666', fg='#ffffff', font=('微软雅黑', 12))
            self.button_start["command"] = self._start
            self.button_start.pack(side='left')
            # 数字显示区
            self.label_num = Label(self.canvas, text='000', bg='#000000', fg='white', font=('微软雅黑', 200), width=10,
                                   height=1)
            self.label_num.pack()
            # 答案显示按钮
            self.button_ans = Button(self.canvas, text='点击显示答案', bg='#666666', fg='#ffffff', font=('微软雅黑', 12))
            self.button_ans['command'] = self._print_ans
            self.button_ans.pack()
            # 退出按钮
            self.quit = Button(self.canvas, text="QUIT", bg='#000000', fg="red", command=self.master.destroy)
            self.quit.pack(side='bottom')
        except:
            self.warn('windows_error')

    def run_mix(self):
        count = 0
        self.summation = 0
        self.rand = 0
        while count < self.count:
            count += 1
            if count == 1:
                sleep(self.time)
            if self.summation > max_num:
                if self.summation != 0:
                    self.rand = randint(- max_num, max_num)
                else:
                    self.rand = randint(0, max_num)
            else:
                self.rand = randint(- self.summation, max_num)
            self.summation += self.rand
            self.change_color(count)
            self.label_num['text'] = str(self.rand)
            sleep(self.time)
        # self.label_ans['text'] = str(self.summation)
        self.ansList += [self.summation]

    def run_sum(self):
        count = 0
        self.summation = 0
        while count < self.count:
            count += 1
            if count == 1:
                sleep(self.time)
            self.rand = randint(0, max_num)
            self.summation += self.rand
            self.change_color(count)
            self.label_num['text'] = str(self.rand)
            sleep(self.time)
        self.ansList += [self.summation]

    def warn(self, text):
        self.boo = False
        window = Tk()
        window.geometry('400x150')
        window.title('警告！')
        message = Message(window, text=errorDic[text], width=400)
        message.pack()
        button = Button(window, text='关闭', command=window.destroy)
        button.pack()
        window.mainloop()
        del window, message, button

    def _sleep(self, time):
        sleep(time)

    def change_color(self, count):
        if count % 2 == 1:
            self.label_num['fg'] = '#66ccff'
        else:
            self.label_num['fg'] = '#9999ff'

    def packer(self):
        try:
            global iniDict
            iniDict = {'version': version,
                       '最大数值': max_num,
                       '每两道题之间的间隔时长': period,
                       '上一次题数': self.quests,
                       '上一次每笔时长(ms)': self.time * 1000,
                       '上一次笔数': self.count,
                       '上一次模式': self.mode,
                       }
            f = open('珠心算练习工具配置文件.json', 'w', encoding='utf-8')
            dump(iniDict, f, ensure_ascii=False)
            f.close()
        except:
            self.warn('pack_error')

    def _print_ans(self):
        self.print_ans(self.ansList)

    def print_ans(self, ansList):
        try:
            s = ''
            window = Tk()
            window.title('答案显示窗口')
            window.geometry('1000x500')
            ansList.reverse()
            count = 1
            while len(ansList) != 0:
                item = ansList.pop()
                s += str(count) + ')  ' + str(item) + '       '
                if count % 5 == 0:
                    s += '\n'
                count += 1
            label = Label(window, text=s, font=('微软雅黑', 20), width=1000)
            label.pack()
            button = Button(window, text='关闭', command=window.destroy)
            button.pack()
            window.mainloop()
        except:
            self.warn('ans_print_error')


# """

pred()
root = Tk()
root.title('珠心算练习工具' + iniDict['version'] + ' by 河瞬 作者邮箱：tianrunme@foxmail.com')
root.geometry('1280x530')
app = App(master=root)
app.mainloop()
# """
