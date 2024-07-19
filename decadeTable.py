import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# 读入文件
tags_df = pd.read_csv("song_all_tag.csv", index_col=False, header=0)
album_df = pd.read_csv('songs.csv')

# 定义标签
electronic_tag = ['house', 'techno', 'trance', 'dubstep', 'drum and bass', 'ambient', 'electro', 'synthwave', 'edm',
                  'future bass']
rock_tag = ['alternative rock', 'indie rock', 'punk rock', 'classic rock', 'hard rock', 'pop rock', 'blues rock',
            'soft rock', 'folk rock', 'progressive rock', 'country rock', 'garage rock', 'psychedelic rock',
            'southern rock', 'rockabilly', 'post-rock', 'art rock']
hip_hop_tag = ['boom bap', 'trap', 'gangsta rap', 'alternative hip-hop', 'east coast hip-hop', 'west coast hip-hop',
               'southern hip-hop', 'conscious hip-hop', 'jazz rap', 'cloud rap', 'drill', 'crunk', 'lo-fi hip-hop']
indie_tag = ['indie rock', 'indie pop', 'indie folk', 'indietronica', 'indie hip-hop', 'indie dance',
             'indie electronic', 'lo-fi indie', 'dream pop', 'shoegaze']
jazz_tag = ['swing', 'bebop', 'hard bop', 'cool jazz', 'modal jazz', 'free jazz', 'fusion', 'smooth jazz', 'latin jazz',
            'acid jazz', 'vocal jazz', 'gypsy jazz', 'contemporary jazz', 'avant-garde jazz']
reggae_tag = ['roots reggae', 'dub', 'dancehall', 'ska', 'rocksteady', 'lovers rock', 'ragga', 'reggae fusion']
british_tag = ['britpop', 'british rock', 'british folk', 'british blues', 'british punk', 'british soul']
punk_tag = ['hardcore punk', 'pop punk', 'post-punk', 'garage punk', 'ska punk', 'punk rock', 'anarcho-punk']
eighties_tag = ['80s pop', '80s rock', '80s metal']
dance_tag = ['house', 'techno', 'trance', 'electro', 'dubstep', 'drum and bass', 'edm', 'disco']
acoustic_tag = ['acoustic rock', 'acoustic folk', 'acoustic pop', 'unplugged']
rnb_tag = ['contemporary rnb', 'neo soul', 'quiet storm', 'funk', 'motown', 'soul']
hardcore_tag = ['hardcore punk', 'metalcore', 'post-hardcore', 'deathcore', 'hardcore techno']
country_tag = ['classic country', 'country pop', 'outlaw country', 'bluegrass', 'alt-country', 'honky tonk',
               'country rock']
blues_tag = ['delta blues', 'chicago blues', 'electric blues', 'country blues', 'blues rock', 'soul blues']
alternative_tag = ['alternative rock', 'alternative metal', 'alternative pop', 'alternative hip-hop',
                   'alternative dance', 'alt-country']
classical_tag = ['baroque', 'romantic', 'modern classical', 'renaissance', 'contemporary classical', 'early music',
                 'opera']
rap_tag = ['gangsta rap', 'trap', 'boom bap', 'conscious rap', 'alternative rap', 'crunk', 'drill', 'mumble rap']
metal_tag = ['heavy metal', 'death metal', 'black metal', 'thrash metal', 'power metal', 'doom metal',
             'symphonic metal', 'folk metal']
genres = ['electronic', 'rock', 'hip-hop', 'indie', 'jazz', 'reggae', 'british', 'punk', '80s', 'dance', 'acoustic',
          'rnb', 'hardcore', 'country', 'blues', 'alternative', 'classical', 'rap', 'metal']
decades = ['10s', '20s', '30s', '40s', '50s', '60s', '70s', '80s', '90s', '00s', '2000s', '2010s', '2020s']


def question2(prefer_genre):
    genre_mapping = {
        0: ("electronic", electronic_tag), 1: ("rock", rock_tag), 2: ("hip-hop", hip_hop_tag),
        3: ("indie", indie_tag), 4: ("jazz", jazz_tag), 5: ("reggae", reggae_tag),
        6: ("british", british_tag), 7: ("punk", punk_tag), 8: ("80s", eighties_tag),
        9: ("dance", dance_tag), 10: ("acoustic", acoustic_tag), 11: ("rnb", rnb_tag),
        12: ("hardcore", hardcore_tag), 13: ("country", country_tag), 14: ("blues", blues_tag),
        15: ("alternative", alternative_tag), 16: ("classical", classical_tag), 17: ("rap", rap_tag),
        18: ("metal", metal_tag)
    }

    # 初始化空集合
    sub_genre_str1 = set()
    sub_genre_str2 = set()

    # 遍历prefer_genre并根据条件更新sub_genre_str1, sub_genre_str2
    for i in range(len(prefer_genre)):
        if prefer_genre[i] == 1:
            genre, tags = genre_mapping[i]
            sub_genre_str1.add(genre)
            sub_genre_str2.update(tags)  # 使用集合更新方法添加标签

    # 将集合转换为列表
    sub_genre_str1 = list(sub_genre_str1)
    sub_genre_str2 = list(sub_genre_str2)

    return sub_genre_str1, sub_genre_str2


def recmd(preference, matrix_df):
    preference_df = pd.DataFrame([preference], columns=matrix_df.columns)
    similarity_scores = cosine_similarity(preference_df, matrix_df)[0]
    similarity_series = pd.Series(similarity_scores, index=matrix_df.index)
    top_n = 20
    similar_albums = similarity_series.sort_values(ascending=False).head(top_n)

    result_df = album_df[album_df['name'].isin(similar_albums.index)][['name', 'url']]
    result_df['similarity'] = result_df['name'].map(similar_albums)
    result_df = result_df.sort_values(by='similarity', ascending=False)

    return result_df


