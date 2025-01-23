# _*_ coding : utf-8 _*_
# @Time : 2025/1/14 1:41
# @Author : 哥几个佛
# @File : open_exist_browser
# @Project : CrawlerJDComment
import subprocess
import traceback

from selenium import webdriver
from selenium.common import SessionNotCreatedException
from selenium.webdriver.chrome.service import Service as ChromeService

from utils.custom_logger import logger

CHROME_DRIVER_PATH = r'E:\PythonProjects\CrawlerJDComment\drivers\chromedriver-131.exe'
EDGE_DRIVER_PATH = r'E:\PythonProjects\CrawlerJDComment\drivers\msedgedriver-122.0.2365.59.exe'
FIREFOX_DRIVER_PATH = ''

"""
    命令行手动打开浏览器（否则无法与selenium建立连接==>SYN_SENT）
"""


def start_chrome_with_debug_port():
    chrome_exe_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    debug_port = 9222
    try:
        # 使用 subprocess.Popen 执行命令
        subprocess.Popen([chrome_exe_path, "--remote-debugging-port=" + str(debug_port)])
        logger.info(f"Chrome started with remote debugging on port {debug_port}")
    except Exception as e:
        logger.error(f"Failed to start Chrome: {e}")
    #     # 使用 subprocess.Popen 执行命令并添加 --headless 选项
    #     subprocess.Popen([chrome_exe_path, "--remote-debugging-port=" + str(debug_port), "--headless"])
    #     logger.info(f"Chrome started with remote debugging on port {debug_port} in headless mode")
    # except Exception as e:
    #     logger.error(f"Failed to start Chrome: {e}")
    pass


def open_exist_browser():
    # 手动打开浏览器
    start_chrome_with_debug_port()

    options = webdriver.ChromeOptions()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    service = ChromeService(executable_path=CHROME_DRIVER_PATH)
    try:
        driver = webdriver.Chrome(service=service, options=options)
        return driver
    except SessionNotCreatedException as e:
        print(e)
        traceback.print_exc()
