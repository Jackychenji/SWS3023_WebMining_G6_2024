import os

import pandas as pd
import requests
from bs4 import BeautifulSoup


def getOnePerson(name, invalid_names):
    page_url = f'https://www.last.fm/user/{name}/library/albums'
    page_response = session.get(page_url, headers=headers)
    if page_response.status_code == 200:
        soup = BeautifulSoup(page_response.text, 'html.parser')
        if soup.find('p', {'class': 'metadata-display', 'data-top-item-count': ''}):
            element = soup.find('p', {'class': 'metadata-display', 'data-top-item-count': ''}).get_text(
                strip=True).replace(",", "")
            if element == "" or int(element) < 200:
                print("invalid {}".format(name))

            else:
                print(name)
                valid_names.add(name)
        else:
            print("invalid {}".format(name))

    else:
        print("invalid {}".format(name))


if __name__ == '__main__':
    # 创建一个会话对象
    session = requests.Session()
    login_url = 'https://www.last.fm/login'
    headers = {
        'Referer': login_url,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # 读取用户数据
    df = pd.read_csv('filtered_user_list_djl.csv')
    names = df["user"].values
    names = set(names)
    valid_names = set()

    # 创建一个目录用于存放结果文件
    result_dir = 'filter'
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    count = 0
    batch_number = 1

    # 获取无效用户
    for name in names:
        getOnePerson(name, valid_names)
        count += 1

        if count == 100:
            # 从当前数据帧中过滤无效用户并保存
            valid_users_df = pd.DataFrame(list(valid_names), columns=['user'])
            valid_users_df.to_csv(f'{result_dir}/filtered_users_batch_{batch_number}.csv', index=False)

            print(f"Filtered users saved to 'filtered_users_batch_{batch_number}.csv'")

            # 重置计数器和无效用户集合
            count = 0
            batch_number += 1
            valid_names.clear()

    # 处理剩余的用户
    if count > 0:
        valid_users_df = pd.DataFrame(list(valid_names), columns=['user'])
        valid_users_df.to_csv(f'{result_dir}/filtered_users_batch_{batch_number}.csv', index=False)
        print(f"Filtered users saved to 'filtered_users_batch_{batch_number}.csv'")
