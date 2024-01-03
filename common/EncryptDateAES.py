# -*- coding: utf-8 -*-
# @Time : 2023/11/3 21:23
# @Author : Hami

"""
对称加密：加密和解密使用的是同一把钥匙，即：使用相同的密匙对同一密码进行加密和解密。
常用的加密方法：DES、3DES、AES...(AES算法是目前最常用的对称加密算法)
"""
import base64
from Crypto.Cipher import AES


class EncryptDate:
    # 构造方法
    def __init__(self, key):
        #  类属性
        self.key = key.encode("utf-8")  # 初始化密钥
        self.length = AES.block_size  # 初始化数据块大小 ：16位
        self.aes = AES.new(self.key, AES.MODE_ECB)  # 初始化AES,ECB模式的实例
        # 截断函数，去除填充的字符
        self.unpad = lambda date: date[0:-ord(date[-1])]

    # 缺几位数据就补齐多少位数据：16的倍数
    def pad(self, text):  # text == tony
        """
        #填充函数，使被加密数据的字节码长度是block_size的整数倍
        """
        count = len(text.encode('utf-8'))  # count = 4
        add = self.length - (count % self.length)  # 求它们相差的位数
        # add = 16- （4%16）  === 16 - 4 == 12
        entext = text + (chr(add) * add)
        #  entext = “tony” + （chr(add) * 12  ）  === entext == tony
        # print("entext的数据是:",entext)
        return entext

    # 加密函数
    def encrypt(self, encrData):  # 加密函数   encrData == tony （16位）
        res = self.aes.encrypt(self.pad(encrData).encode("utf8"))  # self.aes.encrypt(tony)
        msg = str(base64.b64encode(res), encoding="utf8")
        return msg

    # 解密函数
    def decrypt(self, decrData):  # 解密函数   XbXHJrNLwoTVcyfqM9eTgQ==
        # 从base64编码转回来
        res = base64.decodebytes(decrData.encode("utf8"))
        # 将数据进行对应的解密：XbXHJrNLwoTVcyfqM9eTgQ==
        msg = self.aes.decrypt(res).decode("utf8")
        # print("msg的值：",msg)
        # 把转回来的数据后面的字符去掉。
        return self.unpad(msg)


key = "1234567812345678"
ENCRYPTAES = EncryptDate(key)
