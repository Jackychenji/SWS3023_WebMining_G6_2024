# load necessary libraries
import time
import urllib.parse

import cloudmusic
import pandas as pd
import requests
from bs4 import BeautifulSoup

from item_based_recommendation import recommend_albums


class f_Music:
    def __init__(self, id, album, artist, score):
        self.id = id
        self.album = album
        self.artist = artist
        self.score = score


class f_album:
    def __init__(self, album, artist, tag):
        self.album = album
        self.artist = artist
        self.tag = tag


def login(session, login_url, headers):
    # 获取登录页面
    response = session.get(login_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 提取必要的表单数据，假设CSRF token字段名称是 'csrfmiddlewaretoken'
    csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']

    # TODO：username_or_email/password填入自己的
    # 构造登录请求的数据
    login_data = {
        'csrfmiddlewaretoken': csrf_token,
        'next': '/login?next=/user/jolesreal/library/albums',
        'username_or_email': 'jJj1456',
        'password': '123456@j',
        'submit': '登录'
    }

    # 发送登录请求
    login_response = session.post(login_url, data=login_data, headers=headers)
    return login_response


def getOneAlbum(album_url, artist, album, headers, session):
    album_data = []

    while True:
        page_response = session.get(album_url, headers=headers)
        if page_response.status_code != 200:
            print("Error: Unable to fetch page for {}. Status code: {}".format(album, page_response.status_code))
            time.sleep(5)  # 等待5秒后重试
            continue

        soup = BeautifulSoup(page_response.text, 'html.parser')
        # 查找所有 class 为 'tag' 的 <p> 标签
        metadata_elements = soup.find_all('a', class_='link-block-target')

        tag = []
        if metadata_elements:
            for metadata_element in metadata_elements:
                element_text = metadata_element.get_text(strip=True)
                tag.append(element_text)
        Album_wanted = f_album(album=album, artist=artist, tag=tag)
        return Album_wanted
        '''else:
            print("Metadata not found for {}. Retrying...".format(album))
            time.sleep(5)  # 等待5秒后重试'''


def getOneSearch(album, artists, headers, session):
    album_search = str(album).replace(" ", "+")
    album_data = []
    page_url = f'https://www.last.fm/search?q={album_search}'

    while True:
        page_response = session.get(page_url, headers=headers)
        if page_response.status_code != 200:
            print("Error: Unable to fetch page for {}. Status code: {}".format(album, page_response.status_code))
            time.sleep(5)  # 等待5秒后重试
            continue

        soup = BeautifulSoup(page_response.text, 'html.parser')
        # 查找所有 class 为 'tag' 的 <p> 标签
        zhuanji_elements = soup.find_all('p', class_='grid-items-item-main-text')
        if zhuanji_elements:
            for zhuanji_element in zhuanji_elements:
                zhuanji_name = zhuanji_element.get_text(strip=True)
                if album.lower() == zhuanji_name.lower():
                    a_tag = zhuanji_element.find('a', class_='link-block-target')
                    # zhuanji_url = a_tag['herf']
                    if a_tag and 'href' in a_tag.attrs:
                        url = a_tag['href']
                        un_url = urllib.parse.unquote(url)
                        low_un_url = un_url.lower()
                        if low_un_url.find(album_search.lower()) != -1:
                            yesorno = 1
                            start = low_un_url.find(album_search)
                            low_un_url = low_un_url[:start]
                        else:
                            break
                        for artist in artists:
                            un_artist = str(artist).replace(" ", "+")
                            low_un_artist = un_artist.lower()
                            if low_un_url.find(low_un_artist) == -1:
                                yesorno = 0
                                break
                        if yesorno == 1 and un_url != '':
                            wanted = 'https://www.last.fm' + url + '/+tags'
                            return wanted
                    else:
                        print("未找到链接")

            return
        else:
            print("Metadata not found for {}. Retrying...".format(album))
            return


def recommend(user_id):
    list_open = 0
    try:
        user = cloudmusic.getUser(user_id)
        love_albums = []
    except Exception:
        # id不存在
        return -1, None

    try:
        lists = user.getPlaylist()
        love_list_ID = lists[0]['id']
    except Exception:
        # 歌单未开放
        list_open = 1
        print("error1")

    if love_list_ID:
        while True:
            try:
                songs = cloudmusic.getPlaylist(lists[0]['id'])
                for song in songs:
                    album_artist = f_Music(id=song.albumId, album=song.album, artist=song.artist, score=60)
                    love_albums.append(album_artist)
                break
            except Exception:
                print("error2")

    try:
        f_lists = user.getRecord(11)
        for f_list in f_lists:
            score = f_list['score']
            f_song = f_list['music']
            f_album_artist = f_Music(id=f_song.albumId, album=f_song.album, artist=f_song.artist, score=score)
            for love_album in love_albums:
                have = 0
                if love_album.id == f_song.albumId:
                    have = 1
                    love_album.score = 100
                    break
            if have == 0:
                love_albums.append(f_album_artist)
    except Exception:
        # 听歌记录未开放
        list_open = list_open + 2
        print("error3")

    if list_open == 3:
        return 0, None
    else:
        session = requests.Session()
        login_url = 'https://www.last.fm/login'

        headers = {
            'Referer': login_url,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        login_response = login(session, login_url, headers)

        if 'incorrect' not in login_response.text:
            shuju = []
            for love_album in love_albums:
                wante = getOneSearch(love_album.album, love_album.artist, headers, session)
                if wante != None:
                    print(wante)
                    music_album = getOneAlbum(wante, love_album.artist, love_album.album, headers, session)
                    shuju.append({
                        "album": music_album.album,
                        "artist": music_album.artist,
                        "tag": music_album.tag,
                        "score": love_album.score
                    })

            df = pd.DataFrame(shuju)

            code, result = recommend_albums(df)
            if code == -1:
                return -2, result
            result_df = pd.DataFrame(result, columns=['album', 'score'])
            return 1, result_df

        else:
            print('登录失败，请检查用户名和密码')


def info(user_id):
    try:
        user = cloudmusic.getUser(user_id)
        user_info = []
        return user.nickname
    except Exception:
        # id不存在
        return -1
