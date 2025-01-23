import os
import sys
import threading
import time
import traceback
from datetime import datetime
import requests
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from utils.custom_logger import logger
from utils.open_browser import open_browser
from utils.open_exist_browser import open_exist_browser
from utils.send_email import EmailSender
from utils.wait_retry import wait_retry, wait_retry_s, wait_retry_xpath, wait_retry_tag_name, is_has_boss_login_close, \
    try_fount_css_selector

# 定义非法字符及其替换字符
illegal_chars = {
    '<': '_',
    '>': '_',
    ':': '_',
    '"': '_',
    '/': '_',
    '\\': '_',
    '|': '_',
    '?': '_',
    '*': '_'
}

flag = True


def check_text_presence(driver, text):
    """
    检查页面中是否存在指定的文字。
    :param driver: WebDriver实例
    :param text: 要查找的文字
    :return: 如果找到返回True，否则返回False
    """
    try:
        # 尝试查找包含指定文本的元素
        element = driver.find_element(By.XPATH, f"//*[contains(text(), '{text}')]")
        return True
    except Exception:
        # 如果没有找到，捕获异常并返回False
        return False


'''
# 配置Chrome选项
chrome_options = Options()
# chrome_options.add_argument("--headless")  # 无头模式，后台运行

# 指定ChromeDriver的路径
service = Service('drivers/chromedriver129.exe')

# 创建WebDriver对象
drivers = webdriver.Chrome(service=service, options=chrome_options)

try:
    # 打开百度
    drivers.get('https://www.zhipin.com/web/geek/job-recommend?city=100010000&experience=102&jobType=1901')

    # 要查找的文字
    target_text = '谢远程'

    # 循环检查页面是否包含目标文字
    while not check_text_presence(drivers, target_text):
        print(f"未找到文字'{target_text}'，等待1秒后重试...")
        time.sleep(1)  # 等待1秒后重试

    print(f"找到了文字'{target_text}'，可以继续执行下一步操作。")

    # 开始执行逻辑

    # 这里可以添加更多的操作，比如点击某个按钮等

finally:
    # 关闭浏览器
    # drivers.quit()
    print()
'''

previous_thread = None


def login(driver):
    # 要查找的文字
    global previous_thread
    target_text = '谢远程'

    # 判断是否二维码页面
    def is_two_dimensional_code():
        try:
            qr_code_box = WebDriverWait(driver, 10).until(
                ec.presence_of_element_located((By.CSS_SELECTOR, '.qr-code-box'))
            )
            return True
        except TimeoutException:
            return False

    # 等待并获取.btn-sign-switch元素，设置最长等待时间为10秒（可根据实际调整）
    toggle = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.CSS_SELECTOR, '.btn-sign-switch'))
    )
    while not is_two_dimensional_code():
        toggle.click()
        time.sleep(1)
        pass

    # 循环检查页面是否包含目标文字
    while not check_text_presence(driver, target_text):
        try:
            # 等待.invalid-box button元素出现，最长等待10秒
            btn = WebDriverWait(driver, 10).until(
                ec.presence_of_element_located((By.CSS_SELECTOR, '.invalid-box button'))
            )
            btn.click()
            time.sleep(2)  # 点击后等待5秒，给页面一些响应时间，可根据实际调整
            continue
        except Exception:
            try:
                # 等待.qr-code-box img元素出现，最长等待10秒
                img = WebDriverWait(driver, 10).until(
                    ec.presence_of_element_located((By.CSS_SELECTOR, '.qr-code-box img'))
                )
                src = img.get_attribute('src')
                print(src)

                def open_url(url):
                    print(f"正在打开URL: {url}")
                    dri = open_browser()
                    dri.get(url)
                    time.sleep(30)

                # 如果之前存在线程，先尝试将其关闭（这里简单使用join方法等待线程结束来模拟关闭，实际情况可能更复杂，比如线程中有循环等不会自然结束的情况，需要更合理地终止策略）
                if previous_thread and previous_thread.is_alive():
                    previous_thread.join()

                # 创建一条新线程
                thread = threading.Thread(target=open_url, args=(src,))
                thread.start()

                # 将当前新创建的线程赋值给previous_thread，以便下次循环时处理
                previous_thread = thread

            except Exception:
                continue
                pass

        print(f"未找到文字'{target_text}'，等待1秒后重试...")
        time.sleep(1)  # 等待1秒后重试

        # image.app.run(debug=True)

    print(f"找到了文字'{target_text}'，可以继续执行下一步操作。")

    # 返回原来的标签页（即最初打开百度的那个标签页）
    # driver.switch_to.window(driver.window_handles[0])

    driver.get('https://www.zhipin.com')


