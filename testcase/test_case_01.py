#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：qianxun_api 
@File    ：test_case_01.py
@IDE     ：PyCharm 
@Author  ：future76_lly
@Date    ：2023/12/18 14:39 
'''
import json
import pytest
from jinja2 import Template   # 变量渲染
from api_keyword.api_key import ApiKey
from common.FileDataDriver import FileReader
from common.allure_report import AllureReport
from common.extract_data import json_extraction, sql_assertData, sql_extraction
from config import *


class TestCase:
    # 获取对应的数据 CaseData 需要从文档当中去进行读取
    # 1. 获取数据(四要素) 2. 发送请求 3.获取响应数据 4.断言
    AllCaseData = FileReader.read_excel()
    ak = ApiKey()
    # 定义：all_val 存放提取出的数据
    all_var = {}

    @pytest.mark.parametrize("CaseData", AllCaseData)
    def testCase(self, CaseData):
        AllureReport.dynamic_title(CaseData)
        CaseData = eval(Template(str(CaseData)).render(self.all_var))

        print(CaseData)

        # 写Excle的行和列
        row = CaseData["id"]
        column = 11

        # 初始化对应的值：
        res = None
        msg = None
        value = None

        # -------------------------发送请求-------------------------------
        try:
            # 请求数据
            url = CaseData["url"] + CaseData["path"]
            params = eval(CaseData["params"]) if isinstance(CaseData["params"], str) else None
            headers = eval(CaseData["headers"]) if isinstance(CaseData["headers"], str) else None
            # 增加对excel文件中请求体中的null处理
            if CaseData["type"] == "json":
                data = json.loads(CaseData["data"]) if isinstance(CaseData["data"], str) else None
            else:
                data = eval(CaseData["data"]) if isinstance(CaseData["data"], str) else None

            dict_data = {
                "url": url,
                "params": params,
                "headers": headers,
                "data": data
            }

            if CaseData["type"] == "json":
                dict_data["data"] = json.dumps(dict_data["data"])
        except Exception:
            value = MSG_DATA_ERROR
            FileReader.writeDataToExcel(row=row, column=column, value=value)
        else:  # 响应对象
            # 得到对应的响应数据
            res = getattr(self.ak, CaseData["method"])(**dict_data)

        # -------------------------提取数据库的操作---------------------------
        sql_extraction(CaseData, self.all_var)

        # -------------------------进行断言处理-------------------------------
        # 实际结果
        try:
            msg = self.ak.get_text(res.json(), CaseData["actualResult"])
        except Exception:
            value = MSG_EXDATA_ERROR
            FileReader.writeDataToExcel(row=row, column=column, value=value)
        else:
            # 只会是一个分支语言，但是不会造成测试结果成功或者失败，所以必须无论如何都是需要断言
            if msg == CaseData["expectResult"]:
                value = MSG_ASSERT_OK
                # 成功之后进行数据提取
                json_extraction(CaseData, res, self.all_var)

            else:
                value = MSG_ASSERT_NO
            FileReader.writeDataToExcel(row=row, column=column, value=value)
        finally:
            assert msg == CaseData["expectResult"], value

        # -------------------------进行数据库断言处理-------------------------------
        try:
            sqlAssertRes = sql_assertData(CaseData)  # False True
        except:
            print("SQL断言出现问题")
            value = "SQL断言出现问题"
            sqlAssertRes = False
            assert sqlAssertRes, value
        else:
            assert sqlAssertRes
        finally:
            FileReader.writeDataToExcel(row=row, column=column, value=value)

        # -------------------------响应文本全量断言-------------------------------
        if CaseData["responseExpect"]:
            # 期望数据
            json1 = eval(CaseData["responseExpect"])
            other = eval(CaseData["responseExclude"])
            jsonMaxDataRes = self.ak.jsonDeepDiff(json1, res.json(), **other)
            assert jsonMaxDataRes, "两者不一致"
