#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：api-automation-testing
@File    ：file_handle.py
@IDE     ：PyCharm
@Author  ：future76_lly
@Date    ：2024/1/3 9:29
@Desc    ：处理文件相关操作
"""

import os
import shutil
import time
import zipfile
from loguru import logger


def zip_file(in_path, out_path):
    """
    压缩指定文件夹
    :param in_path: 目标文件夹路径
    :param out_path: 压缩文件保存路径+xxxx.zip
    """
    # 如果传入的路径是一个目录才进行压缩操作
    if os.path.isdir(in_path):
        logger.debug(f"目标路径:{in_path} 是一个目录，开始进行压缩......")
        # 写入
        # 压缩文件名    以时间为名
        compressed_file_name = f'{out_path}/test_report{time.strftime("%Y%m%d%H%M%S")}.zip'

        zip = zipfile.ZipFile(compressed_file_name, "w", zipfile.ZIP_DEFLATED)
        for path, dirnames, filenames in os.walk(in_path):
            # 去掉目标跟路径，只对目标文件夹下边的文件及文件夹进行压缩
            fpath = path.replace(in_path, '')
            for filename in filenames:
                zip.write(
                    os.path.join(
                        path, filename), os.path.join(
                        fpath, filename))
        zip.close()
        logger.debug(f"目标路径:{in_path} 压缩完成！, 压缩文件路径：{out_path}")
    else:
        logger.debug(f"目标路径:{in_path} 不是一个目录，请检查！")


def copy_file(src_file_path, dest_dir_path):
    """
    复制一个文件到另一个目录
    :param: src_file_path: 源文件路径
    :param: dest_dir_path: 目标文件夹路径
    """
    # 判断源文件路径是否存在
    if not os.path.isfile(src_file_path):
        return "源文件路径不存在"

    # 判断目标文件夹路径是否存在，不存在则创建
    if not os.path.isdir(dest_dir_path):
        os.makedirs(dest_dir_path)

    # 复制文件
    try:
        shutil.copy(src_file_path, dest_dir_path)
        return "复制成功"
    except Exception as e:
        return f"复制失败：{e}"


if __name__ == '__main__':
    zip_file("../report_utils", "./")
    copy_file("../img.png", "./")
