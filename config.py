#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：qianxun_api 
@File    ：config.py
@IDE     ：PyCharm 
@Author  ：future76_lly
@Date    ：2023/12/18 11:21 
'''

# 获取当前文件的绝对路路径
import os

BASE_DIR = os.path.dirname(__file__)
# 配置 allure程序包bin路径(环境变量)
allure_path_bin = os.path.join(BASE_DIR, "common", "allure-2.13.5/bin")

# 临时报告的路径
allure_temp_path = os.path.join(BASE_DIR, "report", "temp")
#正式报告路径
allure_report_path = os.path.join(BASE_DIR, "report", "allure_report")

# 配置常量的文件
# 环境变量
# 正式环境
PROJECT_URL = "https://gateway.bilinl.com/"

# 测试环境
PROJECT_TEST_URL = "http://gateway.test.csbilin.com/"

# 正式环境
# 商家账号：
MERCHANT_USERNAME = '13627411831'
MERCHANT_PASSWORD = '123456abcd'

# 运营端账号
TERMINAL_USERNAME = '19918899808'
TERMINAL_PASSWORD = 'qianXUN#@*add88'

# 测试环境
# 小二郎商家账号：
TEST_MERCHANT_USERNAME = '13627411667'
TEST_MERCHANT_PASSWORD = '123456abcd'

# 运营账号：
test_TERMINAL_USERNAME = '13627411831'
test_TERMINAL_PASSWORD = '123456abcd'
# # 运行模式：
# RUNMODE = "EXCEL"
# RUNMODE = "YAML"

# 测试用例的路径：
CASEDATAURL = "./data/excel/api_cases.xlsx"
SHEETNAME = "Sheet1"

YAMLDATA = "./data/yaml/api_yaml.yaml"


# 错误提示异常信息
MSG_DATA_ERROR = "数据解析错误，请检查dict_data的值的正确性。"
MSG_EXDATA_ERROR = "响应数据提取失败。"
MSG_ASSERT_OK = "测试通过，断言成功。"
MSG_ASSERT_NO = "测试失败，断言失败。"

# 测试数据库的连接信息
DB_HOST = 'shop-xo.hctestedu.com'  # 数据库地址
DB_PORT = 3306
DB_USER = 'api_test'  # 数据库用户名
DB_PASSWORD = 'Aa9999!'  # 数据库密码
DB_NAME = 'shopxo_hctested'  # 数据库名称


if __name__ == '__main__':
    print(allure_temp_path,allure_report_path)