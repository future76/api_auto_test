#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：api-automation-testing 
@File    ：extract_data.py
@IDE     ：PyCharm 
@Author  ：future76_lly
@Date    ：2023/12/19 10:52 
'''
import json
from api_keyword.api_key import ApiKey


def json_extraction(CaseData, res, all_var: dict):
    '''
    提取响应之后的数据
    :param CaseData: 当前的Case，主要获取需要提取数据的字段：jsonExData
    :param res: 响应得到的对应的结果
    :param all_var: 空字典
    :return:
    '''
    try:
        if CaseData["jsonExData"]:
            Exdata = eval(CaseData["jsonExData"])  # {"VAR_TOKEN":"$..token","MSG":"$.msg"}
            print("需要提取的数据：>>>", Exdata)
            for key, value in Exdata.items():
                # 通过对应的jsonpath获取具体的数据
                new_value = ApiKey().get_text(res.json(), value)
                all_var.update(
                    {key: new_value}
                )
            print("提取出来的数据：>>>", all_var)
        else:
            print("需要提取的数据为空")
    except Exception:
        print("请检查你需要提取数据数据格式的正确性。")


def sql_extraction(CaseData, all_var: dict):
    """
     从数据库提取数据
    :param CaseData: 当前的Case，主要获取需要提取数据的字段：sqlExData
    :return:
    """
    try:
        if CaseData["sqlExData"]:
            Exdata = eval(CaseData[
                              "sqlExData"])  # {"name":"SELECT username FROM sxo_user WHERE username='hami'","id":"SELECT id FROM sxo_user WHERE username='hami'"}
            print("SQL-需要提取的数据：>>>", Exdata)
            for key, value in Exdata.items():
                # 通过对应的sql获取具体的数据
                new_value = ApiKey().get_sqlData(value)
                all_var.update(
                    {key: new_value}
                )
            print("SQL-提取出来的数据：>>>", all_var)
        else:
            print("SQL-需要提取的数据为空")
    except Exception:
        print("SQL-请检查你需要提取数据数据格式的正确性。")


def sql_assertData(CaseData):
    res = True
    if CaseData["sqlAssertData"] and CaseData["sqlExpectResult"]:
        # 实际结果：从数据库读取出来的数据--字典的格式 # {"name":"SELECT username FROM sxo_user WHERE username='hami'","id":"SELECT id FROM sxo_user WHERE username='hami'"}
        realityData = eval(CaseData["sqlAssertData"])
        # 期望结果:{"name":"hami","id":75}
        expectData = json.loads(CaseData["sqlExpectResult"])

        realityDataDict = {}
        for key, value in realityData.items():
            # 通过对应的sql获取具体的数据
            new_value = ApiKey().get_sqlData(value)
            realityDataDict.update(
                {key: new_value}
            )

        if expectData != realityDataDict:
            res = False
    return res

