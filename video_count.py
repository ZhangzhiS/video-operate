#!/usr/bin/python3.6
# -*- coding: UTF-8 -*-
import os
import json

from src.load_config import LoadConfig

config = LoadConfig()


def more_than_limit():
    input_path = config.OriginalMp4Path
    limit_size = config.limit_size
    limit_size_bytes = int(limit_size)*1024*1024
    file_list = os.listdir(input_path)
    largest_limit_files = [file for file in file_list if os.path.getsize(os.path.join(input_path, file)) > limit_size_bytes]
    data = {"videos": largest_limit_files}
    return json.dumps(data)


if __name__ == '__main__':
    a = more_than_limit()
    print(a)