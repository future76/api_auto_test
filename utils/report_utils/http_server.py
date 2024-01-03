# -*- coding: UTF-8 -*-
'''
@Project ：qianxun 
@File    ：http_server.py
@IDE     ：PyCharm 
@Author  ：future76_lly
@Date    ：2023/12/20 15:15 
'''
import http.server
import socketserver
import os
from functools import partial
import sys



'''
2. 将服务打包成exe文件
然后将这个服务使用Pyinstaller模块打包成exe文件。
1）安装Pyinstaller： pip install pyinstaller
2) 打包python服务：pyinstaller -F  源文件， 例如pyinstaller -F http_server.py

打包后会生成一个build目录，dist目录，http_server.spec文件。 我们只需要用到dist目录下的http_server.exe。

3） 将http_server.exe复制到allure-html报告根目录下。

'''
class HttpServer:
    def __init__(self, bind: str = "127.0.0.1", port: int = 8000, directory=os.getcwd()):
        """
        :param bind: 指定地址，如本地主机
        :param port: 自定义端口号, 服务器默认监听端口是 8000
        :param directory: 指定工作目录, 服务器默认工作目录为当前目录
        """
        self.bind = bind
        self.port = port
        self.directory = directory
        args = sys.argv
        for i in range(1, len(args)):
            if args[i] == "-port" and i + 1 < len(args):
                self.port = int(args[i + 1])
            if args[i] == "-dir" and i + 1 < len(args):
                self.directory = args[i + 1]
            if args[i] == "-bind" and i + 1 < len(args):
                self.bind = args[i + 1]

    def run(self):
        try:
            with socketserver.TCPServer((self.bind, self.port), partial(http.server.SimpleHTTPRequestHandler,
                                                                        directory=self.directory)) as httpd:
                print(
                    f"工作目录：{self.directory}\n"
                    f"Serving HTTP on {self.bind} port {self.port} \n"
                    f"http://{self.bind}:{self.port}/ ..."
                )
                httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nKeyboard interrupt received, exiting.")
            sys.exit(0)


if __name__ == '__main__':
    server = HttpServer()
    server.run()
