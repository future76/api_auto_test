#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：qianxun_api 
@File    ：run.py
@IDE     ：PyCharm 
@Author  ：future76_lly
@Date    ：2023/12/18 11:21 
'''

import pytest

import config
from common.allure_report import AllureReport



# 框架的运行入口
if __name__ == '__main__':
    #  通过pytest 运行 并且生成allure报告【默认】
    # 第一步： 指定运行文件，通过文件会生成运行结果后的数据放在：./result ； --clean-alluredir（每次运行之前清空这个文件夹的历史数据）
    # pytest.main(["./testcase/test_case_01.py", "--alluredir", "./report/temp", "--clean-alluredir"])
    # pytest.main(["./testcase/test_case_01.py", "--alluredir", "./report/temp"])
    pytest.main(["./testcase/test_case_01.py"])
    # 第二步：把数据转成测试报告（html）：allure generate ./result -o ./report_allure --clean
    # os.system() # 在cmd（终端）去运行命令  cmd = f" cd {allure_path_bin} | allure generate -c {config.allure_temp_dir_path} -o {config.allure_report_dir_path}"
    # os.system(f"cd {allure_path_bin} |allure generate ./result -o ./report_allure --clean")

    # 生成allure报告
    AllureReport.generate_report(config)
    # 生成趋势图
    AllureReport.tendency_chart(config)
