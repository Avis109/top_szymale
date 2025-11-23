let reversed=false;

async function loadSongs(){
  const res = await fetch('/songs');
  const data = await res.json();
  data.sort((a,b)=>b.votes-a.votes);
  const list = reversed ? data.reverse() : data;
  const container = document.getElementById('songs');
  container.innerHTML = list.map((s,i)=>`
    <div class="song">
      <b>${i+1}. ${s.title}</b> — ${s.artist} | ${s.votes} głosów
      <div>
        <button onclick="vote(${i})">Głosuj</button>
        <button onclick="announceAndPlay(${i})">Odtwórz z zapowiedzią</button>
      </div>
      <div class="player">
        <iframe src="https://open.spotify.com/embed/track/${s.spotify}" width="300" height="80" frameborder="0" allow="encrypted-media"></iframe>
      </div>
    </div>
  `).join('');
}

async function vote(i){
  await fetch('/vote/'+i, {method:'POST'});
  await loadSongs();
}

function toggleOrder(){
  reversed = !reversed;
  loadSongs();
}
document.getElementById('toggleBtn').addEventListener('click', toggleOrder);

async function searchSong(){
  const q = document.getElementById('searchInput').value;
  if(!q) return;
  const res = await fetch('/search?q=' + encodeURIComponent(q));
  const data = await res.json();
  if(data.error){
    alert(data.error);
    return;
  }
  window.searchResults = data;
  const resultsDiv = document.getElementById('results');
  resultsDiv.innerHTML = data.map((s,i)=>`
    <div class="songResult">
      <img src="${s.album_img}" width="50" /> <b>${s.title}</b> — ${s.artist}
      <button onclick="add(${i})">Dodaj do rankingu</button>
    </div>
  `).join('');
}
document.getElementById('searchBtn').addEventListener('click', searchSong);

async function add(i){
  const song = window.searchResults[i];
  await fetch('/songs', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(song)});
  await loadSongs();
}

function announceAndPlay(index){
  // get current sorted list to find actual position
  fetch('/songs').then(r=>r.json()).then(list=>{
    list.sort((a,b)=>b.votes-a.votes);
    const item = list[index];
    const pos = index + 1;
    // Speak using browser TTS
    const msg = new SpeechSynthesisUtterance('Miejsce ' + pos + ' na liście Top.');
    window.speechSynthesis.speak(msg);
    // After a short delay, play the embedded player by focusing iframe (can't auto-play due to browser policies)
    // The user can press play on the iframe manually if autoplay blocked.
    // Optionally, we can set focus:
    setTimeout(()=>{ const iframes = document.getElementsByTagName('iframe'); if(iframes[index]) iframes[index].focus(); }, 800);
  });
}

window.addEventListener('DOMContentLoaded', loadSongs);
