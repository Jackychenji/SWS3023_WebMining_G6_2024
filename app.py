from flask import Flask, render_template, request, jsonify
import pandas as pd

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
        print(data)
        account_data = data.get('account_data')
        print(f"Received account data: {account_data}")

        # 从CSV文件中读取数据
        df = pd.read_csv('music_data.csv')

        # 假设你根据某些逻辑处理数据，例如这里简单地返回前3条数据
        music_data = df.head(3).to_dict(orient='records')
        
        return jsonify(success=True, music_data=music_data)
    return render_template("music.html")


@app.route('/choose', methods=['GET', 'POST'])
def choose():
    if request.method == 'POST':
        data = request.json
        print(data)
        feedback = data.get('feedback')
        audio_src = data.get('audioSrc')
        print(f"Received feedback: {feedback} for audio source: {audio_src}")
        return jsonify(success=True, feedback=feedback, audioSrc=audio_src)

    return render_template("choose.html")


if __name__ == '__main__':
    app.run(debug=True)
