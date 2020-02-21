#!/usr/bin/python3.6
# -*- coding: UTF-8 -*-
import os
import ssh_client
from ssh_config import ssh_map
from settings import *


def run_del_cmd(hostname, username, password, port=22):
    client = ssh_client.create_ssh_client(
        hostname=hostname,
        port=port,
        username=username,
        password=password
    )
    cmd = "cd {script_path};{python_version} delete_videos.py".format(
        script_path=SERVER_SCRIPT_PATH,
        python_version=PYTHON,
    )
    client.exec_command(cmd)
    data = "服务器{hostname}：删除命令已经发送".format(hostname=hostname)
    print(data)


def put_video_name(hostname, username, password, port=22):
    sftp_client = ssh_client.create_sftp_client(hostname, username, password, port)
    p = os.getcwd()
    # 本地路径
    local_path = os.path.join(p, "violation.txt")
    # 远程路径
    remote_path = os.path.join(SERVER_SCRIPT_PATH, "violation.txt")
    sftp_client.put(local_path, remote_path)
    run_del_cmd(hostname, username, password, port)


def start_del():
    for host in ssh_map:
        ssh_config = ssh_map[host]
        put_video_name(
            ssh_config["hostname"],
            ssh_config["username"],
            ssh_config["password"],
            ssh_config["port"]
        )


if __name__ == '__main__':
    start_del()