def bian_li(driver):
    """
    city_list = []
    city_list_items = wait_retry_s(driver, '.dropdown-city-list li:not(:last-child)')

    # 遍历城市
    for city_item in city_list_items:
        city_list.append(city_item.text)
    print(city_list)
    """

    city_list = ['深圳', '广州', '杭州', '厦门', '全国']
    # 开始遍历
    for city in city_list:
        city_list_items = wait_retry_s(driver, '.dropdown-city-list li:not(:last-child)')
        # 将boss上的所有的城市打印一遍
        for city_item in city_list_items:
            print('@@@', city_item.text)
        for city_item in city_list_items:
            # 判断当前自定义城市与boss的城市是否一致，如果一致就进行求职
            if city == city_item.text:
                print(city)
                city_item.click()
                send(driver, city)
                break


def zi_ding_yi(driver):
    while True:
        # 从控制台读取用户输入
        city = input("请输入城市（输入“exit”退出）: ")

        if city.__eq__('exit'):
            return

        # 打印用户输入的内容
        print("你输入的城市是:", city)

        # 开始求职
        send(driver, city)


def get_job_info(body):
    print('职位信息函数...', body)

    # 文件夹名
    file_name = ''

    # 工商信息
    try:
        business_info = body.find_element(By.CSS_SELECTOR, '.level-list')
        # 获取所有的 li 元素
        li_elements = business_info.find_elements(By.TAG_NAME, 'li')
        # 获取公司名称
        company_name = li_elements[0].text.split('\n')[1]
        print(company_name)
        file_name = file_name + company_name
    except NoSuchElementException:
        logger.warning('没有”工商信息“元素')
        try:
            company_info = body.find_element(By.CSS_SELECTOR, '.sider-company')
            div_element = company_info.find_element(By.CSS_SELECTOR, '.company-info')
            # 获取所有 a 元素
            a_elements = div_element.find_elements(By.TAG_NAME, 'a')
            # 获取公司名称
            file_name = file_name + a_elements[1].text
        except NoSuchElementException:
            logger.warning('没有工商信息就算了，还没有公司信息')
            print(body)
            time.sleep(60)

    # 岗位
    try:
        post = body.find_element(By.CSS_SELECTOR, '.info-primary .name h1').get_attribute('innerHTML')
        print(post)
        # 替换非法字符
        post = ''.join(illegal_chars.get(char, char) for char in post)
        file_name = file_name + '-' + post
    except NoSuchElementException:
        logger.warning('没有”岗位“元素')

    # 获取当前日期并格式化
    current_date = datetime.now().strftime("%Y-%m-%d")

    # 创建文件夹
    file_dir = fr'static\boss\{current_date}\{file_name}'
    print('路径：', file_dir)

    # 创建文件夹
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
        logger.info(f"文件夹已创建: {file_dir}")
    else:
        logger.warning(f"文件夹已存在: {file_dir}")

    # 创建文本.txt
    with open(file_dir + fr'\{file_name}.txt', 'w', encoding='utf-8') as f:
        f.write('==========岗位==========\n')
        # 岗位
        try:
            post = body.find_element(By.CSS_SELECTOR, '.info-primary .name h1').get_attribute('innerHTML')
            print(post)
            f.write(post)
            f.write('\n')
        except NoSuchElementException:
            logger.warning('没有”岗位“元素')

        f.write('==========薪资==========\n')
        # 薪资
        try:
            salary = body.find_element(By.CSS_SELECTOR, '.info-primary .salary').get_attribute('innerHTML')
            print(salary)
            f.write(salary)
            f.write('\n')
        except NoSuchElementException:
            logger.warning('没有”薪资“元素')

        f.write('==========地点==========\n')
        # 地点
        try:
            location = body.find_element(By.CSS_SELECTOR, '.text-city').get_attribute('innerHTML')
            print(location)
            f.write(location)
            f.write('\n')
        except NoSuchElementException:
            logger.warning('没有”地点“元素')

        f.write('==========经验要求==========\n')
        # 经验要求
        try:
            experiece = body.find_element(By.CSS_SELECTOR, '.text-experiece').get_attribute('innerHTML')
            print(experiece)
            f.write(experiece)
            f.write('\n')
        except NoSuchElementException:
            logger.warning('没有”经验要求“元素')

        f.write('==========学历要求==========\n')
        # 学历要求
        try:
            degree = body.find_element(By.CSS_SELECTOR, '.text-degree').get_attribute('innerHTML')
            print(degree)
            f.write(degree)
            f.write('\n')
        except NoSuchElementException:
            logger.warning('没有”学历要求“元素')

        f.write('==========福利==========\n')
        # 福利
        try:
            welfare = body.find_element(By.CSS_SELECTOR, '.tag-container-new .job-tags')
            print(welfare.get_attribute('outerHTML'))
            # 获取所有的 span 元素
            span_elements = welfare.find_elements(By.TAG_NAME, 'span')
            # 遍历每个 span 元素并获取其文本内容
            for span in span_elements:
                print(span.get_attribute('textContent'))  # textContent 通常更能准确地获取到动态生成的内容，特别是在内容是通过 JavaScript 动态插入的情况下
                f.write(span.get_attribute('textContent'))
                f.write('\n')
        except NoSuchElementException:
            logger.warning('没有”福利“元素')

        f.write('==========技术栈要求==========\n')
        # 技术栈要求
        try:
            technology_stack = body.find_element(By.CSS_SELECTOR, '.job-keyword-list')
            print(technology_stack.get_attribute('outerHTML'))
            # 获取所有的 li 元素
            li_elements = technology_stack.find_elements(By.TAG_NAME, 'li')
            # 遍历每个 li 元素并获取其文本内容
            for li in li_elements:
                print(li.text)
                f.write(li.text)
                f.write('\n')
        except NoSuchElementException:
            logger.warning('没有”技术栈“元素')

        f.write('==========招聘时间要求==========\n')
        # 招聘时间要求
        try:
            recruitment_time = body.find_element(By.CSS_SELECTOR, '.school-job-sec')
            print(recruitment_time.get_attribute('outerHTML'))
            # 获取所有的 span 元素
            span_elements = recruitment_time.find_elements(By.TAG_NAME, 'span')
            # 遍历每个 span 元素并获取其文本内容
            for span in span_elements:
                print(span.text)
                f.write(span.text)
                f.write('\n')
        except NoSuchElementException:
            logger.warning('没有”招聘时间“元素')

        f.write('==========岗位职责==========\n')
        # 岗位职责
        try:
            post_statement = body.find_element(By.CSS_SELECTOR, '.job-sec-text')
            print(post_statement.text)
            f.write(post_statement.text)
            f.write('\n')
        except NoSuchElementException:
            logger.warning('没有”岗位职责“元素')

        f.write('==========公司介绍==========\n')
        # 公司介绍
        try:
            company_introduction = body.find_element(By.CSS_SELECTOR, '.fold-text')
            print(company_introduction.text)
            f.write(company_introduction.text)
            f.write('\n')
        except NoSuchElementException:
            logger.warning('没有”公司介绍“元素')

        f.write('==========工商信息==========\n')
        # 工商信息
        try:
            business_info = body.find_element(By.CSS_SELECTOR, '.level-list')
            # 获取所有的 li 元素
            li_elements = business_info.find_elements(By.TAG_NAME, 'li')
            # 遍历
            for li in li_elements:
                print(li.text)
                f.write(li.text.replace('\n', '：'))
                f.write('\n')
        except NoSuchElementException:
            logger.warning('没有”工商信息“元素')

        f.write('==========工作地址==========\n')
        # 工作地址
        try:
            job_address = body.find_element(By.CSS_SELECTOR, '.location-address')
            print(job_address.text)
            f.write(job_address.text)
            f.write('\n')
        except NoSuchElementException:
            logger.warning('没有”工作地址“元素')

        f.write('==========公司信息==========\n')
        # 公司信息
        try:
            company_info = body.find_element(By.CSS_SELECTOR, '.sider-company')
            # print(company_info.get_attribute('outerHTML'))
            # 获取 div 元素
            div_element = company_info.find_element(By.CSS_SELECTOR, '.company-info')
            # 获取所有 a 元素
            a_elements = div_element.find_elements(By.TAG_NAME, 'a')
            # 获取logo
            logo_img = a_elements[0].find_element(By.TAG_NAME, 'img')
            print(logo_img.get_attribute('src'))
            # 下载logo
            response = requests.get(logo_img.get_attribute('src'))
            if response.status_code == 200:
                # 保存图片
                with open(file_dir + fr'\{file_name}.jpg', 'wb') as fp:
                    fp.write(response.content)
                print(f"图片已保存")
            else:
                print(f"请求失败，状态码: {response.status_code}")
            # 获取公司名称
            print(a_elements[1].text)
            f.write(a_elements[1].text)
            f.write('\n')
            # 获取所有的 p 元素
            p_elements = company_info.find_elements(By.TAG_NAME, 'p')[1:]
            # 是否融资
            # 公司规模
            # 公司行业
            for p_element in p_elements:
                print(p_element.text)
                f.write(p_element.text)
                f.write('\n')
        except NoSuchElementException:
            logger.warning('没有”公司信息“元素')


