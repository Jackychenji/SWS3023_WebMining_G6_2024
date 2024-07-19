import pandas as pd
import numpy as np

albums_singleTag_df = pd.read_csv("songs.csv", encoding='UTF-8')
albums_singleTag_df['name'] = albums_singleTag_df['name'].astype(str).str.lower()
albums_singleTag_df['artist'] = albums_singleTag_df['artist'].astype(str).str.lower()


def recommending(sorted_grouped_df):
    # recommend 10 albums based on the percentage of his preferred tags
    # 计算每一类的百分比
    total_play_count = sorted_grouped_df['count'].sum()
    sorted_grouped_df['percentage'] = sorted_grouped_df['count'] / total_play_count * 100
    # 计算每一类对应的数值（假设总单位是10），保留到整数位
    sorted_grouped_df['corresponding_value'] = np.floor(sorted_grouped_df['percentage'] / 10).astype(int)
    # 调整总数以确保总数为10
    diff = 10 - sorted_grouped_df['corresponding_value'].sum()
    if diff > 0:
        # 增加差值到最大的项
        sorted_grouped_df.loc[sorted_grouped_df['corresponding_value'].idxmax(), 'corresponding_value'] += diff
    elif diff < 0:
        # 减少差值从最大的项
        sorted_grouped_df.loc[sorted_grouped_df['corresponding_value'].idxmax(), 'corresponding_value'] += diff

    sorted_grouped_df = sorted_grouped_df[sorted_grouped_df['corresponding_value'] != 0]

    # 初始化结果列表
    result = []
    # 迭代 tag 表中的每个标签
    for index, row in sorted_grouped_df.iterrows():
        tag = row['tag']
        n = row['corresponding_value']
        # 在 album 表中检索相应标签的播放量最高的专辑
        top_albums = albums_singleTag_df[albums_singleTag_df['tag'] == tag].nlargest(n, 'listeners')
        # 将结果添加到结果列表中
        result.append(top_albums)
    # 合并结果到一个 DataFrame 中
    final_result = pd.concat(result, ignore_index=True)
    return final_result

