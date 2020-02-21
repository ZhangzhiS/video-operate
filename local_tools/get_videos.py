import paramiko
import json

import ssh_client
from settings import *
from ssh_config import ssh_map


def get_videos(hostname, username, password, port=22):
    """ 获取服务器上超过限制的视频 """
    client = ssh_client.create_ssh_client(
        hostname=hostname,
        port=port,
        username=username,
        password=password
    )
    cmd = "cd {script_path};{python_version} video_count.py".format(
        script_path=SERVER_SCRIPT_PATH,
        python_version=PYTHON,
    )
    stdin, stdout, stderr = client.exec_command(cmd)

    print("连接{hostname}服务器".format(hostname=hostname))

    data = stdout.read().decode("utf-8")
    if data:
        with open("need_slice_server.txt", "a") as af:
            af.write(hostname)
            af.write("\n")
    data = json.loads(data)
    file_name = "{hostname}.txt".format(hostname=hostname.replace(".","_"))
    with open(file_name, "w") as wd:
        # s = "videos = {videos}".format(videos=data["videos"])
        # wd.write(s)
        for  line in data["videos"]:
            # print(line)
            wd.write(line)
            wd.write("\n")
    client.close()


def read_videos(hostname):
    """查看服务器中需要切片的视频"""
    file_name = "{hostname}.txt".format(
        hostname=hostname.replace(".", "_")
    )
    with open(file_name, "r") as fb:
        data = fb.read()
        data = data.split("\n")
    return data


def main():
    for host in ssh_map:
        ssh_config = ssh_map[host]
        get_videos(
            ssh_config["hostname"],
            ssh_config["username"],
            ssh_config["password"],
            ssh_config["port"]
        )


if __name__ == '__main__':
    main()