import re
import os
import xlsxwriter as xw
import requests
import json

import xlsxwriter.exceptions


def process_data():
    for row in data:
        row[1] = ip2loca[row[0]]


def query_ip():
    for ip in ips:
        location = \
            json.loads(requests.get(f"http://opendata.baidu.com/api.php?query={ip}&co=&resource_id=6006&oe=utf8").text)[
                "data"][0]["location"]
        ip2loca[ip] = location


def export2xlsx():
    workbook = xw.Workbook("log_analyze.xlsx")  # 创建工作簿
    worksheet1 = workbook.add_worksheet("sheet1")  # 创建子表
    worksheet1.activate()  # 激活表
    # title = ['序号', '项目', '数据']  # 设置表头
    worksheet1.set_column(0, 0, 16)
    worksheet1.set_column(1, 1, 18)
    worksheet1.set_column(3, 3, 20)
    worksheet1.set_column(5, 5, 40)
    worksheet1.set_column(7, 7, 7)
    worksheet1.set_column(10, 10, 50)

    worksheet1.write_row('A1', columns)  # 从A1单元格开始写入表头
    i = 2  # 从第二行开始写入数据
    while True:
        try:
            for info in data:
                row = "A" + str(i)
                worksheet1.write_row(row, info)
                i += 1
            break
        except xlsxwriter.exceptions.FileCreateError:
            print("文件打开无法保存，关闭该文件！！")
            input("关闭后回车继续")
            continue
    workbook.close()




def grasp_infos(s: str):
    def get_path(s: str):
        try:
            s = s.split('"')[1].split(" ")[1]
        except:
            try:
                s = s.split('"')[1].split(" ")[0]
            except:
                s = "/"
        return s

    def output():
        data.append([ip, "", user, time, method, path, http_ver, http_status, body_bytes_sent, http_referer, ua, s])

    s = repr(s)  # 防止转义！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
    ip = re.search(r"(\d+\.){3}\d+", s)[0]  # 匹配连接者ip地址
    ips.append(ip)
    try:
        user = re.search(rf"(?<={ip} - )\w+", s)[0]  # 匹配用户名
    except:
        user = ''
    # 处理时间
    t = re.search(r"\[.*]", s)[0][1:-7]  # 掐头去尾的时间
    t1 = t.split("/")
    t2 = t1[2].split(":")
    time = t2[0] + '/' + months[t1[1]] + '/' + t1[0] + " " + t2[1] + ':' + t2[2] + ':' + t2[3]
    # print(time)
    try:
        method = re.search(r"GET|POST|PUT|HEAD|DELETE|OPTIONS|CONNECT|TRACH|PROPFIND", s)[0]
        path = get_path(s)
        http_ver = re.search(rf"HTTP/\d\.\d", s)[0]
        http_status = re.search(rf"(?<={http_ver}\" )\d+", s)[0]
        body_bytes_sent = re.search(rf"(?<={http_status} )\d+", s)[0]
        http_referer = re.search(rf"(?<={body_bytes_sent} \").+?\"", s)[0][:-1]
        ua = s.split('"')[-2]
    except:
        method = "-"
        path = get_path(s)
        http_ver = "-"
        http_status = re.search(r"\d+", s.split('"')[2])[0]
        body_bytes_sent = re.search(rf"(?<={http_status} )\d+", s)[0]
        http_referer = re.search(rf"(?<={body_bytes_sent} \").+?\"", s)[0][:-1]
        ua = s.split('"')[-2]
    finally:
        output()


def main():
    files = os.listdir("log")
    log_files = []
    for t in files:
        if os.path.isfile("log\\" + t):
            if t.find(".log") != -1:
                log_files.append("log\\" + t)

    for file in log_files:
        with open(file, "r", ) as f:
            for line in f.readlines():
                grasp_infos(line)

    global ips
    ips = set(ips)
    print(ips)
    print("数据处理完成，开始请求属地")
    query_ip()
    process_data()
    export2xlsx()
    print("导出完成")


months = {"Jan": "01",
          "Feb": "02",
          "Mar": "03",
          "Apr": "04",
          "May": "05",
          "Jun": "06",
          "Jul": "07",
          "Aug": "08",
          "Sep": "09",
          "Oct": "10",
          "Nov": "11",
          "Dec": "12"}
columns = ["ip地址", "ip属地", "用户", "时间", "请求方法", "请求路径/内容", "http版本", "http请求状态码", "包体数据大小", "http来源", "ua", "日志原文"]
data = []
ips = []
ip2loca = {}
main()
