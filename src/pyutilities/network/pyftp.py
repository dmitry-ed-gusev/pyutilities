#!/usr/bin/env python3
# -*- coding=utf-8 -*-

"""
    FTP/SFTP Client in python.

    Useful documentation:
        - ???

    Created:  Dmitrii Gusev, 22.11.2022
    Modified: Dmitrii Gusev, 27.11.2022
"""

import paramiko
from pyutilities.logging import init_logging


def sft_process():
    host = "92.53.96.211"
    user = "cp23965_pult"
    password = ""
    commands = ["cd ~", "pwd", "whoami"]

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(
        host,
        port=21,
        username=user,
        password=password,
        sock=paramiko.ProxyCommand("ssh webproxy.merck.com:8080 nc %h %p"),
    )
    # ssh.connect(host, port=2022, username=user, password=password)

    stdin, stdout, stderr = ssh.exec_command("; ".join(commands))
    print("stdin -> ", stdin)

    # sftp = ssh.open_sftp()
    # print("sftp opened...")
    # sftp.get(remote_fname, local_fname)  # get a file from server
    # sftp.put(local_fname, new_remote_fname)  # upload a file on server
    # ssh.close()


def ftp_process():
    pass


def pyftp():
    print("pyftp running... not implemented yet!")


if __name__ == "__main__":
    init_logging()
    pyftp()
