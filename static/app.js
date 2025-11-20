let reversed = false;

function loadSongs() {
    fetch("/songs")
        .then(res => res.json())
        .then(data => {
            const sorted = data.sort((a, b) => b.votes - a.votes);
            const list = reversed ? sorted.reverse() : sorted;

            document.getElementById("songs").innerHTML = list.map((song, index) =>
                `<div class="song">
                    <b>${song.title}</b> – ${song.artist} |
                    Głosy: ${song.votes}
                    <button onclick="vote(${index})">Głosuj</button>
                </div>`
            ).join("");
        });
}

function addSong() {
    const title = document.getElementById("title").value;
    const artist = document.getElementById("artist").value;

    fetch("/songs", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({title, artist})
    }).then(() => loadSongs());
}

function vote(id) {
    fetch(`/vote/${id}`, { method: "POST" })
        .then(() => loadSongs());
}

function reverseList() {
    reversed = !reversed;
    loadSongs();
}

loadSongs();
