import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# 读入文件
tags_df = pd.read_csv("song_all_tag.csv", index_col=False, header=0)
album_df = pd.read_csv('songs.csv')
user_album_df = pd.DataFrame(columns=album_df.columns)  # 后续建矩阵处理数据用

# 初始化：定义标签列表
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
big_tag_df = pd.DataFrame(0, index=album_df['name'].unique(), columns=genres)


# 计算推荐结果公用函数，prefer是读入的01一维数组，matrix_df是基于album数据的
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

# 输入19个大tag的选择，return小tag
sub_genre = []
sub_genre_str2 = []


def question2(prefer_genre, sub_genre_str1):
    # 初始化一个空的 DataFrame
    output_df = pd.DataFrame()
    # 拼接对应的标签
    if prefer_genre[0] == 1:
        sub_genre_str1.append("electronic")
        sub_genre_str2.append(electronic_tag)
        for tag in electronic_tag:
            output_df[tag] = 0
    if prefer_genre[1] == 1:
        sub_genre_str1.append("rock")
        sub_genre_str2.append(rock_tag)
        for tag in rock_tag:
            output_df[tag] = 0
    if prefer_genre[2] == 1:
        sub_genre_str1.append("hip-hop")
        sub_genre_str2.append(hip_hop_tag)
        for tag in hip_hop_tag:
            output_df[tag] = 0
    if prefer_genre[3] == 1:
        sub_genre_str1.append("indie")
        sub_genre_str2.append(indie_tag)
        for tag in indie_tag:
            output_df[tag] = 0
    if prefer_genre[4] == 1:
        sub_genre_str1.append("jazz")
        sub_genre_str2.append(jazz_tag)
        for tag in jazz_tag:
            output_df[tag] = 0
    if prefer_genre[5] == 1:
        sub_genre_str1.append("reggae")
        sub_genre_str2.append(reggae_tag)
        for tag in reggae_tag:
            output_df[tag] = 0
    if prefer_genre[6] == 1:
        sub_genre_str1.append("british")
        sub_genre_str2.append(british_tag)
        for tag in british_tag:
            output_df[tag] = 0
    if prefer_genre[7] == 1:
        sub_genre_str1.append("punk")
        sub_genre_str2.append(punk_tag)
        for tag in punk_tag:
            output_df[tag] = 0
    if prefer_genre[8] == 1:
        sub_genre_str1.append("80s")
        sub_genre_str2.append(eighties_tag)
        for tag in eighties_tag:
            output_df[tag] = 0
    if prefer_genre[9] == 1:
        sub_genre_str1.append("dance")
        sub_genre_str2.append(dance_tag)
        for tag in dance_tag:
            output_df[tag] = 0
    if prefer_genre[10] == 1:
        sub_genre_str1.append("acoustic")
        sub_genre_str2.append(acoustic_tag)
        for tag in acoustic_tag:
            output_df[tag] = 0
    if prefer_genre[11] == 1:
        sub_genre_str1.append("rnb")
        sub_genre_str2.append(rnb_tag)
        for tag in rnb_tag:
            output_df[tag] = 0
    if prefer_genre[12] == 1:
        sub_genre_str1.append("hardcore")
        sub_genre_str2.append(hardcore_tag)
        for tag in hardcore_tag:
            output_df[tag] = 0
    if prefer_genre[13] == 1:
        sub_genre_str1.append("country")
        sub_genre_str2.append(country_tag)
        for tag in country_tag:
            output_df[tag] = 0
    if prefer_genre[14] == 1:
        sub_genre_str1.append("blues")
        sub_genre_str2.append(blues_tag)
        for tag in blues_tag:
            output_df[tag] = 0
    if prefer_genre[15] == 1:
        sub_genre_str1.append("alternative")
        sub_genre_str2.append(alternative_tag)
        for tag in alternative_tag:
            output_df[tag] = 0
    if prefer_genre[16] == 1:
        sub_genre_str1.append("classical")
        sub_genre_str2.append(classical_tag)
        for tag in classical_tag:
            output_df[tag] = 0
    if prefer_genre[17] == 1:
        sub_genre_str1.append("rap")
        sub_genre_str2.append(rap_tag)
        for tag in rap_tag:
            output_df[tag] = 0
    if prefer_genre[18] == 1:
        sub_genre_str1.append("metal")
        sub_genre_str2.append(metal_tag)
        for tag in metal_tag:
            output_df[tag] = 0
    sub_genre.append(output_df.columns)  # 建矩阵有用，可以不接前端
    return output_df.columns.tolist(), recmd(prefer_genre, big_tag_df)


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


def onlyTagOperation(prefer_genre):
    prefer_genre = create_binary_list(prefer_genre)
    for index, row in album_df.iterrows():
        if row['tag'] in genres:
            big_tag_df.at[row['name'], row['tag']] = 1
    sub_genre_str1 = []
    return question2(prefer_genre, sub_genre_str1)

