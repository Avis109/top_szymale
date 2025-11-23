TOP Spotify Ranking - instrukcja uruchomienia i wdrożenia
=========================================

Pliki:
- app.py             (Flask backend)
- songs.json         (baza rankingów)
- config.example.json (przykład konfiguracji z CLIENT ID/SECRET)
- requirements.txt
- Procfile
- render.yaml
- templates/index.html
- static/app.js
- static/style.css

1) Lokalnie:
- Skopiuj config.example.json -> config.json i wpisz swoje Spotify credentials
  OR ustaw zmienne środowiskowe SPOTIFY_CLIENT_ID i SPOTIFY_CLIENT_SECRET
  (env vars mają pierwszeństwo).
- Zainstaluj zależności:
    pip install -r requirements.txt
- Uruchom:
    python app.py
- Otwórz http://127.0.0.1:5000

2) Wdrożenie na Render:
- Utwórz repo na GitHub i wypchnij projekt
- Na render.com wybierz New -> Web Service -> wybierz repo
- W ustawieniach serwisu dodaj zmienne środowiskowe:
    SPOTIFY_CLIENT_ID
    SPOTIFY_CLIENT_SECRET
- Start command: gunicorn app:app
- Deploy

3) Uwagi:
- Aplikacja używa Spotify Client Credentials flow (tylko do wyszukiwania).
- Odtwarzanie w iframe może wymagać ręcznego kliknięcia Play (autoplay blokowane przez przeglądarki).
- Funkcja zapowiedzi używa przeglądarkowego TTS (SpeechSynthesis).

Jeśli chcesz, mogę spakować projekt do ZIP i podać link do pobrania.
