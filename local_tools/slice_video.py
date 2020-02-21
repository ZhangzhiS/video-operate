import ssh_client
from settings import *
from ssh_config import ssh_map


def start_by_ssh(hostname, username, password, port=22):
    """ 启动切片程序 """
    client = ssh_client.create_ssh_client(
        hostname=hostname,
        port=port,
        username=username,
        password=password
    )
    cmd = "cd {script_path};{python_version} slice_video.py".format(
        script_path=SERVER_SCRIPT_PATH,
        python_version=PYTHON
    )
    client.exec_command(cmd)
    data = "服务器{hostname}：执行切片命令已经发送".format(hostname=hostname)
    print(data)
    client.close()


def main():
    with open("need_slice_server.txt", "r") as rf:
        need_slice_server = rf.readlines()
        for host in need_slice_server:
            ssh_config = ssh_map[host.replace("\n", "")]
            start_by_ssh(
                ssh_config["hostname"],
                ssh_config["username"],
                ssh_config["password"],
                ssh_config["port"]
            )
        rf.close()
    with open("need_slice_server.txt", "w") as cl:
        cl.truncate()



if __name__ == '__main__':
    data = main()