def job_seeking(driver):
    time.sleep(5)

    # 获取整个<body>
    body = wait_retry_tag_name(driver, 'body')
    print(body)

    # 猎头顾问直接跳过
    filter_list = ['猎头顾问', '代招']
    for _ in filter_list:
        if check_text_presence(driver, _):
            logger.warning(f'{_}=>pass')
            return

    # 立即沟通
    try:
        chat_btn = body.find_element(By.CSS_SELECTOR, '.btn-startchat-wrap .btn-startchat')
        print(chat_btn.text)
        if chat_btn.text == '立即沟通':
            chat_btn.click()
            time.sleep(5)
            # 检测文本是否存在
            if check_text_presence(driver, '今日沟通人数已达上限，请明天再试'):
                logger.critical("沟通失败！==>今日沟通人数已达上限，请明天再试")
                # 创建EmailSender类的实例
                email_sender = EmailSender(
                    '2532127048@qq.com',
                    'rtnezlqbpzolecfe',
                    '2532127048@qq.com'
                )

                # 调用send_email方法发送邮件
                email_sender.send_email('boss直聘打招呼自动化系统', '今日沟通人数已达上限，请明天再试')
                sys.exit(1)  # 终止程序，返回状态码1表示异常退出
            else:
                logger.info(f'沟通成功！')
                get_job_info(body)  # 获取职位信息
        else:
            logger.warning(f'该岗位已沟通过！')
    except NoSuchElementException:
        logger.warning('没有“沟通”元素')


