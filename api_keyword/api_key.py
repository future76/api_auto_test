#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：qianxun_api
@File    ：api_key.py
@IDE     ：PyCharm 
@Author  ：future76_lly
@Date    ：2023/12/4 15:16 
'''
from deepdiff import DeepDiff

from config import *

"""
    通过添加对应的测试步骤：
    - @allure.step("步骤内容注释")
    - @allure.title("测试用例标题")
"""
import allure
import json
import jsonpath
import requests


class ApiKey:
    '''
    api关键字驱动
    '''

    @allure.step(">>>>>>发送get请求")
    def get(self, url, params=None, **kwargs):
        '''
        发送get请求
        :param url: 请求的URL
        :param params: 需要拼装在url中的参数
        :param kwargs: 其他参数，参考requests.get()
        :return: 响应数据
        '''
        return requests.get(url=url, params=params, **kwargs)

    @allure.step(">>>>>>发送post请求")
    def post(self, url, data=None, json=None, **kwargs):
        '''
        发送post请求
        :param url:请求的url
        :param data: 请求的数据
        :param json: 请求数据如果是json可直接使用该参数
        :param kwargs: 其他参数，参考requests.post()
        :return: 响应数据
        '''
        return requests.post(url=url, data=data, json=json, **kwargs)

    @allure.step(">>>>>>发送options请求")
    def options(self, url, **kwargs):
        '''
        发送options请求
        :param url: 请求的url
        :param kwargs: 其他参数，参考requests.options()
        :return: 响应数据
        '''
        return requests.options(url=url, **kwargs)

    @allure.step(">>>>>>发送head请求")
    def head(self, url, **kwargs):
        '''
        发送head请求
        :param url: 请求的url
        :param kwargs: 其他参数，参考requests.head()
        :return: 响应数据
        '''
        return requests.head(url=url, **kwargs)

    @allure.step(">>>>>>发送put请求")
    def put(self, url, data=None, **kwargs):
        '''
        发送put请求
        :param url: 请求的url
        :param data: 请求的数据
        :param kwargs: 其他参数，参考requests.put()
        :return: 响应数据
        '''
        return requests.put(url=url, data=data, **kwargs)

    @allure.step(">>>>>>发送patch请求")
    def patch(self, url, data=None, **kwargs):
        '''
        发送patch请求
        :param url: 请求的url
        :param data: 请求的数据
        :param kwargs: 其他参数，参考requests.patch()
        :return: 响应数据
        '''
        return requests.patch(url=url, data=data, **kwargs)

    @allure.step(">>>>>>发送delete请求")
    def delete(self, url, **kwargs):
        '''
        发送delete请求
        :param url: 请求的delete
        :param kwargs: 其他参数，参考requests.delete()
        :return: 响应数据
        '''
        return requests.delete(url=url, **kwargs)

    @allure.step(">>>>>>获取响应数据")
    def get_text(self, response, key):
        '''
        基于jsonpath获取数据的关键字：用于提取所需要的内容
        :param response: 响应报文，默认为json格式
        :param key: jsonpath的表达式
        :return:
        '''
        print("-----------获取响应数据-----------")
        # 判断对应的变量是不是字符串格式
        if isinstance(response, str):
            '''如果是字符串，就转成JSON 格式的字符串转换为 Python 对象。'''
            response = json.loads(response)
        value_list = jsonpath.jsonpath(response, key)
        return value_list[0]

    @allure.step(">>>>>>:开始提取数据库的数据")
    def get_sqlData(self, sqlValue):
        """

        :param sqlValue: SQL,返回的数据是一个元组
        :return:
        """
        import pymysql

        # 1. 配置数据库连接信息并连接
        connection = pymysql.connect(
            host=DB_HOST,  # 数据库地址
            port=DB_PORT,
            user=DB_USER,  # 数据库用户名
            password=DB_PASSWORD,  # 数据库密码
            db=DB_NAME,  # 数据库名称
        )
        # 2. 创建游标对象，使用它进行操作
        cursor = connection.cursor()
        # 4. 使用游标对象去执行操作SQL
        cursor.execute(sqlValue)
        # 5. 得到结果集的下一行
        result = cursor.fetchone()
        # 6. 关闭数据库连接
        cursor.close()
        return result[0]

    @allure.step(">>>>>>:响应数据全量对比")
    def jsonDeepDiff(self, json1, json2, **other):
        """
        对比json数据的一致性
        :param json1: 期望结果
        :param json2: 实际结果
        :param other: 你想要写的对应的规则
        :return:
        """
        res = DeepDiff(json1, json2, **other)
        if res == {}:
            return True
        else:
            return False


if __name__ == '__main__':
    ak = ApiKey()
    data = {
        "clientId": "83YslrcMpBt3X3c0eK8jvhdPAW84ScHc",
        "clientSecret": "rosJtPuAMy69wnEMiw9UqRaQNELypEyk",
        "loginIp": "113.240.251.66",
        "username": "13627411831",
        "password": "123456abcd",
        "phoneLogin": "0"
    }
    resp = ak.post(url="https://gateway.bilinl.com/uaa/login/acct", data=data)
    print(resp.text)
    results=ak.get_text(resp.text, "$..message")
    print(results)
