import os
import time

# import torch

import threading

# print(torch.cuda.is_available())
#
# lock = threading.Lock()
# #python激活虚拟环境
# i=0
# def deal():
#     global i
#     # for t in range(100):
#     lock.acquire()
#     os.system('conda activate paddle')
#     time.sleep(1)
#     os.system('pip -V')
#     lock.release()
# def deal2():
#     global i
#     # for t in range(100):
#     lock.acquire()
#     os.system('pip -V')
#     lock.release()
# job1 = threading.Thread(target=deal)
# job2 = threading.Thread(target=deal2)
# job2.start()
# job1.start()

import subprocess

def run_command(command):
    # 使用 subprocess 运行系统命令
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if process.returncode == 0:
        print("成功执行命令：", command)
        print("输出：\n", stdout.decode('utf-8'))
    else:
        print("执行命令失败：", command)
        print("错误信息：\n", stderr.decode('utf-8'))

def main():
    # 定义要在子线程中运行的系统命令
    commands = ["conda activate dl", "pip list", "pwd"]

    # 创建一个线程列表
    threads = []

    # 为每个命令创建一个线程，并添加到线程列表中
    for command in commands:
        thread = threading.Thread(target=run_command, args=(command,))
        threads.append(thread)

    # 启动所有线程
    for thread in threads:
        thread.start()

    # 等待所有线程完成
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()


