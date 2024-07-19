from flask import Flask, render_template, request, jsonify
import OnlyTag
import get_recommendation_data
import tag_based_recommendation
import sub_tag
import artistTable
import decadeTable

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/index')
def home():
    return index()


@app.route('/music', methods=['GET', 'POST'])
def music():
    if request.method == 'POST':
        # 获取前端传回来的账号数据
        data = request.json
        account_data = data.get('account_data')
        # 从CSV文件中读取数据
        code, df = get_recommendation_data.recommend(account_data)
        if code == -1:
            return jsonify(success=True, music_data=False)
        elif code == -2:
            music_data = tag_based_recommendation.recommending(df).to_dict(orient='records')
            return jsonify(success=True, music_data=music_data)
        elif code == 0:
            return jsonify(success=True, music_data=False)
        else:
            music_data = df.to_dict(orient='records')
            return jsonify(success=True, music_data=music_data)

    return render_template("music.html")


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        # 获取前端传回来的账号数据
        data = request.json
        account_data = data.get('account_data')
        name = get_recommendation_data.info(account_data)  # 直接使用字符串作为名字
        return jsonify(success=True, personal_info=name)

    return render_template("music.html")


@app.route('/choose', methods=['GET', 'POST'])
def tag():
    if request.method == 'POST':
        data = request.json
        tags = data.get('tags')
        next_tag, df = OnlyTag.onlyTagOperation(tags)

        df_with_name_column = df.reset_index().rename(columns={0: 'score'})
        df_with_name_column = df_with_name_column.drop_duplicates(subset=['name'])
        music_data = df_with_name_column.to_dict(orient='records')
        return jsonify(success=True, stags=next_tag, music_data=music_data)

    return render_template("choose.html")


@app.route('/stag', methods=['GET', 'POST'])
def stag():
    if request.method == 'POST':
        data = request.json
        stags = data.get('stags')
        tags = data.get('tags')
        df, decades = sub_tag.data_process(tags, stags)
        df_with_name_column = df.reset_index().rename(columns={0: 'score'})
        df_with_name_column = df_with_name_column.drop_duplicates(subset=['name'])
        music_data = df_with_name_column.to_dict(orient='records')
        return jsonify(success=True, decades=decades, music_data=music_data)

    return render_template("choose.html")


@app.route('/decade', methods=['GET', 'POST'])
def decade():
    if request.method == 'POST':
        data = request.json
        decades = data.get('decades')
        stags = data.get('stags')
        tags = data.get('tags')
        df, artists = decadeTable.data_process(tags, stags, decades)
        df_with_name_column = df.reset_index().rename(columns={0: 'score'})
        df_with_name_column = df_with_name_column.drop_duplicates(subset=['name'])
        music_data = df_with_name_column.to_dict(orient='records')
        return jsonify(success=True, artists=artists, music_data=music_data)

    return render_template("choose.html")


@app.route('/artist', methods=['GET', 'POST'])
def artist():
    if request.method == 'POST':
        data = request.json
        artists = data.get('artists')
        decades = data.get('decades')
        stags = data.get('stags')
        tags = data.get('tags')
        artist_str = data.get('artist_str')
        df = artistTable.data_process(tags, stags, decades, artist_str, artists)
        df_with_name_column = df.reset_index().rename(columns={0: 'score'})
        df_with_name_column = df_with_name_column.drop_duplicates(subset=['name'])
        music_data = df_with_name_column.to_dict(orient='records')
        return jsonify(success=True, music_data=music_data)

    return render_template("choose.html")


if __name__ == '__main__':
    app.run(host='172.25.101.70', port=8080, debug=False)