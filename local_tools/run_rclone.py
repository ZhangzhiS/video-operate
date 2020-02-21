#!/usr/bin/python3.6
# -*- coding: UTF-8 -*-
from ssh_config import ssh_map
import ssh_client
from settings import *


def rclone(hostname, username, password, port=22):
    """ 启动切片程序 """
    client = ssh_client.create_ssh_client(
        hostname=hostname,
        port=port,
        username=username,
        password=password
    )
    cmd = "cd {script_path};{rclione_cmd}".format(
        script_path=RCLONE,
        rclione_cmd=RCLONE_CMD
    )
    # print(cmd)
    client.exec_command(cmd)
    #
    data = "服务器{hostname}：rclone命令已经发送".format(hostname=hostname)
    # data = stdout.readlines()
    # if not data:
    #     data = stderr.read()
    # print(json.loads(data))
    # print(data)
    client.close()
    return data

def main():
    for host in ssh_map:
        ssh_config = ssh_map[host]
        rclone(
            ssh_config["hostname"],
            ssh_config["username"],
            ssh_config["password"],
            ssh_config["port"]
        )


if __name__ == '__main__':
    main()