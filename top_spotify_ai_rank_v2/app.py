from flask import Flask, jsonify, request, render_template
import json, requests, base64, os

app = Flask(__name__)
DATA_FILE = "songs.json"
CONFIG_FILE = "config.json"

def load_config():
    # Try env vars first, then config file if present
    cfg = {}
    cfg['SPOTIFY_CLIENT_ID'] = os.getenv('SPOTIFY_CLIENT_ID')
    cfg['SPOTIFY_CLIENT_SECRET'] = os.getenv('SPOTIFY_CLIENT_SECRET')
    if not cfg['SPOTIFY_CLIENT_ID'] or not cfg['SPOTIFY_CLIENT_SECRET']:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                file_cfg = json.load(f)
            cfg['SPOTIFY_CLIENT_ID'] = cfg['SPOTIFY_CLIENT_ID'] or file_cfg.get('SPOTIFY_CLIENT_ID')
            cfg['SPOTIFY_CLIENT_SECRET'] = cfg['SPOTIFY_CLIENT_SECRET'] or file_cfg.get('SPOTIFY_CLIENT_SECRET')
    return cfg

def get_spotify_token(client_id, client_secret):
    auth_str = f"{client_id}:{client_secret}"
    b64_auth = base64.b64encode(auth_str.encode()).decode()
    headers = {"Authorization": f"Basic {b64_auth}"}
    data = {"grant_type": "client_credentials"}
    r = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data, timeout=10)
    r.raise_for_status()
    return r.json().get("access_token")

def search_spotify(query, token):
    headers = {"Authorization": f"Bearer {token}"}
    params = {"q": query, "type": "track", "limit": 6}
    r = requests.get("https://api.spotify.com/v1/search", headers=headers, params=params, timeout=10)
    r.raise_for_status()
    results = r.json().get("tracks", {}).get("items", [])
    out = []
    for t in results:
        img = ""
        if t.get("album", {}).get("images"):
            img = t["album"]["images"][0]["url"]
        out.append({
            "title": t["name"],
            "artist": ", ".join([a["name"] for a in t.get("artists", [])]),
            "spotify": t["id"],
            "album_img": img
        })
    return out

def load_songs():
    if not os.path.exists(DATA_FILE):
        return []
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
    # avoid duplicates by spotify id
    if not any(s.get("spotify") == data.get("spotify") for s in songs):
        songs.append({ "title": data.get("title"), "artist": data.get("artist"), "spotify": data.get("spotify"), "votes": 0 })
        save_songs(songs)
    return jsonify({"ok": True})

@app.route("/vote/<int:song_id>", methods=["POST"])
def vote(song_id):
    songs = load_songs()
    if 0 <= song_id < len(songs):
        songs[song_id]["votes"] += 1
        save_songs(songs)
        return jsonify({"ok": True})
    return jsonify({"ok": False}), 400

@app.route("/search", methods=["GET"])
def search():
    q = request.args.get("q","").strip()
    if not q:
        return jsonify([])
    cfg = load_config()
    client_id = cfg.get("SPOTIFY_CLIENT_ID")
    client_secret = cfg.get("SPOTIFY_CLIENT_SECRET")
    if not client_id or not client_secret:
        return jsonify({"error": "Missing Spotify credentials. Create config.json or set environment variables."}), 500
    token = get_spotify_token(client_id, client_secret)
    results = search_spotify(q, token)
    return jsonify(results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
