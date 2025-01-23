import concurrent.futures

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from utils.custom_logger import logger
from utils.open_browser import open_browser


def fun():
    url = ("file:///C:/Users/25321/Desktop/Web_Big/SpringBoot/SpringBootProjectes/SpringBoot-WebSocket/src/main"
           "/resources/templates/index.html")
    # 创建Chrome浏览器实例
    driver = open_browser(browser='edge', headless=True)
    driver.get(url)
    # 循环新建标签页并切换
    for i in range(1000):  # 这里以新建5个标签页为例，你可以按需修改循环次数
        # 执行JavaScript代码来新建标签页
        driver.execute_script("window.open('');")
        # 获取当前所有窗口句柄
        handles = driver.window_handles
        # 切换到最新打开的标签页（窗口）
        driver.switch_to.window(handles[-1])
        # 在当前切换到的新标签页中打开百度网址
        driver.get(url)
        logger.info(f'打开标签：{url}')
        # 等待按钮元素可见，最长等待10秒
        wait = WebDriverWait(driver, 10)
        buttons = wait.until(EC.visibility_of_all_elements_located((By.TAG_NAME, 'button')))
        buttons[0].click()
        # time.sleep(1)

    # 可以在这里添加后续操作，比如关闭浏览器等，示例如下：
    # time.sleep(5)  # 等待一段时间便于查看效果
    # driver.quit()


if __name__ == '__main__':
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=18)
    futures = [executor.submit(fun) for _ in range(18)]
