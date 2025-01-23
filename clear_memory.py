# 安装：pip install pyautogui -i https://pypi.tuna.tsinghua.edu.cn/simple
import time

import psutil
import pyautogui

from utils.open_browser import open_browser


def click_fast_ball():
    # 假设你已经确定了加速球在屏幕上的坐标（x, y）
    # 这里只是示例坐标，你需要根据实际情况进行调整
    accelerate_ball_x = 1870  # 假设的屏幕宽度为1920，加速球在右侧
    accelerate_ball_y = 976  # 假设的屏幕高度为1080，加速球在任务栏附近
    # accelerate_ball_x = 500  # 假设的屏幕宽度为1920，加速球在右侧
    # accelerate_ball_y = 500  # 假设的屏幕高度为1080，加速球在任务栏附近

    # 给一点时间切换到桌面并找到加速球
    time.sleep(5)

    # 移动鼠标到加速球的位置
    pyautogui.moveTo(accelerate_ball_x, accelerate_ball_y, duration=1)

    # 等待一点时间以确保鼠标已经到达目标位置
    time.sleep(2)

    # 点击鼠标左键
    # pyautogui.click()

    # 如果需要，还可以执行其他操作，比如双击或右键点击
    pyautogui.doubleClick()
    # pyautogui.rightClick()


def clear_memory():
    # 获取物理内存信息
    memory = psutil.virtual_memory()

    # 打印总内存、可用内存等信息
    print(f"Total memory: {memory.total / (1024 ** 3):.2f} GB")
    print(f"Available memory: {memory.available / (1024 ** 3):.2f} GB")
    print(f"Used memory: {(memory.total - memory.available) / (1024 ** 3):.2f} GB")
    print(f"Percentage: {memory.percent}%")
    while 1:
        driver = open_browser()
        driver.get("https://www.jd.com")
        # 获取物理内存信息
        memory = psutil.virtual_memory()
        print(memory.percent)
        if memory.percent >= 50:
            click_fast_ball()
        time.sleep(1)


if __name__ == '__main__':
    clear_memory()
