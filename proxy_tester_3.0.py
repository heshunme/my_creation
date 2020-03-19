import json
import re
from concurrent.futures import ThreadPoolExecutor
from time import sleep

import requests

url = 'http://www.httpbin.org/ip'
urll = 'https://www.httpbin.org/ip'
headers = {
    'Host': 'httpbin.org',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'DNT': '1',
    'Accept-Encoding': 'gzself.ip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}
proxies = []
result_dict = {'both': [], 'http_only': [], 'https_only': []}
point = -1
error_list = ['-http get website successfully: ',
              '---------http connection error: ',
              '------------------http timeout: ',
              '------------http content error: ',
              '-------------------http Unsafe: ',
              '--------------http test passed: ',
              'https get website successfully: ',
              '--------https connection error: ',
              '-----------------https timeout: ',
              '-----------https content error: ',
              '------------------https Unsafe: ',
              '-------------https test passed: ',
              '----------------------------------------------All passed: ',
              '-----------------------------------------http passed: ',
              '----------------------------------------https passed: ',
              '-------------------------error: ',
              '--------------------http error: ',
              '-------------------https error: ',
              ]
log = open('proxy tester.log', 'w')
both_count = 0
http_count = 0
https_count = 0
finish_count = -1
'''
185.132.178.141:1080
23.252.209.36:8080
185.132.133.179:1080
'''


class proxyTest(object):
    def __init__(self, point):
        self.point = point
        self.timeout = 15
        self.ip = ''

    def logger(self, code):
        '''
        :param int
            code: different numbers have different meaning:
               1:Successfully get the website through http proxy
               2:http connection error
               3:http timeout
               4:http content error
               5:http unsafe error透明代理
               6:http alright
               7:Successfully get the website through https proxy
               8:https connection error
               9:https timeout
               10:https content error
               11:https unsafe error
               12:https alright
               13:strange error(no way!)
               13:all passed
               14:http passed only
               15:https passed only
        :return:
        '''
        '''
        logger is to write a beautiful log....and process the errors but may be I can't realize this purpose because of 
        my poor programming skills...however,I will try my best.  ^_^
        '''
        log.write(error_list[code - 1] + str(self.point + 1) + ' ' + proxies[self.point]['http'] + '\n')
        return

    def http(self):
        json_http = {}
        require_http = None
        html_http = ''

        # get http
        try:
            require_http = requests.get(url=url, headers=headers, proxies=proxies[self.point], timeout=self.timeout)
            require_http.raise_for_status()
            html_http = require_http.text
            self.logger(code=1)
            # print('Successfully get the website through http://' + proxies[self.point]['http'])
        except ConnectionError:
            self.logger(code=2)
            return False
            # print(str(self.point) + ' ' + proxies[self.point]['http'] + ' connection error')
        except TimeoutError:
            self.logger(code=3)
            return False
            # print(str(self.point) + ' ' + proxies[self.point]['http'] + ' timeout')
        finally:
            require_http.close()

        json_http = json.loads(html_http)
        if json_http['origin'].find(self.ip) != -1:  # content correct
            if json_http['origin'].find('115.215') == -1:  # http enbled and safe
                self.logger(code=6)
                return True
            else:  # http unsafe
                self.logger(code=5)
                return False
                # print(str(self.point) + ' ' + proxies[self.point]['http'] + ' is unsafe')
        else:  # content error
            self.logger(code=4)
            return False
            # print(str(self.point) + ' ' + proxies[self.point]['http'] + ' content error')

    def https(self):
        json_https = {}
        require_https = None
        html_https = ''

        # get https
        try:
            # print('https test: ' + proxies[self.point]['https'])
            require_https = requests.get(url=urll, headers=headers, proxies=proxies[self.point], timeout=self.timeout)
            html_https = require_https.text
            if html_https.find('baidu') != -1:
                self.logger(code=7)
            # print('Successfully get the website through https://' + proxies[self.point]['https'])
        except ConnectionError:
            self.logger(code=8)
            return False
        except TimeoutError:
            self.logger(code=9)
            return False
        finally:
            require_https.close()

        # judge
        json_https = json.loads(html_https)
        if json_https['origin'].find(self.ip) != -1:  # https enbled
            if json_https['origin'].find('115.215') == -1:  # https enbled and safe
                self.logger(code=12)
                return True
            else:  # unsafe
                self.logger(code=11)
                return False
                # print(str(self.point) + ' ' + proxies[self.point]['https'] + ' is unsafe')
        else:  # https content error
            self.logger(code=10)
            return False

    def start(self):
        global result_dict, both_count, http_count, https_count, finish_count
        try:
            self.ip = re.findall('(\d+.\d+.\d+.\d+)', proxies[self.point]['http'], re.S)[0]
            http = self.http()
            https = self.https()
            if http:
                if https:  # both http and https
                    result_dict['both'] += [proxies[self.point]['http']]
                    both_count += 1
                    self.logger(code=13)
                else:  # http only
                    result_dict['http_only'] += [proxies[self.point]['http']]
                    http_count += 1
                    self.logger(code=14)
            elif https:
                result_dict['https_only'] += [proxies[self.point]['https']]
                https_count += 1
                self.logger(code=15)
        except:
            self.logger(code=16)
        finally:
            finish_count += 1
            eve = (finish_count + 1) / total * 100
            print('Have Finished %d %%' % eve)
        return


def process(point):
    test = proxyTest(point=point)
    test.start()
    del test
    return


print('input the proxies and end with a empty line:')

line = input()
while line != '':
    temp = {
        'http': line,
        'https': line
    }
    proxies = proxies + [temp]
    line = input()
total = len(proxies)

print('Received!')
print(proxies)

sleep(1)

print('Start Testing......')

file = open('C:\\Users\\Adm\\Desktop\\proxy.txt', 'w')
file.write('Total:%d \n\n' % total)
file.write('Both https and http: \n')

pool = ThreadPoolExecutor(512)
if __name__ == '__main__':
    while point + 1 < len(proxies):
        point += 1
        pool.submit(process, point)
pool.shutdown(wait=True)

for term in result_dict['both']:
    file.write(term + '\n')
file.write('Both total: %d \n\n' % both_count)
file.write('Http_Only: %d\n' % http_count)
for term in result_dict['http_only']:
    file.write(term + '\n')
file.write('\nHttps_Only: %d\n' % https_count)
for term in result_dict['https_only']:
    file.write(term + '\n')

print(result_dict)

file.close()
log.close()
print('Finished\nResults are on the desktop now.')
