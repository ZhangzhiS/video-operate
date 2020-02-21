#!/usr/bin/python3.6
# -*- coding: UTF-8 -*-

"""
加载配置文件
"""

import os
try:
    import configparser
except:
    import ConfigParser as configparser


class LoadConfig(object):
    """ 加载配置文件 """

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super(LoadConfig, cls).__new__(cls)
        return cls._instance

    def __init__(self, configfile_path="sliceconfig.ini"):
        if os.path.exists(configfile_path):
            config_obj = configparser.ConfigParser()
            try:
                config_obj.read(configfile_path, encoding="utf-8")
            except:
                config_obj.read(configfile_path)
            try:
                self.MySqlUser = config_obj.get("SliceConfig", "MySqlUser")
                self.MySqlLocal = config_obj.get("SliceConfig", "MySqlLocal")
                self.MySqlPort = config_obj.get("SliceConfig", "MySqlPort")
                self.MySqlPass = config_obj.get("SliceConfig", "MySqlPass")
                self.MySqlDB = config_obj.get("SliceConfig", "MySqlDB")
                self.FirstExecution = config_obj.get("SliceConfig", "FirstExecution")
                self.OriginalMp4Path = config_obj.get("SliceConfig", "OriginalMp4Path")
                self.HandleMp4Path = config_obj.get("SliceConfig", "HandleMp4Path")
                self.KeyFilePath = config_obj.get("SliceConfig", "KeyFilePath")
                self.FileNameKeyString = config_obj.get("SliceConfig", "FileNameKeyString")
                self.OpensslKeyString = config_obj.get("SliceConfig", "OpensslKeyString")
                self.FirstExecution = config_obj.get("SliceConfig", "FirstExecution")
                self.Thread = config_obj.get("SliceConfig", "Thread")
                self.segmenttime = config_obj.get("SliceConfig", "segmenttime")
                self.Url = config_obj.get("SliceConfig", "Url")
                self.limit_size = config_obj.get("SliceConfig", "limit_size")
            except configparser.NoOptionError as e:
                print(e)
        else:
            print("not found")
            exit()


if __name__ == "__main__":
    config_path = "../sliceconfig.ini"
    c = LoadConfig(config_path)
    print(c.FileNameKeyString)
