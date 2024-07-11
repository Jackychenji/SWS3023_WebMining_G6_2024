from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/index')
def home():
    # return render_template("index.html")
    return index()



@app.route('/music', methods=['GET', 'POST'])
def music():
    if request.method == 'POST':
        # 获取前端传回来的账号数据
        data = request.json
        print(data)
        account_data = data.get('account_data')
        print(f"Received account data: {account_data}")
        music_data = [
            {
                'name': 'Song A',
                'url': 'http://example.com/song_a',
                'artist': 'Artist A',
                'listeners': 12345,
                'release_date': '2023-01-01',
                'tracks': 10,
                'tag': 'pop'
            },
            {
                'name': 'Song B',
                'url': 'http://example.com/song_b',
                'artist': 'Artist B',
                'listeners': 54321,
                'release_date': '2023-02-01',
                'tracks': 12,
                'tag': 'rock'
            },
            {
                'name': 'Song C',
                'url': 'http://example.com/song_c',
                'artist': 'Artist C',
                'listeners': 67890,
                'release_date': '2023-03-01',
                'tracks': 8,
                'tag': 'jazz'
            }
        ]

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


@app.route('/team')
def team():
    return render_template("team.html")


if __name__ == '__main__':
    app.run()
