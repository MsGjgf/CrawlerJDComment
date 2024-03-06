import time

from selenium import webdriver
from selenium.webdriver.common.by import By

path = 'driver/chromedriver.exe'
browser = webdriver.Chrome(path)

url = 'https://item.jd.com/100071377749.html'
# 访问京东网站
browser.get(url)

# 如果需要登录
if browser.current_url == ('https://passport.jd.com/new/login.aspx?ReturnUrl=https%3A%2F%2Fitem.jd.com%2F100071377749'
                           '.html&czLogin=1'):
    text_name = browser.find_element(By.ID, 'loginname')
    text_name.send_keys('18377767441')
    text_pwd = browser.find_element(By.ID, 'nloginpwd')
    text_pwd.send_keys('5422xyc')
    text_login = browser.find_element(By.ID, 'loginsubmit')
    text_login.click()
time.sleep(60)
contents = browser.find_elements(By.CLASS_NAME, 'comment-item')
print(contents)
browser.quit()
