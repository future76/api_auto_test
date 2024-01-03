#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：qianxun_api 
@File    ：conftest.py
@IDE     ：PyCharm 
@Author  ：future76_lly
@Date    ：2023/12/18 11:21 
'''
# 注意：名字是固定的。
# 可以写具体的方法、正常的调用某个接口
# pytest在运行的时候【会自动】先调起这个文件，后面还具体调用这个方法

# 方法：获取token
# 1. 正常的请求对应的接口并且提取数据
# 2. 告诉别人这个是一个测试夹具（测试前置、后置操作）：@pytest.fixture()
import logging
import pytest
from api_keyword.api_key import ApiKey


@pytest.fixture(scope="session")
def token_fix():
    ak = ApiKey()
    url = "https://gateway.bilinl.com/uaa/login/acct"
    data = {
        "clientId": "83YslrcMpBt3X3c0eK8jvhdPAW84ScHc",
        "clientSecret": "rosJtPuAMy69wnEMiw9UqRaQNELypEyk",
        "loginIp": "113.240.251.66",
        "username": "13627411831",
        "password": "123456abcd",
        "phoneLogin": "0"
    }
    resp = ak.post(url=url, data=data)
    token = "Bearer " + ak.get_text(resp.text, "$..value")
    return ak, token


# 当执行一个case的时候会自动的调用这个方法：把对应的数据传过来给到call
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    # 通过 out = yield 定义了一个生成器。在生成器中，res = out.get_result() 获取了测试结果对象。
    out = yield
    res = out.get_result()
    #  res.when == "call"：表示正在运行调用测试函数的阶段。
    if res.when == "call":
        logging.info(f"用例ID：{res.nodeid}")
        logging.info(f"测试结果：{res.outcome}")
        logging.info(f"故障表示：{res.longrepr}")
        logging.info(f"异常：{call.excinfo}")
        logging.info(f"用例耗时：{res.duration}")
        logging.info("**************************************")