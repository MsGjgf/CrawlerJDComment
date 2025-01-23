# _*_ coding : utf-8 _*_
# @Time : 2024/8/21 20:23
# @Author : 哥几个佛
# @File : qq_span
# @Project : CrawlerJDComment
import os
import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


def qq_span():
    # chrome_options = Options()
    # chrome_options.add_argument('--headless')
    # chrome_driver_path = Service('drivers/chromedriver129.59.exe')
    # drivers = webdriver.Chrome(options=chrome_options, service=chrome_driver_path)

    edge_options = Options()
    edge_options.add_argument('--headless')
    edge_driver_path = Service('drivers/msedgedriver-122.0.2365.59.exe')
    driver = webdriver.Chrome(options=edge_options, service=edge_driver_path)

    # drivers = webdriver.Chrome(executable_path=chrome_driver_path)

    # 最大化浏览器窗口
    # drivers.maximize_window()

    # 假设你已经有了一个可以直接访问的QQ空间URL（这里用占位符代替）
    url = 'https://user.qzone.qq.com/202478245'
    driver.get(url)

    time.sleep(5)

    # 等待iframe加载完成（可选，取决于iframe的加载方式）
    # 注意：这里的iframe_locator需要根据实际情况来定位iframe
    # 假设iframe有一个唯一的ID
    iframe_locator = (By.ID, 'login_frame')  # 替换为实际的iframe ID
    wait = WebDriverWait(driver, 10)
    iframe = wait.until(ec.presence_of_element_located(iframe_locator))

    # 切换到iframe
    driver.switch_to.frame(iframe)

    # 现在可以在iframe中查找元素了
    # 假设我们要找的元素在iframe中有一个ID 'switcher_login'
    element_locator = (By.ID, 'nick_2532127048')
    element = wait.until(ec.presence_of_element_located(element_locator))

    # 对元素进行操作，比如点击
    # element.click()

    # ... 在这里执行你的其他操作 ...
    # 现在，使用XPath的'..'来定位父元素
    parent_element = element.find_element(By.XPATH, '..')
    parent_element.click()

    ###########################################

    # 我知道了
    time.sleep(10)
    driver.refresh()

    ###################################################

    # 此时页面上的JavaScript应该已经执行完毕，可以获取页面源码
    html_source = driver.page_source

    # 截屏并保存
    now = datetime.now()
    formatted_now = now.strftime("%Y-%m-%d_%H-%M-%S")
    driver.get_screenshot_as_file(os.path.join(os.path.join(os.getcwd(), 'pics'), f"{formatted_now}.png"))

    # 打印或保存源码
    # print(html_source)
    # 或者保存到文件
    with open('static/qq_space_source.html', 'w', encoding='utf-8') as f:
        f.write(html_source)

    # 退出iframe（可选，但建议在最后执行）
    driver.switch_to.default_content()

    # 关闭浏览器
    driver.quit()


if __name__ == '__main__':
    count = 0
    while 1:
        qq_span()
        count += 1
        print(
            f'第{count}次访问QQ空间，时间：{datetime.now().year}年{datetime.now().month}月{datetime.now().day}日{datetime.now().hour}时{datetime.now().minute}分{datetime.now().second}秒')
        time.sleep(60 * 10)
