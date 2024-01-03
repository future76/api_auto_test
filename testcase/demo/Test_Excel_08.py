
import json
import pytest
from common.FileDataDriver import FileReader
from api_keyword.api_key import ApiKey
from config import *
import allure
from jinja2 import Template  # 变量渲染


class TestCase:
    # 获取对应的数据 CaseData 需要从文档当中去进行读取
    # 1. 获取数据(四要素) 2. 发送请求 3.获取响应数据 4.断言
    AllCaseData = FileReader.read_excel()
    ak = ApiKey()
    # 定义：all_val 存放提取出的数据
    all_var = {}

    def __dynamic_title(self, CaseData):
        # # 动态生成标题
        # allure.dynamic.title(data[11])

        # 如果存在自定义标题
        if CaseData["caseName"] is not None:
            # 动态生成标题
            # allure.dynamic.title(CaseData["caseName"])
            caseName = "CASEID:{}--{}".format(CaseData["id"], CaseData["caseName"])
            allure.dynamic.title(caseName)

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

    def __json_extraction(self, CaseData, res):
        """
        提取响应之后的数据
        :param CaseData: 当前的Case，主要获取需要提取数据的字段：jsonExData
        :param res:响应得到的对应的结果
        :return:
        """
        try:
            if CaseData["jsonExData"]:
                Exdata = eval(CaseData["jsonExData"])  # {"VAR_TOKEN":"$..token","MSG":"$.msg"}
                print("需要提取的数据：>>>", Exdata)
                for key, value in Exdata.items():
                    # 通过对应的jsonpath获取具体的数据
                    new_value = self.ak.get_text(res.json(), value)
                    self.all_var.update(
                        {key: new_value}
                    )
                print("提取出来的数据：>>>", self.all_var)
            else:
                print("需要提取的数据为空")
        except Exception:
            print("请检查你需要提取数据数据格式的正确性。")

    def __sql_extraction(self, CaseData):
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
                    new_value = self.ak.get_sqlData(value)
                    self.all_var.update(
                        {key: new_value}
                    )
                print("SQL-提取出来的数据：>>>", self.all_var)
            else:
                print("SQL-需要提取的数据为空")
        except Exception:
            print("SQL-请检查你需要提取数据数据格式的正确性。")

    def __sql_assertData(self, CaseData):
        res = True
        if CaseData["sqlAssertData"] and CaseData["sqlExpectResult"]:
            # 实际结果：从数据库读取出来的数据--字典的格式 # {"name":"SELECT username FROM sxo_user WHERE username='hami'","id":"SELECT id FROM sxo_user WHERE username='hami'"}
            realityData = eval(CaseData["sqlAssertData"])
            # 期望结果:{"name":"hami","id":75}
            expectData = json.loads(CaseData["sqlExpectResult"])

            realityDataDict = {}
            for key, value in realityData.items():
                # 通过对应的sql获取具体的数据
                new_value = self.ak.get_sqlData(value)
                realityDataDict.update(
                    {key: new_value}
                )

            if expectData != realityDataDict:
                res = False
        return res

    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    @pytest.mark.parametrize("CaseData", AllCaseData)
    def testCase(self, CaseData):
        self.__dynamic_title(CaseData)
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

            if CaseData["data"] is None:  # 会影响框架的性能
                data = None
            else:
                # 进行加密处理
                data = FileReader.data_EncryptDateAES(eval(CaseData["data"]))

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
        self.__sql_extraction(CaseData)

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
                self.__json_extraction(CaseData, res)

            else:
                value = MSG_ASSERT_NO
            FileReader.writeDataToExcel(row=row, column=column, value=value)
        finally:
            assert msg == CaseData["expectResult"], value

        # -------------------------进行数据库断言处理-------------------------------
        try:
            sqlAssertRes = self.__sql_assertData(CaseData)  # False True
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