def get_decade_label(year):
    if year >= 2020:
        return '2020s'
    elif year >= 2010:
        return '2010s'
    elif year >= 2000:
        return '2000s'
    elif year >= 1990:
        return '90s'
    elif year >= 1980:
        return '80s'
    elif year >= 1970:
        return '70s'
    elif year >= 1960:
        return '60s'
    elif year >= 1950:
        return '50s'
    elif year >= 1940:
        return '40s'
    elif year >= 1930:
        return '30s'
    elif year >= 1920:
        return '20s'
    elif year >= 1910:
        return '10s'
    else:
        return None


def create_binary_list(prefer_genre):
    prefer_genre = [genre.lower() for genre in prefer_genre]
    binary_list = [0] * 19  # Initialize a list of 19 zeros

    # Define the genres list
    genres = ['electronic', 'rock', 'hip-hop', 'indie', 'jazz', 'reggae', 'british', 'punk', '80s', 'dance',
              'acoustic', 'rnb', 'hardcore', 'country', 'blues', 'alternative', 'classical', 'rap', 'metal']

    # Check each genre tag against the `prefer_genre` list and set the corresponding index to 1 if present
    for index, genre in enumerate(genres):
        if genre in prefer_genre:
            binary_list[index] = 1

    return binary_list


def create_binary_list_stag(stags, prefer_stag):
    prefer_stag = [genre.lower() for genre in prefer_stag]
    binary_list = [0] * len(stags)

    # Check each genre tag against the `prefer_genre` list and set the corresponding index to 1 if present
    for index, stag in enumerate(stags):
        if stag in prefer_stag:
            binary_list[index] = 1

    return binary_list


def create_binary_list_decade(prefer_decade):
    prefer_decade = [decade.lower() for decade in prefer_decade]
    binary_list = [0] * len(decades)  # Initialize a list of 19 zeros

    # Check each genre tag against the `prefer_genre` list and set the corresponding index to 1 if present
    for index, decade in enumerate(decades):
        if decade in prefer_decade:
            binary_list[index] = 1

    return binary_list


def data_process(bigTag_prefer, subTag_prefer, decade_prefer):
    user_album_df = pd.DataFrame(columns=album_df.columns)  # 后续建矩阵处理数据用
    prefer_genre = create_binary_list(bigTag_prefer)
    sub_genre_str1, sub_genre_str2 = question2(prefer_genre)

    for sub_g in sub_genre_str1:
        filtered_album_df = album_df[album_df['tag'] == sub_g]
        user_album_df = pd.concat([user_album_df, filtered_album_df], ignore_index=True)

    album_sub_tag_df = pd.merge(user_album_df, tags_df, on='url', how='left')
    album_sub_tag_df = album_sub_tag_df[['name_x', 'url', 'artist', 'listeners', 'release_date', 'tracks', 'tag_y']]
    album_sub_tag_df = album_sub_tag_df.rename(columns={'name_x': 'name', 'tag_y': 'sub_tag'})

    sub_tag_df = pd.DataFrame(0, index=album_sub_tag_df['name'].unique(), columns=sub_genre_str2)
    # 填充零一矩阵
    for index, row in album_sub_tag_df.iterrows():
        album_name = row['name']
        for tag in sub_genre_str2:
            if tag in row['sub_tag'].split(','):
                sub_tag_df.at[album_name, tag] = 1

    mask = (sub_tag_df != 0).any(axis=1)
    sub_tag_df = sub_tag_df[mask]

    subTag_prefer = create_binary_list_stag(sub_genre_str2, subTag_prefer)

    # 将sub_genre_str2作为subTag_prefer的表头
    subTag_prefer_df = pd.DataFrame([subTag_prefer[:len(sub_genre_str2)]], columns=sub_genre_str2)
    album_sub_tag_df['release_date'] = pd.to_datetime(album_sub_tag_df['release_date'], errors='coerce')
    album_sub_tag_df['release_year'] = album_sub_tag_df['release_date'].dt.year
    album_sub_tag_df['decade_label'] = album_sub_tag_df['release_year'].apply(get_decade_label)
    for decade in decades:
        filtered_album_df = album_sub_tag_df[album_sub_tag_df['decade_label'] == decade]
        album_sub_tag_df = pd.concat([album_sub_tag_df, filtered_album_df], ignore_index=True)
        album_sub_tag_df = album_sub_tag_df.drop_duplicates()
    for decade in decades:
        sub_tag_df[decade] = 0
    # 填充矩阵
    for index, row in album_sub_tag_df.iterrows():
        album_name = row['name']
        decade = row['decade_label']
        if decade in decades and album_name in sub_tag_df.index:
            sub_tag_df.at[album_name, decade] = 1
    tag_count_df = album_sub_tag_df.groupby('name').size().reset_index(name='count')
    # 获取 artist 列并添加到 tag_count_df 中
    tag_count_df = tag_count_df.merge(album_sub_tag_df[['name', 'artist']].drop_duplicates(), on='name')
    # 打印结果
    tag_count_df = tag_count_df[['artist', 'count']].sort_values('count', ascending=False)
    tag_count_df = tag_count_df.drop_duplicates()
    # tag_count_df
    # 从 DataFrame 中随机选取 20 行
    sampled_df = tag_count_df.sample(n=20)
    # 将 'artist' 列转换为列表
    artists_list = sampled_df['artist'].tolist()
    # 将列表转换为字符串，使用逗号分隔
    artists_str = ', '.join(artists_list)
    decade_prefer = create_binary_list_decade(decade_prefer)
    input_str = subTag_prefer + decade_prefer
    result = recmd(input_str, sub_tag_df)
    return result, artists_str

