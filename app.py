from flask import Flask, jsonify, request, render_template
import json

app = Flask(__name__)
DATA_FILE = "songs.json"

def load_songs():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_songs(songs):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(songs, f, indent=2, ensure_ascii=False)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/songs", methods=["GET"])
def get_songs():
    return jsonify(load_songs())

@app.route("/songs", methods=["POST"])
def add_song():
    data = request.json
    songs = load_songs()
    songs.append({
        "title": data["title"],
        "artist": data["artist"],
        "votes": 0
    })
    save_songs(songs)
    return jsonify({"status": "added"})

@app.route("/vote/<int:song_id>", methods=["POST"])
def vote(song_id):
    songs = load_songs()
    songs[song_id]["votes"] += 1
    save_songs(songs)
    return jsonify({"status": "voted"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
