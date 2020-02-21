#!/usr/bin/python3.6
# -*- coding: UTF-8 -*-
import os
import subprocess
import shutil

from src.load_config import LoadConfig
from src.operate import Operate as op

config = LoadConfig()


def delete_video(video_name):
    """删除某条视频 """
    try:
        file_name_str = op.create_key_str(
            file_name=video_name,
            key_str=config.FileNameKeyString
        )
        output_path = os.path.join(config.HandleMp4Path, file_name_str)
        shutil.rmtree(output_path)
        # print("done")
    except FileNotFoundError:
        try:
            file_name_str = op.create_key_str(
                file_name=os.path.join(config.OriginalMp4Path, video_name),
                key_str=config.FileNameKeyString
            )
            output_path = os.path.join(config.HandleMp4Path, file_name_str)
            shutil.rmtree(output_path)
        except FileNotFoundError:
            pass


def main():
    with open("violation.txt", "r") as fb:
        videos = fb.read()
        data = videos.split("\n")
        fb.close()
    for video in data:
        delete_video(video)
        # print("del:", video)
    os.remove("violation.txt")


if __name__ == '__main__':
    main()
