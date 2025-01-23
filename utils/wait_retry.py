# _*_ coding : utf-8 _*_
# @Time : 2024/10/22 23:40
# @Author : 哥几个佛
# @File : wait_retry
# @Project : CrawlerJDComment
import logging
import time

from selenium.webdriver.common.by import By

from utils.custom_logger import logger


def is_yan_zheng(driver):
    # 获取当前页面的 URL
    current_url = driver.current_url

    # 判断 URL 是否为特定的 URL
    target_url = 'https://www.zhipin.com/web/user/safe/verify-slider?callbackUrl='
    if current_url.startswith(target_url):
        print("URL matches the condition.")
        btn = driver.find_element(By.CSS_SELECTOR, '[ka="validate_button_click"]')
        btn.click()
        time.sleep(20)
    else:
        print("URL does not match the condition.")


is_has_boss_login_close_flag = False


# 关闭弹窗
def is_has_boss_login_close(driver):
    try:
        boss_login_close_ = driver.find_element(By.CSS_SELECTOR, '.boss-login-close')
        boss_login_close_.click()
        logging.info('find_boss_login_close')
    except Exception:
        logging.error('no_find_boss_login_close')


def try_fount_css_selector(driver, selector):
    try:
        # 尝试查找包含指定文本的元素
        if is_has_boss_login_close_flag:
            is_has_boss_login_close(driver)
        is_yan_zheng(driver)
        element = driver.find_element(By.CSS_SELECTOR, selector)
        return True
    except Exception as e:
        # 如果没有找到，捕获异常并返回False
        return False


def wait_retry(driver, selector):
    while not try_fount_css_selector(driver, selector):
        print(f"未找到元素'{selector}'，等待1秒后重试...")
        driver.refresh()  # 刷新页面
        time.sleep(2)  # 等待1秒后重试
    time.sleep(5)
    is_has_boss_login_close(driver)
    result = driver.find_element(By.CSS_SELECTOR, selector)
    print(f"找到元素：{selector}->{result}")
    return result


def try_fount_css_selectors(driver, selector):
    try:
        # 尝试查找包含指定文本的元素
        if is_has_boss_login_close_flag:
            is_has_boss_login_close(driver)
        is_yan_zheng(driver)
        element = driver.find_elements(By.CSS_SELECTOR, selector)
        return True
    except Exception:
        # 如果没有找到，捕获异常并返回False
        return False


def wait_retry_s(driver, selector):
    while not try_fount_css_selectors(driver, selector):
        print(f"未找到元素'{selector}'，等待1秒后重试...")
        driver.refresh()  # 刷新页面
        time.sleep(2)  # 等待1秒后重试
    time.sleep(5)
    is_has_boss_login_close(driver)
    result = driver.find_elements(By.CSS_SELECTOR, selector)
    print(f"找到元素：{selector}->{result}")
    return result


def try_find_xpath_selector(driver, xpath):
    try:
        # 尝试查找包含指定文本的元素
        if is_has_boss_login_close_flag:
            is_has_boss_login_close(driver)
        is_yan_zheng(driver)
        element = driver.find_element(By.XPATH, xpath)
        return True
    except Exception as e:
        logger.error(e)
        # 如果没有找到，捕获异常并返回False
        return False


def wait_retry_xpath(driver, xpath):
    while not try_find_xpath_selector(driver, xpath):
        print(f"未找到元素'{xpath}'，等待1秒后重试...")
        # driver.refresh()  # 刷新页面
        time.sleep(2)  # 等待1秒后重试
    time.sleep(5)
    is_has_boss_login_close(driver)
    result = driver.find_element(By.XPATH, xpath)
    print(f"找到元素：{xpath}->{result}")
    return result


def try_find_tag_name(driver, tag_name):
    try:
        # 尝试查找包含指定文本的元素
        if is_has_boss_login_close_flag:
            is_has_boss_login_close(driver)
        is_yan_zheng(driver)
        element = driver.find_element(By.TAG_NAME, tag_name)
        return True
    except Exception as e:
        # 如果没有找到，捕获异常并返回False
        return False


def wait_retry_tag_name(driver, tag_name):
    while not try_find_tag_name(driver, tag_name):
        print(f"未找到元素'{tag_name}'，等待1秒后重试...")
        driver.refresh()  # 刷新页面
        time.sleep(2)  # 等待1秒后重试
    time.sleep(5)
    is_has_boss_login_close(driver)
    result = driver.find_element(By.TAG_NAME, tag_name)
    print(f"找到元素：{tag_name}->{result}")
    return result
