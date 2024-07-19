# import chromedriver_binary
import ast
from collections import Counter

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


# 预测用户对未听过专辑的评分
def predict_ratings(user_album_matrix, album_similarity_df):
    mean_user_rating = user_album_matrix.mean(axis=1).values.reshape(-1, 1)
    ratings_diff = (user_album_matrix - mean_user_rating)
    pred = mean_user_rating + album_similarity_df.dot(ratings_diff.T).T / np.abs(album_similarity_df).sum(axis=1)
    return pred


def recommend_albums_item_based(user, user_album_matrix_02, predicted_ratings_item_based_df, n_recommendations=10):
    user_ratings = user_album_matrix_02.loc[user]
    user_predictions = predicted_ratings_item_based_df.loc[user]
    already_rated = user_ratings[user_ratings > 0].index
    recommendations = user_predictions.drop(already_rated).sort_values(ascending=False).head(n_recommendations)
    return recommendations


def recommend_albums(df):
    data = pd.read_csv("songs.csv")

    # 确保 release_date 列是日期时间类型
    data['release_date'] = pd.to_datetime(data['release_date'], errors='coerce')

    # 获取当前时间
    now = pd.Timestamp.now()

    # 删除 release_date 晚于现在的行
    data = data[data['release_date'] <= now]

    # 清洗 data 的数据，全改为小写
    data.loc[:, 'name'] = data['name'].str.strip().str.lower()
    data.loc[:, 'artist'] = data['artist'].str.strip().str.lower()

    df['album'] = df['album'].str.lower()
    matching_albums = df[df['album'].isin(data['name'])]
    print(len(matching_albums))

    target_tags = [
        '80s', 'acoustic', 'alternative', 'blues', 'british',
        'classical', 'country', 'dance', 'electronic', 'hardcore',
        'hip-hop', 'indie', 'jazz', 'metal', 'punk', 'reggae', 'rap', 'mb', 'rock'
    ]

    if len(matching_albums) >= 20:
        user1 = pd.read_csv("result_djl.csv")

        # 清洗 user1 的数据，全改为小写
        user1.loc[:, 'album_name'] = user1['album_name'].str.strip().str.lower()
        user1.loc[:, 'artist'] = user1['artist'].str.strip().str.lower()

        # 合并 user1 和 data，以删除匹配不上的行
        merged_user1 = user1.merge(data[['name', 'artist']], left_on=['album_name', 'artist'],
                                   right_on=['name', 'artist'],
                                   how='inner')

        # 打印删除不匹配行前后的数据行数
        print(f"Before cleaning: {len(user1)} rows")
        print(f"After cleaning: {len(merged_user1)} rows")

        # 更新 user1 为匹配上的数据
        user11 = merged_user1.drop(columns=['name'])

        # 移除rank列中的逗号
        user11["rank"] = user11["rank"].str.replace(',', '')

        user11["rank"] = user11["rank"].astype("int64")

        matching_albums['user'] = None
        matching_albums['rank'] = None

        # 创建新的记录
        new_records = pd.DataFrame()
        new_records['user'] = pd.DataFrame(['new_user'] * len(matching_albums))  # 设置用户名称
        new_records['rank'] = pd.DataFrame([1] * len(matching_albums))  # 设置 rank
        new_records['album_name'] = matching_albums['album'].values  # 映射专辑名
        new_records['artist'] = matching_albums['artist'].values  # 映射艺术家
        new_records['play_count'] = matching_albums['score'].values  # 映射听众数作为播放次数

        print(new_records)

        # 使用 pd.concat 将新记录添加到 user11
        user11 = pd.concat(
            [user11[['user', 'rank', 'album_name', 'artist', 'play_count']],
             new_records],
            ignore_index=True)

        print(user11)

        # 在 user11 中新增一列 'url'
        user11['url'] = None  # 初始化

        # 遍历 user11，根据 album_name 和 artist 到 data 中查找匹配的 url 值
        for index, row in user11.iterrows():
            album_name = row['album_name']
            artist = row['artist']
            match = data[(data['name'] == album_name) & (data['artist'] == artist)]
            if not match.empty:
                user11.at[index, 'url'] = match.iloc[0]['url']

        # 计算每个用户对所有专辑中最多的一个收听次数
        max_play_counts = user11.groupby('user')['play_count'].max().reset_index()
        max_play_counts.columns = ['user', 'max_play_count']

        # 合并 max_play_counts 和 user1，以获取每个用户的最大收听次数
        user11 = user11.merge(max_play_counts, on='user', how='left')

        # 新增一列 'normalized_play_count'，为用户听该专辑的次数除以用户对所有专辑中最多的一个收听次数
        user11['npc'] = user11['play_count'] / user11['max_play_count'] * 10

        print("User1 with normalized play counts:")

        # 合并 user1 和 data 数据，以获取每个专辑的 url
        user11 = user11.merge(data[['name', 'artist', 'url']], left_on=['album_name', 'artist'],
                              right_on=['name', 'artist'], how='left')

        # 创建一个新的列 'album_artist'，表示专辑名和艺术家的组合
        user11['album_artist'] = user11['album_name'] + ' by ' + user11['artist']

        # 创建用户-专辑交互矩阵，以 album_artist 作为唯一标识符
        user_album_matrix_01 = user11.pivot_table(index='user', columns='album_artist', values='play_count',
                                                  fill_value=0)

        # 打印用户-专辑交互矩阵，内部为收听次数
        print("User-Album Matrix:")

        # 合并 user1 和 data 数据，以获取每个专辑的 url
        user11 = user11.merge(data[['name', 'artist', 'url']], left_on=['album_name', 'artist'],
                              right_on=['name', 'artist'], how='left')

        # 创建一个新的列 'album_artist'，表示专辑名和艺术家的组合
        user11['album_artist'] = user11['album_name'] + ' by ' + user11['artist']

        # 创建用户-专辑交互矩阵，以 album_artist 作为唯一标识符
        user_album_matrix_02 = user11.pivot_table(index='user', columns='album_artist', values='npc', fill_value=0)

        # 打印用户-专辑交互矩阵，内部为计算的加权值
        print("User-Album Matrix:")

        # 计算专辑之间的相似度矩阵
        album_similarity = cosine_similarity(user_album_matrix_02.T)

        # 创建专辑相似度的 DataFrame
        album_similarity_df = pd.DataFrame(album_similarity, index=user_album_matrix_02.columns,
                                           columns=user_album_matrix_02.columns)
        predicted_ratings_item_based = predict_ratings(user_album_matrix_02, album_similarity_df)
        predicted_ratings_item_based_df = pd.DataFrame(predicted_ratings_item_based, index=user_album_matrix_02.index,
                                                       columns=user_album_matrix_02.columns)
        # 示例：为某个用户生成推荐列表
        user = 'new_user'
        recommendations_item_based = recommend_albums_item_based(user, user_album_matrix_02,
                                                                 predicted_ratings_item_based_df)
        return 0, recommendations_item_based
    else:
        # 初始化一个 Counter 对象来统计标签出现次数
        tag_counter = Counter()

        # 遍历 tag 列
        for tags in df['tag']:
            # 如果标签不为空
            if tags != '[]':
                # 将字符串转换为列表
                tag_list = ast.literal_eval(str(tags))

                # 找到第一个目标标签并计数
                for tag in tag_list:
                    if tag in target_tags:
                        tag_counter[tag] += 1

        # 将计数器转换为 DataFrame
        tag_counts = pd.DataFrame(tag_counter.items(), columns=['tag', 'count'])

        return -1, tag_counts
