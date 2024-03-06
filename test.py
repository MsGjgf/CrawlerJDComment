# 导入selenium
from selenium import webdriver

# 创建浏览器操作对象
path = 'driver/chromedriver.exe'
browser = webdriver.Chrome(path)

browser.get('https://www.jd.com')

browser.quit()
