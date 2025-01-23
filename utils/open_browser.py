# _*_ coding : utf-8 _*_
# @Time : 2024/10/25 9:22
# @Author : 哥几个佛
# @File : open_browser
# @Project : CrawlerJDComment
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService

CHROME_DRIVER_PATH = r'E:\PythonProjects\CrawlerJDComment\drivers\chromedriver-131.exe'
EDGE_DRIVER_PATH = r'E:\PythonProjects\CrawlerJDComment\drivers\msedgedriver-122.0.2365.59.exe'
FIREFOX_DRIVER_PATH = ''


def open_browser(
        browser='chrome',
        headless=False,
        proxy=None,
        user_agent=None
):
    """
    打开一个浏览器实例。

    :param browser: 指定浏览器
    :param headless: 是否启用无头模式
    :param proxy: 代理 IP 地址，格式为 'ip:port'
    :param user_agent: 用户代理字符串
    :return: WebDriver 对象
    """

    if browser == 'chrome':
        # 配置 Chrome 选项
        options = ChromeOptions()

        # 指定 ChromeDriver 的路径
        service = ChromeService(executable_path=CHROME_DRIVER_PATH)
    elif browser == 'edge':
        # 配置 Edge 选项
        options = EdgeOptions()

        # 指定 EdgeDriver 的路径
        service = EdgeService(executable_path=EDGE_DRIVER_PATH)
    else:
        # 假设写错字符串
        raise ValueError("Unsupported browser. Choose 'chrome' or 'edge'.")

    # 设置代理
    if proxy:
        options.add_argument(f'--proxy-server={proxy}')
    options.add_experimental_option("excludeSwitches", ['enable-automation'])   # 关闭chrome自动化检测

    # 设置用户代理
    if user_agent:
        options.add_argument(f'user-agent={user_agent}')

    # 启用无头模式
    if headless:
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')

    # 创建 WebDriver 对象
    if browser == 'chrome':
        return webdriver.Chrome(service=service, options=options)
    elif browser == 'edge':
        return webdriver.Edge(service=service, options=options)


# 示例用法
if __name__ == "__main__":
    # 配置参数
    browser = 'chrome'
    headless = False
    proxy = 'http://18.223.25.15:80'
    user_agent = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/58.0.3029.110 Safari/537.3')

    # 打开浏览器实例
    driver = open_browser(browser=browser, headless=headless, proxy=None, user_agent=user_agent)

    try:
        # 打开目标网页
        driver.get('https://www.baidu.com')

        # 将浏览器窗口最大化
        driver.maximize_window()

        # 等待页面加载完成
        driver.implicitly_wait(10)

        # 执行后续操作
        time.sleep(5)
        print(dir(driver))
        for attr in dir(driver):
            try:
                value = getattr(driver, attr)
                print(f"{attr}: {value}")
            except Exception as e:
                print(f"Could not get value for {attr}: {str(e)}")

    finally:
        # 关闭浏览器
        driver.quit()
