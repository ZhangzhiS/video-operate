#!/usr/bin/python3.6
# -*- coding: UTF-8 -*-

"""
字符串常量
"""

class LogStr(object):
    start_log = "\n\n共有{tasks_count:^}个视频\n"
    task_numb = "共有{tasks_count}个视频，现在开始第{task_numb}个"
    task_start_info = "正在对《{name}》进行切片"
    task_end_info = "任务《{name}》已完成"
    end_log = "\n\n共有{count}个视频被执行，{complete}个成功\n\n"
    db_init = "DB inited"
    ffmpeg_not_found = "'ffmpeg' not found"
    folder_error = "permissions error or folder not found"
    end_program = "------结束程序------"
