#!/usr/bin/python3.6
# -*- coding: UTF-8 -*-
import paramiko


def create_ssh_client(hostname, username, password, port=22):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(
        hostname=hostname,
        port=port,
        username=username,
        password=password
    )
    return client


def create_sftp_client(hostname, username, password, port=22):
    transport = paramiko.Transport(hostname, port)
    transport.connect(username=username, password=password)
    client = paramiko.SFTPClient.from_transport(transport)
    return client

