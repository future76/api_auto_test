#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：qianxun_api 
@File    ：allure_report.py
@IDE     ：PyCharm 
@Author  ：future76_lly
@Date    ：2023/12/18 15:07 
'''
import os
import shutil

import allure


class AllureReport:
    '''allure报告相关'''

    @staticmethod
    def dynamic_title(CaseData):
        '''动态生成标题'''
        # allure.dynamic.title(data[11])

        # 如果存在自定义标题
        if CaseData["caseName"] is not None:
            # 动态生成标题
            allure.dynamic.title(CaseData["caseName"])

        if CaseData["storyName"] is not None:
            # 动态获取story模块名
            allure.dynamic.story(CaseData["storyName"])

        if CaseData["featureName"] is not None:
            # 动态获取feature模块名
            allure.dynamic.feature(CaseData["featureName"])

        if CaseData["remark"] is not None:
            # 动态获取备注信息
            allure.dynamic.description(CaseData["remark"])

        if CaseData["rank"] is not None:
            # 动态获取级别信息(blocker、critical、normal、minor、trivial)
            allure.dynamic.severity(CaseData["rank"])

    @staticmethod
    def generate_report(config):
        '''
        allure报告生成
        :param config:
        :return:
        '''
        # 构建 cd 路径 | alllure generate -c 临时报告路径 -o 正式报告路径
        cmd = f" cd {config.allure_path_bin} | allure generate -c {config.allure_temp_path} -o {config.allure_report_path}"
        # 通过os.system将cmd在cmd命令窗口运行
        os.system(cmd)

    @staticmethod
    def tendency_chart(config):
        '''
        趋势图
        :param config:
        :return:
        '''
        # report报告的路径
        ALLURE_REPORT_HISTORY = os.path.join(config.allure_report_path, "history")
        # temp的路径
        ALLURE_TEMP_HISTORY = os.path.join(config.allure_temp_path, "history")
        # 首先需要删除temp目录下存在的history
        if os.path.exists(ALLURE_TEMP_HISTORY):
            shutil.rmtree(ALLURE_TEMP_HISTORY)
        # 从report目录中。复制history目录树到 temp的hisotry
        shutil.copytree(ALLURE_REPORT_HISTORY, ALLURE_TEMP_HISTORY)
