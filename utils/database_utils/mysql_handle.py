#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：api-automation-testing 
@File    ：mysql_handle.py
@IDE     ：PyCharm 
@Author  ：future76_lly
@Date    ：2023/12/25 15:08
使用pymysql模块连接mysql数据库的公共方法
'''
import pymysql
from typing import Union
import json
from datetime import datetime
from sshtunnel import SSHTunnelForwarder
from loguru import logger


class MysqlServer:
    """
    初始化数据库连接(支持通过SSH隧道的方式连接)，并指定查询的结果集以字典形式返回
    """

    def __init__(self, db_host, db_port, db_user, db_pwd, db_database, ssh=False,
                 **kwargs):
        """
        初始化方法中， 连接mysql数据库， 根据ssh参数决定是否走SSH隧道方式连接mysql数据库
        """
        self.server = None
        if ssh:
            self.server = SSHTunnelForwarder(
                ssh_address_or_host=(kwargs.get("ssh_host"), kwargs.get("ssh_port")),  # ssh 目标服务器 ip 和 port
                ssh_username=kwargs.get("ssh_user"),  # ssh 目标服务器用户名
                ssh_password=kwargs.get("ssh_pwd"),  # ssh 目标服务器用户密码
                remote_bind_address=(db_host, db_port),  # mysql 服务ip 和 part
                local_bind_address=('127.0.0.1', 5143),  # ssh 目标服务器的用于连接 mysql 或 redis 的端口，该 ip 必须为 127.0.0.1
            )
            self.server.start()
            db_host = self.server.local_bind_host  # server.local_bind_host 是 参数 local_bind_address 的 ip
            db_port = self.server.local_bind_port  # server.local_bind_port 是 参数 local_bind_address 的 port
        # 建立连接
        self.conn = pymysql.connect(host=db_host,
                                    port=db_port,
                                    user=db_user,
                                    password=db_pwd,
                                    database=db_database,
                                    charset="utf8",
                                    cursorclass=pymysql.cursors.DictCursor  # 加上pymysql.cursors.DictCursor这个返回的就是字典
                                    )
        # 创建一个游标对象
        self.cursor = self.conn.cursor()

    def query_all(self, sql):
        """
        查询所有符合sql条件的数据
        :param sql: 执行的sql
        :return: 查询结果
        """
        try:
            self.conn.commit()
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            # 关闭数据库链接和隧道
            self.close()
            return self.verify(data)
            # return data
        except Exception as e:
            logger.error(f"查询所有符合sql条件的数据报错: {e}")
            raise e

    def query_one(self, sql):
        """
        查询符合sql条件的数据的第一条数据
        :param sql: 执行的sql
        :return: 返回查询结果的第一条数据
        """
        try:
            self.conn.commit()
            self.cursor.execute(sql)
            data = self.cursor.fetchone()
            # 关闭数据库链接和隧道
            self.close()
            return self.verify(data)
            # return data
        except Exception as e:
            logger.error(f"查询符合sql条件的数据的第一条数据报错: {e}")
            raise e

    def insert(self, sql):
        """
        插入数据
        :param sql: 执行的sql
        """
        try:
            self.cursor.execute(sql)
            # 提交  只要数据库更新就要commit
            self.conn.commit()
            # 关闭数据库链接和隧道
            self.close()
        except Exception as e:
            logger.error(f"插入数据报错: {e}")
            raise e

    def update(self, sql):
        """
        更新数据
        :param sql: 执行的sql
        """
        try:
            self.cursor.execute(sql)
            # 提交 只要数据库更新就要commit
            self.conn.commit()
            # 关闭数据库链接和隧道
            self.close()
        except Exception as e:
            logger.error(f"更新数据报错: {e}")
            raise e

    def query(self, sql, one=True):
        """
        根据传值决定查询一条数据还是所有
        :param sql: 查询的SQL语句
        :param one: 默认True. True查一条数据，否则查所有
        :return:
        """
        try:
            if one:
                return self.query_one(sql)
            else:
                return self.query_all(sql)
        except Exception as e:
            logger.error(f"查询数据报错: {e}")
            raise e

    def close(self):
        """
        断开游标，关闭数据库
        如果开启了SSH隧道，也关闭
        :return:
        """
        # 关闭游标
        self.cursor.close()
        # 关闭数据库链接
        self.conn.close()
        # 如果开启了SSH隧道，则关闭
        if self.server:
            self.server.close()
    # 暂时注释掉
    def verify(self, result):
        """验证结果能否被json.dumps序列化"""
        # 尝试变成字符串，解决datetime 无法被json 序列化问题
        try:
            json.dumps(result)
        except TypeError as e:  # TypeError: Object of type datetime is not JSON serializable
            logger.info(f"datetime无法被json序列化：{e},接下来将datetime进行转换")
            if isinstance(result, dict):
                for k, v in result.items():
                    if isinstance(v, datetime):
                        result[k] = str(v)
            elif isinstance(result, list):
                for i in result:
                    for k, v in i.items():
                        if isinstance(v, datetime):
                            i[k] = str(v)
        # except AttributeError: # 'list' object has no attribute 'items'
        #     for i in result:
        #         for k, v in i.items():
        #             if isinstance(v, datetime):
        #                 result[k] = str(v)
        return result


if __name__ == '__main__':
    # 以下调试链接方式，请使用自己的测试数据库配置进行测试。
    # ----------需要走SSH隧道的数据库---------------
    db_host = "pc-bp1avf10pbl2ygn49.rwlb.rds.aliyuncs.com"
    db_port = 3306
    db_user = "u_customerportrait_read"
    db_pwd = "ZS2Ka4E3%w5%qk5%"
    db_database = "neighbour_jingtun_igb"
    ssh = True
    ssh_info = {
        "ssh_host": "47.114.181.194",
        "ssh_port": 52666,
        "ssh_user": "neighbour-ssh",
        "ssh_pwd": "&86JSeDw1Jb!I3nX"
    }

    # --------------------------------------------------------------
    # db_host = "pc-bp1avf10pbl2ygn49.rwlb.rds.aliyuncs.com"
    # db_port = 3306
    # db_user = "jingtun_read"
    # db_pwd = "FnGZY1vk"
    # db_database = "neighbour_jingtun"
    # ssh = True
    # ssh_info = {
    #     "ssh_host": "47.114.181.194",
    #     "ssh_port": 52666,
    #     "ssh_user": "neighbour-ssh",
    #     "ssh_pwd": "&86JSeDw1Jb!I3nX"
    # }

    # ----------不需要走SSH隧道的数据库---------------
    # db_host = "127.0.0.1"
    # db_port = 3306
    # db_user = "root"
    # db_pwd = "123456"
    # db_database = "mytools"
    # ssh = False

    db = MysqlServer(db_host, db_port, db_user, db_pwd, db_database, ssh,
                     **ssh_info)
    # print(db.query(sql="select * from ad_alias_number_batch ;",one=True))
    print(db.query(sql="select * from igb_business_target_batch_record_reset ;",one=False))