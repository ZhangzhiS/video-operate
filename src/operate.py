#!/usr/bin/python3.6
# -*- coding: UTF-8 -*-

import os
import ssl
from hashlib import md5


class Operate(object):
    """文件的一些操作"""

    @staticmethod
    def check_permissions(file_path):
        """检查文件夹权限"""
        permissions = os.access(file_path, os.R_OK)
        return permissions

    @staticmethod
    def get_not_empty_video(file_path):
        """获取不为空的文件列表"""
        file_list = os.listdir(file_path)
        not_empty_list = []
        for file in file_list:
            if not os.path.isdir(file):
                temp = os.path.join(file_path, file)
                if os.path.getsize(temp) > 0:
                    # 筛选mp4文件
                    if ".mp4" in file or ".MP4" in file:
                        not_empty_list.append(temp)
        data = {
            "file_list": not_empty_list,
            "file_count": len(not_empty_list)
        }
        return data

    @staticmethod
    def create_key_str(file_name, key_str):
        """生成需要的key"""
        m = md5()
        data = "{file_name}|{key_str}".format(file_name=file_name, key_str=key_str)
        m.update(data.encode("UTF-8"))
        key = m.hexdigest()
        return key

    @staticmethod
    def create_ssl_key(filename, path):
        """创建*.key文件"""
        ssl_key = ssl.RAND_bytes(16)
        with open(os.path.join(path, filename + ".key"), "wb") as w:
            w.write(ssl_key)

    @staticmethod
    def create_keyinfo(filename, url, path):
        """创建*.keyinfo文件"""
        VI = ''.join([('0' + hex(ord(os.urandom(1)))[2:])[-2:] for x in range(16)])
        keyinfo_path = os.path.join(path, filename + ".keyinfo")
        with open(keyinfo_path, "w") as w:
            w.write(os.path.join(url, filename + ".key") + "\n")
            w.write(os.path.join(path, filename + ".key") + "\n")
            w.write(VI)
        return keyinfo_path

    @staticmethod
    def clean_video_content(filename):
        """清空文件内容"""
        with open(filename, "wb") as cl:
            cl.truncate()
            cl.close()