def send(driver, city):
    print('开始投递简历或者发送消息===>求职城市：', city)

    # 等待页面加载
    time.sleep(10)

    # 查找所有的 <li> 标签
    job_list_items = wait_retry_s(driver, '.job-list-box li.job-card-wrapper')

    # 遍历每个 <li> 标签并点击其中的链接
    for index, item in enumerate(job_list_items):
        # if index < len(job_list_items) - 1:
        #     continue
        try:
            # 将元素滚动到视窗内
            driver.execute_script("arguments[0].scrollIntoView(true);", item)

            # 直接在列表页判断是否是猎头，是即下滑一格，否则继续
            # 使用CSS选择器，查找li元素内alt属性为"猎头"的img元素
            img_elements = item.find_elements(By.CSS_SELECTOR, "img[alt='猎头']")
            if len(img_elements) > 0:
                # 使用JavaScript的window.open方法打开新标签页
                driver.execute_script("window.open('https://www.example.com');")
                # 切换到新标签页
                driver.switch_to.window(driver.window_handles[-1])
                logger.warning("列表页猎头")
                continue

            # 查找 <li> 标签内的链接
            link = item.find_element(By.CSS_SELECTOR, 'a.job-card-left')

            # 使用 JavaScript 点击
            driver.execute_script("arguments[0].click();", link)

            # 等待新页面加载完成（可选）
            # 这里假设新页面会在新的标签页中打开
            driver.switch_to.window(driver.window_handles[-1])

            # 在这里可以进行你需要的操作，比如抓取数据
            print('进入招聘页面...')
            job_seeking(driver)
            time.sleep(1)
        except Exception as e:
            print(f"点击链接时发生错误: {e}")
        finally:
            # 关闭新窗口并返回主窗口
            driver.close()
            time.sleep(1)
            driver.switch_to.window(driver.window_handles[0])

    # 等待页面加载
    time.sleep(5)

    # 执行JavaScript代码，将滚动条滚动到页面最底部
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    timeout = 60  # 60秒还没找到就跳出
    selector = '.options-pages a[href="javascript:;"]:last-child'
    while not try_fount_css_selector(driver, selector):
        print(f"未找到元素{selector}，等待1秒后重试...")
        driver.refresh()  # 刷新页面
        time.sleep(2)  # 等待2秒后重试
        timeout -= 2
        logger.info(timeout)
        if timeout <= 0:
            return
    time.sleep(5)
    is_has_boss_login_close(driver)
    next_page_button = driver.find_element(By.CSS_SELECTOR, selector)
    print(f"找到元素：{selector}->{next_page_button}")

    # 检查按钮是否有 disabled 类
    if 'disabled' in next_page_button.get_attribute('class'):
        print("下一页按钮是禁用状态")

        # 执行JavaScript代码，将滚动条返回到页面顶部
        driver.execute_script("window.scrollTo(0, 0);")

        return
    else:
        print("下一页按钮是启用状态")

        # 使用 JavaScript 点击
        driver.execute_script("arguments[0].click();", next_page_button)

        # 等待页面加载
        time.sleep(2)

        send(driver, city)


