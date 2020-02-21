#!/usr/bin/python3.6
# -*- coding: UTF-8 -*-

import os

from ffmpy import FFmpeg


class FfmpegCmd(object):
    """拼接视频切片需要的命令"""

    def __init__(self, input_file, output_file_path, input_cmd="-y -loglevel quiet", output_cmd="", output_name="index.m3u8"):
        """
        初始化
        :param input_file: 输入文件
        :param output_file_path: 输出文件
        :param input_cmd: 输入文件需要带的参数，-y （global）：默认自动覆盖输出文件，而不再询问确认。
        :param output_cmd: 输出文件需要的参数
        """
        self.input_file = input_file
        self.input = dict()
        self.input_cmd = [input_cmd]
        self.output_file_path = output_file_path
        self.output = dict()
        self.output_cmd = [output_cmd]
        self.output_name = os.path.join(output_file_path, output_name)


    def codec_schema(self, stream="-c", schema="copy"):
        """
        为特定的文件选择编/解码模式
        :param stream: 数据流选择 ”-c“指全部输入
        :param schema: 输出选项 “copy” 流数据直接复制不再编码
        """
        self.output_cmd.append(stream)
        self.output_cmd.append(schema)

    def bit_filter(self, stream="v", bitstream_filters="h264_mp4toannexb"):
        """
        为每个匹配流设置bit流滤镜
        :param stream: 流选择
        :param bitstream_filters: 滤镜
        """
        start_cmd = "-bsf:"
        start_cmd = start_cmd+stream
        self.output_cmd.append(start_cmd)
        self.output_cmd.append(bitstream_filters)

    def map_select(self, stream="0"):
        """
        设定一个或者多个输入流作为输出流的源
        :param stream:
        """
        cmd = "-map"
        self.output_cmd.append(cmd)
        self.output_cmd.append(stream)

    def hls_select(self, hls_time, hls_key_info_file, hls_list_size=0, hls_segment_filename="%03d.ts"):
        """
        HLS分割选项
        :param hls_time: 每段ts的时长
        :param hls_segment_filename: ts的命名规则
        :param hls_key_info_file: keyInfo的路径
        :param hls_list_size: 设置播放列表中字段最大数，0为全部分段
        """

        hls_time_cmd = "-hls_time %s" % hls_time
        hls_key_info_file = "-hls_key_info_file %s" % hls_key_info_file
        hls_list_size = "-hls_list_size %s" % hls_list_size
        hls_segment_filename = "-hls_segment_filename %s" % os.path.join(self.output_file_path, hls_segment_filename)
        self.output_cmd += [hls_time_cmd, hls_list_size, hls_key_info_file, hls_segment_filename]

    def join_cmd(self):
        """拼接命令"""
        self.input_cmd = " ".join(self.input_cmd)
        self.output_cmd = " ".join(self.output_cmd)
        self.input[self.input_file] = self.input_cmd
        self.output[self.output_name] = self.output_cmd+" -hls_flags round_durations "

    def add_params(self, hls_time, hls_key_info_file):
        """打包命令"""
        self.codec_schema()
        self.bit_filter()
        self.map_select()
        self.hls_select(hls_time=hls_time, hls_key_info_file=hls_key_info_file)
        self.join_cmd()

    def run(self):
        """执行切片任务"""
        ff = FFmpeg(
            inputs=self.input,
            outputs=self.output
        )
        ff.run()
