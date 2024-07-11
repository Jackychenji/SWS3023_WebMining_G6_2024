from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import ui
from webdriver_manager.chrome import ChromeDriverManager

# 初始化 Chrome 浏览器
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# 打开网页
driver.get("http://music.163.com/#/user/songs/rank?id=39686047")

# 切换到 iframe
driver.switch_to.frame("g_iframe")

data=''#用来保存数据

try:
    wait = ui.WebDriverWait(driver, 15)

    # 找到歌曲列表所在的父标签

    if wait.until(lambda driver: driver.find_element_by_class_name('g-bd')):

        print('success!')

        data += driver.find_element_by_id('rHeader').find_element_by_tag_name('h4').text + '\n'

        print(data)  # 抓取用户听了多少首歌

        lists = driver.find_element_by_class_name('m-record').find_elements_by_tag_name('li')

        print(len(lists))  # 网易只给出了前100首听的最频繁的歌

        for l in lists:
            temp = '歌曲名：' + l.find_element_by_tag_name('b').text + ' 歌手：' + l.find_element_by_class_name(
                's-fc8').text.replace('-', '') + ' 频率：' + l.find_element_by_class_name('bg').get_attribute('style')

            print(temp)  # 解析出歌名 歌手 频率

            data += temp + '\n'
finally:
    driver.quit()

