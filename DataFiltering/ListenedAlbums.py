#load necessary libraries
import os
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup


def login():

    # 获取登录页面
    response = session.get(login_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 提取必要的表单数据，假设CSRF token字段名称是 'csrfmiddlewaretoken'
    csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']

    #TODO：username_or_email/password填入自己的
    # 构造登录请求的数据
    login_data = {
        'csrfmiddlewaretoken': csrf_token,
        'next': '/login?next=/user/jolesreal/library/albums',
        'username_or_email': 'Saber232',
        'password': '1661076516@gmail.com',
        'submit': '登录'
    }

    # 发送登录请求
    login_response = session.post(login_url, data=login_data, headers=headers)
    return login_response


def getOnePage(page_num, name, personal_data):
    print("page_num:{}".format(page_num))
    page_url = f'https://www.last.fm/user/{name}/library/albums?page={page_num}'
    page_response = session.get(page_url, headers=headers)
    page_soup = BeautifulSoup(page_response.text, 'html.parser')
    target_html = page_soup.find('tbody', {'data-playlisting-add-entries': True})

    if target_html:
        chartlist_rows = target_html.find_all('tr', class_='chartlist-row')

        for row in chartlist_rows:
            chartlist_index = row.find('td', class_='chartlist-index').get_text(strip=True)
            album_name = row.find('td', class_='chartlist-name').find('a').get_text(strip=True)
            if album_name not in song_names.values:
                continue
            artist_name = row.find('td', class_='chartlist-artist').find('a').get_text(strip=True)
            play_count = row.find('span', class_='chartlist-count-bar-value').get_text(strip=True).split("s")[
                0].replace(",", "")

            personal_data.append({
                "user": name,
                "rank": chartlist_index,
                "album_name": album_name,
                "artist": artist_name,
                "play_count": play_count,
            })
        return page_num + 1

    else:
        print("Page {} Once again".format(page_num))
        time.sleep(20)
        return page_num


def getOnePerson(name):
    personal_data = []
    page_url = f'https://www.last.fm/user/{name}/library/albums'

    while True:
        page_response = session.get(page_url, headers=headers)
        if page_response.status_code != 200:
            print("Error: Unable to fetch page for {}. Status code: {}".format(name, page_response.status_code))
            time.sleep(5)  # 等待5秒后重试
            continue

        soup = BeautifulSoup(page_response.text, 'html.parser')
        metadata_element = soup.find('p', {'class': 'metadata-display', 'data-top-item-count': ''})

        if metadata_element:
            element = metadata_element.get_text(strip=True).replace(",", "")
            if int(element) % 50 == 0:
                num = int(int(element) / 50)
            else:
                num = int(int(element) / 50) + 1
            print("num:{}".format(num))
            page_num = 1
            while page_num <= num:
                page_num = getOnePage(page_num, name, personal_data)
            print("{} Success, total {}".format(name, len(personal_data)))
            all_data.extend(personal_data)
            return  # 成功后退出循环
        else:
            print("Metadata not found for {}. Retrying...".format(name))
            time.sleep(5)  # 等待5秒后重试


# 创建一个会话对象
session = requests.Session()
# TODO：变成专辑的CSV
df = pd.read_csv('grouped_data.csv')
song_names = df['name']

login_url = 'https://www.last.fm/login'

headers = {
    'Referer': login_url,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
login_response = login()
# 检查是否登录成功
if 'incorrect' not in login_response.text:
    for i in range(50, 40, -1):
        # TODO:换成你的对应的用户的CSV
        df = pd.read_csv(f'users/subframe_{i}.csv')
        names = df["user"].values
        names = set(names)

        all_data = []

        for name in names:
            getOnePerson(name)

        # 创建结果文件夹（如果不存在）
        result_dir = 'result'
        if not os.path.exists(result_dir):
            os.makedirs(result_dir)

        # 保存结果到CSV文件
        result_df = pd.DataFrame(all_data)
        result_df.to_csv(f'{result_dir}/subframe_{i}.csv', index=False)
        print("Finished")
else:
    print('登录失败，请检查用户名和密码')