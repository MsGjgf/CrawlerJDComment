# _*_ coding : utf-8 _*_
# @Time : 2024/8/25 20:03
# @Author : 哥几个佛
# @File : qq_bot
# @Project : CrawlerJDComment

# 使用psutil来判断QQ是否登录
import os
import time

import psutil
import pyautogui
import pyautogui as gui
import pyperclip

people = '2532127048'  # 好友全称
message = 'Hello World！'  # 发送的消息

QQ_dir = r'D:\LenovoQMDownload\SoftMgr\Tencent\QQ\Bin\QQ.exe'  # QQ路径


# 判断QQ是否登录
def proc_exist(process_name):
    pl = psutil.pids()
    for pid in pl:  # 通过PID判断
        if psutil.Process(pid).name() == process_name:
            return isinstance(pid, int)


# 发送消息
def send_msg(peo, msg):
    if proc_exist('QQ.exe'):
        # 打开QQ主界面
        gui.hotkey('ctrl', 'alt', 'z')
        time.sleep(0.5)
        pyautogui.write(peo, interval=0.1)
        time.sleep(0.5)
        gui.hotkey('Enter')
    else:
        # 登录QQ
        qq_login()

    pyperclip.copy(msg)
    count = 10
    while count > 0:
        count -= 1
        gui.hotkey('ctrl', 'v')
        gui.hotkey('ctrl', 'Enter')

    # 隐藏主界面并退出聊天界面
    gui.hotkey('ctrl', 'w')


# 登录QQ
def qq_login():
    os.startfile(QQ_dir)
    print('正在打开QQ')
    time.sleep(3)
    gui.hotkey('Enter')
    time.sleep(10)


if __name__ == "__main__":
    send_msg(people, message)
