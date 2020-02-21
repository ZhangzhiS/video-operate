#!/usr/bin/python3.6
# -*- coding: UTF-8 -*-
import os
import datetime

from ffmpy import FFmpeg, FFExecutableNotFoundError

from src import log_str, log_print
from src.operate import Operate
from src.load_config import LoadConfig
from src.ffmpeg_cmd import FfmpegCmd
from src.thread_pool import CustomThreadPool
from src.db import DataBaseORM, Sliclog, Slicdata


def get_now_time():
    now_time_str = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    return now_time_str


class SliceVideo(object):

    def __init__(self, config_path):
        self.op = Operate()
        self.complete_count = 0
        self.start_time = get_now_time()
        self.tasks_count = 0
        self.currentstate = "init"
        self.session = None
        self.config = LoadConfig(config_path)
        self.db = None
        self.slice_id = 0
        self.tasks_order = 1

    def insert_slicelog(self, msg):
        """ 插入切片程序日志 """
        slicelog_obj = self.db.create_sliclog_obj(
            self.start_time,
            get_now_time(),
            self.tasks_count,
            self.complete_count,
            self.currentstate,
            msg,
        )
        self.session.add(slicelog_obj)
        self.session.commit()

    def init_db(self):
        """ 初始化数据库 """
        try:
            self.db = DataBaseORM(
                user=self.config.MySqlUser,
                password=self.config.MySqlPass,
                port=self.config.MySqlPort,
                host=self.config.MySqlLocal,
                db_name=self.config.MySqlDB,
            )
            # 验证数据库连接
            self.db.check_database_connect()
            # 如果第一次运行，则创建表
            if int(self.config.FirstExecution) is 0:
                self.db.create_column()
            # 获取与数据库的会话
            self.session = self.db.create_session()
            log_print(log_str.db_init)

        except Exception as e:
            error_msg = str(e)
            log_print(error_msg)
            exit()

    def check_ffmpeg(self):
        """ 检查系统中是否安装了FFmpeg """
        temp_ff = FFmpeg()
        try:
            # 运行打印ffmpeg版本的命令验证是否安装了ffmpeg
            temp_ff.cmd = "ffmpeg -loglevel quiet"
            temp_ff.run()
        except Exception as e:
            if type(e) == FFExecutableNotFoundError:
                # 如果是FFExecutableNotFoundError，则说明 ffmpeg 没安装,结束程序
                log_print(log_str.ffmpeg_not_found)
                # 将日志写入数据库
                sliclog_obj = self.db.create_sliclog_obj(
                    self.start_time, get_now_time(),
                    self.tasks_count,
                    self.complete_count,
                    self.currentstate, log_str.ffmpeg_not_found,
                )
                self.session.add(sliclog_obj)
                self.session.commit()
                self.session.close()
                # 结束程序
                exit()

    def get_video_list(self):
        """ 获取需要处理的视频列表 """
        if not self.op.check_permissions(self.config.OriginalMp4Path):
            msg = log_str.folder_error
            # 将日志写入数据库
            self.currentstate = "check input path permissions"
            self.insert_slicelog(msg)
            self.session.close()
            # 结束程序
            exit()
        else:
            data = self.op.get_not_empty_video(self.config.OriginalMp4Path)
            file_count = data["file_count"]
            if file_count == 0:
                msg = "All files have a size of 0"
                self.currentstate = "get_video_list"
                self.insert_slicelog(msg)
                self.session.close()
                log_print(msg)
                # 结束程序
                exit()
            else:
                log_print(log_str.start_log.format(tasks_count=file_count))
                video_list = data["file_list"]
                self.tasks_count = file_count
                self.currentstate = "task count"
                msg = "no abnormalities"
                self.insert_slicelog(msg)
                slicelog_obj = self.session.query(
                    Sliclog
                ).filter(
                    Sliclog.execstartctime == self.start_time
                ).one()
                self.slice_id = slicelog_obj.id
                return video_list

    @staticmethod
    def check_or_create_dir(path):
        """确认keys文件夹是否存在,不存在则创建"""
        if os.path.exists(path):
            pass
        else:
            os.mkdir(path)

    def key_operate(self, video):
        """ 有关key的操作，包括生成key以及key.info"""
        self.currentstate = "slice"
        openssl_key_str = self.op.create_key_str(
            file_name=video,
            key_str=self.config.OpensslKeyString,
        )
        filename_key_str = self.op.create_key_str(
            file_name=video,
            key_str=self.config.FileNameKeyString,
        )
        # 生成*.key文件
        self.op.create_ssl_key(
            openssl_key_str,
            self.config.KeyFilePath,
        )
        # 生成*.keyinfo文件
        keyinfo_path = self.op.create_keyinfo(
            openssl_key_str,
            self.config.Url,
            self.config.KeyFilePath,
        )
        output_path = os.path.join(
            self.config.HandleMp4Path,
            filename_key_str,
        )
        self.check_or_create_dir(output_path)
        original_file = os.path.join(
            self.config.OriginalMp4Path,
            video,
        )
        return keyinfo_path, output_path, original_file

    def update_complete_count(self):
        """更新完成的任务数量"""
        self.currentstate = "complete"
        self.session.query(
            Sliclog
        ).filter(
            Sliclog.id == self.slice_id
        ).update(
            {
                "completenumber": self.complete_count,
                "currentstate": self.currentstate
            },
            synchronize_session=False,
        )


