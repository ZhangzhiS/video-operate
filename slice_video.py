#!/usr/bin/python3.6
# -*- coding: UTF-8 -*-
import os
import json
import subprocess


def start():
    try:
        subprocess.Popen(["python3", "slice.py"])
        print("success")
        data = {
            "msg": "切片程序已启动",
        }
    except Exception as e:
        data = {
            "msg": "切片程序异常",
            "err_data": str(e)
        }
    return data


if __name__ == '__main__':
    data = start()
    # print(json.dumps(data))