def do(driver):
    # 打开BOSS直聘
    driver.get('https://www.zhipin.com/web/user/?ka=header-login')  # 登录页
    # driver.get('https://www.zhipin.com/shenzhen/?seoRefer=index')  # 首页

    login(driver)

    # 查找所有带有特定属性的元素
    search_btn = wait_retry(driver, '[ka="header-job"]')
    print(search_btn.get_attribute('outerHTML'))
    search_btn.click()

    # 查找所有带有特定属性的输入框元素
    search_input = wait_retry(driver, '[placeholder="搜索职位、公司"]')
    print(search_input.get_attribute('outerHTML'))
    search_input.send_keys('Java')
    # search_input.send_keys('兼职 肯德基 便利店 奶茶店 理货 分拣 汉堡')

    # 查找所有带有特定属性的搜索按钮元素
    elements_search = wait_retry(driver, '[ka="job_search_btn_click"]')
    print(elements_search.get_attribute('outerHTML'))
    elements_search.click()

    # """
    # 使用XPath定位元素并筛选条件
    def condition_filter_select(filter_label, option_ka, option_text):
        # 使用XPath定位第一个“工作经验/公司规模”选择框
        condition_filter_select = wait_retry_xpath(driver,
                                                   f'//div[contains(@class, "condition-filter-select") and .//span['
                                                   f'text()="{filter_label}"]][1]')

        # 使用ActionChains模拟鼠标悬停在“工作经验/公司规模”上
        action = ActionChains(driver)
        action.move_to_element(condition_filter_select).perform()

        # 查找“应届生/0-20人”选项
        recent_graduate_option = wait_retry_xpath(driver, f'//li[@ka="{option_ka}"]')

        # 点击“应届生/0-20人”选项
        recent_graduate_option.click()

        # 打印成功信息
        print(f"{option_text}选项点击成功")

        time.sleep(10)

    # 选择“工作经验”中的“应届生”
    for scale_ka, scale_text in [
        ("sel-exp-102", "应届生"),
        ("sel-exp-101", " 经验不限"),
        ("sel-exp-103", " 1年以内")
    ]:
        condition_filter_select("工作经验", scale_ka, scale_text)

    # 选择“公司规模”中的多个选项
    for scale_ka, scale_text in [
        ("sel-scale-301", "0-20人"),
        ("sel-scale-302", "20-99人"),
        ("sel-scale-303", "100-499人"),
        ("sel-scale-304", "500-999人"),
        ("sel-scale-305", "1000-9999人")
    ]:
        condition_filter_select("公司规模", scale_ka, scale_text)

    # 选择“学历要求”中的“本科”
    for scale_ka, scale_text in [
        ("sel-degree-202", "大专"),
        ("sel-degree-203", "本科")
    ]:
        condition_filter_select("学历要求", scale_ka, scale_text)
    # """

    bian_li(driver)


if __name__ == '__main__':
    # 配置参数
    # browser = 'edge'
    browser = 'chrome'
    headless = False
    # headless = True
    proxy = 'http://18.223.25.15:80'
    user_agent = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/58.0.3029.110 Safari/537.3')

    # 打开浏览器实例
    driver = open_browser(browser=browser, headless=headless, proxy=None, user_agent=user_agent)
    # driver = open_exist_browser()

    try:
        do(driver)
        # 创建EmailSender类的实例
        email_sender = EmailSender(
            '2532127048@qq.com',
            'rtnezlqbpzolecfe',
            '2532127048@qq.com'
        )

        # 调用send_email方法发送邮件
        email_sender.send_email('boss直聘打招呼自动化系统', '打招呼完毕！（可能出现异常Exception）')
    except Exception:
        # 清空控制台
        os.system('cls')
        # 打印详细的堆栈跟踪信息
        traceback.print_exc()
        do(driver)
    finally:
        driver.quit()