def slice_task(input_file, output_file_path, sv, hls_key_info_file):
    """ 执行切片的函数 """
    log_print(log_str.task_numb.format(tasks_count=sv.tasks_count, task_numb=sv.tasks_order))
    sv.tasks_order += 1
    originalmp4path, input_file_name = os.path.split(input_file)
    log_print(log_str.task_start_info.format(name=input_file_name))
    # 新建slicdata对象
    create_slicdata_obj = sv.db.create_slicdata_obj(
        input_file_name,
        originalmp4path,
        output_file_path,
        hls_key_info_file,
        sv.config.FileNameKeyString,
        sv.config.OpensslKeyString,
        "0",
        sv.slice_id,
    )
    try:
        f_obj = FfmpegCmd(
            input_file=input_file,
            output_file_path=output_file_path
        )
        f_obj.add_params(hls_time=sv.config.segmenttime, hls_key_info_file=hls_key_info_file)
        f_obj.run()
        # 完成对该视频的切片，将slicdata对象的任务状态改为1
        create_slicdata_obj.status = "1"
        sv.session.add(create_slicdata_obj)
        # 切片成功的统计加1
        sv.complete_count += 1
        # 清空源文件
        sv.op.clean_video_content(input_file)
        log_print(log_str.task_end_info.format(name=input_file_name))
    except Exception as e:
        # 视频切片过程出错，在数据库中进行记录
        msg = str(e)
        temp_session = sv.db.create_session()
        temp_session.add(create_slicdata_obj)
        temp_session.commit()
        slicdata_obj = temp_session.query(
            Slicdata
        ).filter(
            Slicdata.originalmp4name == input_file_name,
            Slicdata.originalmp4path == originalmp4path,
        ).one()
        # 记录报错信息
        error_obj = sv.db.create_slicerror_obj(
            sv.slice_id,
            slicdata_obj.id,
            get_now_time(),
            msg
        )
        temp_session.add(error_obj)
        temp_session.commit()
        temp_session.close()
        log_print(msg)


def start_thread_pool(tasks, pool_size):
    """ 启动线程池任务 """
    task_thread_pool = CustomThreadPool(pool_size)
    task_thread_pool.add_task(tasks)
    task_thread_pool.add_thread()
    task_thread_pool.start_thread()
    task_thread_pool.close()


def slice_video(config):
    slice_video_obj = SliceVideo(config)
    slice_video_obj.init_db()
    slice_video_obj.check_ffmpeg()
    videos = slice_video_obj.get_video_list()
    slice_video_obj.check_or_create_dir(slice_video_obj.config.KeyFilePath)
    tasks = []
    for video in videos:
        video = os.path.split(video)[1]
        keyinfo_path, output_path, original_file = slice_video_obj.key_operate(video)
        input_file = os.path.join(slice_video_obj.config.OriginalMp4Path, video)
        temp_task = [slice_task, (input_file, output_path, slice_video_obj, keyinfo_path)]
        tasks.append(temp_task)

    # 将任务添加到线程池，并启动
    pool_size = int(slice_video_obj.config.Thread)
    start_thread_pool(tasks, pool_size)
    # 所有线程都结束之后，更新本次任务的状态
    slice_video_obj.update_complete_count()
    slice_video_obj.session.commit()
    slice_video_obj.session.close()
    log_print(log_str.end_log.format(
        count=slice_video_obj.tasks_count,
        complete=slice_video_obj.complete_count,
    )
    )
    log_print(log_str.end_program)


if __name__ == '__main__':
    con_path = "sliceconfig.ini"
    slice_video(con_path)

