from selenium import webdriver
import time

url = 'https://www.csdn.net/'
browser = webdriver.Edge()
browser.get(url)
# 1500*4680
for c in range(100):
    js = 'window.scrollBy(0,100)'
    browser.execute_script(js)
    time.sleep(0.5)  # 每次滑动时间间隔0.5秒
    browser.save_screenshot('page' + str(c+1) + '.png')

print(browser.page_source)

browser.quit()
