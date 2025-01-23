# _*_ coding : utf-8 _*_
# @Time : 2024/11/3 2:33
# @Author : 哥几个佛
# @File : test
# @Project : CrawlerJDComment

import psutil

from utils.custom_logger import logger


def get_cpu_percent():
    # 获取包括超线程在内的逻辑CPU数量（即线程数）
    logical_cpu_count = psutil.cpu_count(logical=True)

    # 获取不考虑超线程的物理CPU核心数
    physical_cpu_count = psutil.cpu_count(logical=False)

    print(f"逻辑CPU数量（包含超线程的线程数）: {logical_cpu_count}")
    print(f"物理CPU核心数（不考虑超线程）: {physical_cpu_count}")


if __name__ == '__main__':
    get_cpu_percent()

    import time

    print("这是原始的一行内容", end="")
    time.sleep(2)

    print("\r新的一行内容", end="")

    # 提示用户输入名字
    name = input("请输入您的名字：")
    print(f"你好, {name}!")

    logger.info("这是原始的一行内容")
    time.sleep(2)

    logger.info("\r新的一行内容")
