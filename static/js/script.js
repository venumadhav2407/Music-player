const img = document.querySelector("#img");
const playPause = document.querySelector("#playpause");
const playPauseBtn = document.querySelector("#playpause-btn");
const audio = document.querySelector("#audio");
const musicId = document.getElementById("musicId");
const title = document.querySelector("#title");
const prevBtn = document.querySelector("#prevbtn");
const nextBtn = document.querySelector("#nextbtn");
const progress = document.querySelector("#progress");
const progressBar = document.querySelector(".progress-bar");
const currTime = document.querySelector(".current-time");
const totalDuration = document.querySelector(".duration-time");
const volume = document.querySelector("#volume");
const layer = document.querySelector(".layer");
const volBar = document.querySelector(".bar");
const progressLine = document.querySelector(".progress-line");
const volumeRange = document.querySelector(".volumerange");
const repeatBtn = document.querySelector("#repeat");
const likeBtn = document.querySelector("#like");
const likeIcon = document.querySelector("#likeicon");
const songListBtn = document.querySelector("#list");
const songList = document.querySelector("#songs-list");
const listCloseBtn = document.querySelector("#listclose");





// deafult song index 

let songIndex = 0;

let songs = [];
$(document).ready(function () {
    $.ajax(
        {
            url: "/songs",
            success: function (result) {
                let songslist = JSON.parse(result);
                songslist.forEach((data) => {
                    songs.push({ 'id' : data.id , 'path': data.path, 'displayName': data.title, 'artist': data.artist, 'cover': '/static/images/rythmimg.jpg' });
                });
                loadSong(songs[songIndex]);
                load_listofsongs();
            }
        });

});

function load_listofsongs() {
    let tracks = document.querySelector('.tracks');

    //creating a list or generating Html
    for (let i = 0; i < songs.length; i++) {

        let Html = ` <div class="song">
                    <div class="img">
                    <img src="${songs[i].cover}"/>
                    </div>
                    <div class="more">
                        <audio src="${songs[i].path}" id="music"></audio>
                        <div class="song_info">
                            <p id="title">${songs[i].displayName}</p>
                            <p id='artist'>${songs[i].artist}</p>
                        </div>
                        <button id="play_btn" onclick ="tracklistsong(`+ i +`);">
                        <i id ="icon`+ i +`" class="fas fa-play track-playpause"></i>
                        </button>
                    </div>
                </div>`;

        tracks.insertAdjacentHTML("beforeend", Html);
    };
}




// song default state

let isPlaying = false;


// song pause function

function playSong(indexsong) {
    isPlaying = true;
    playPauseBtn.classList.replace("fa-play", "fa-pause");
    if (indexsong != undefined)
    {
        let trackicon = document.getElementById('icon'+indexsong );
        var el = $('.track-playpause');
        el.removeClass('fa-pause');
        el.addClass('fa-play');
        trackicon.classList.replace("fa-play", "fa-pause");
        
    }
   
    audio.play();
}

// song play function

function pauseSong(indexsong) {
    isPlaying = false;
    playPauseBtn.classList.replace("fa-pause", "fa-play");
    if (indexsong != undefined) {
        let trackicon2 = document.getElementById('icon' + indexsong);
        trackicon2.classList.replace("fa-pause", "fa-play");
    }
    else {
        var el = $('.track-playpause');
        el.removeClass('fa-pause');
        el.addClass('fa-play');
    }
    audio.pause();
}

// loading songs

function loadSong(song) {
    img.src = song.cover;
    musicId.textContent = song.id;
    title.textContent = song.displayName;
    audio.src = song.path;

};

// previous song 

function prevSong() {
    songIndex--;
    if (songIndex < 0) {
        songIndex = songs.length - 1;
    }
    loadSong(songs[songIndex]);
    playSong(songIndex);
}

// next song

function nextSong() {
    songIndex++;
    if (songIndex > songs.length - 1) {
        songIndex = 0;
    }
    loadSong(songs[songIndex]);
    playSong(songIndex);
}

// track list playpause
function tracklistsong(songIndex) {
    let trackicon = document.querySelectorAll('.track-playpause');
        if (trackicon[songIndex].classList.contains("fa-pause")) {
            trackicon[songIndex].classList.replace("fa-pause", "fa-play");
            pauseSong(songIndex);
        }
        else {
            trackicon[songIndex].classList.replace("fa-play", "fa-pause");
            loadSong(songs[songIndex]);
            playSong(songIndex);
    }
}


function updateProgress(e) {
    if (isPlaying) {
        const { duration, currentTime } = e.target;
        // Update progress bar width
        const progressPercent = (currentTime / duration) * 100;
        progress.value = progressPercent;
        progressLine.style.width = `${progressPercent}%`;
        if (progressPercent == 100) {
            return nextSong();
        }
        // Calculate display for duration
        const durationMinutes = Math.floor(duration / 60);
        let durationSeconds = Math.floor(duration % 60);
        if (durationSeconds < 10) {
            durationSeconds = `0${durationSeconds}`;
        }
        // Delay switching duration Element to avoid NaN
        if (durationSeconds) {
            totalDuration.textContent = `${durationMinutes}:${durationSeconds}`;
        }
        // Calculate display for currentTime
        let currentMinutes = Math.floor(currentTime / 60);
        let currentSeconds = Math.floor(currentTime % 60);
        if (currentSeconds < 10) {
            currentSeconds = `0${currentSeconds}`;
        }
        currTime.textContent = `${currentMinutes}:${currentSeconds}`;
    }
}

function progressSlide(e) {
    const { value } = e.target;
    const progressTime = Math.ceil((audio.duration / 100) * value);
    audio.currentTime = progressTime;
    console.log(progressTime);
    if (!isPlaying) {
        progressLine.style.width = `${value}%`;
    }
}

function volumeBar() {
    layer.classList.toggle('hide');
    setTimeout(() => {
        if (layer.classList.contains("hide")) {
            layer.classList.remove("hide");
        }
    }, 5000);
}

function setVolume() {
    audio.volume = volumeRange.value;
    const barWidth = (volumeRange.value / 1) * 100;
    volBar.style.width = `${barWidth}%`;
}

function repeat() {
    repeatBtn.classList.toggle('color');
    const repeatBtnState = repeatBtn.classList.contains("color");
    if (repeatBtnState) {
        audio.loop = true;
        loadSong();
    } else {
        audio.loop = false;
        loadSong();
    }

}



function like() {
    if (likeBtn.classList.toggle('color')) {
        likeIcon.classList.replace('far', 'fas');
    } else {
        likeIcon.classList.replace('fas', 'far');
    }
}

$(document).ready(function () {
    // add-to-playlist
    $('.add-to-playlist').on("click", function() {
        // Retrieve music ID from data attribute
        var musicId = $("#musicId").text();
        var playlistId = $(this).attr('data-playlist-id');
        $.ajax({
            url: '/add_to_playlist', 
            type: 'POST',
            data: {
                music_id: musicId,
                playlist_id: playlistId
            },
            success: function(response) {
                // Handle success response, if needed
                console.log('Music liked:', response);
            },
            error: function(error) {
                // Handle error response, if needed
                console.log('Error liking music:', error);
            }
        });
    });

    // remove-from-playlist
    $('.remove-from-playlist').on("click", function() {
        // Retrieve music ID from data attribute
        var musicId = $("#musicId").text();
        var playlistId = $(this).attr('data-playlist-id');
        $.ajax({
            url: '/remove_from_playlist', 
            type: 'POST',
            data: {
                music_id: musicId,
                playlist_id: playlistId
            },
            success: function(response) {
                // Handle success response, if needed
                console.log('Music liked:', response);
                // Update UI to indicate music is liked, if needed
                // $('#likeicon').removeClass('far').addClass('fas');
            },
            error: function(error) {
                // Handle error response, if needed
                console.log('Error liking music:', error);
            }
        });
    });
});



playPause.addEventListener("click", () => (isPlaying ? pauseSong() : playSong()));
prevBtn.addEventListener("click", prevSong);
nextBtn.addEventListener("click", nextSong);
audio.addEventListener("timeupdate", updateProgress);
progress.addEventListener("input", progressSlide);
volume.addEventListener("click", volumeBar);
volumeRange.addEventListener("input", setVolume);
repeatBtn.addEventListener("click", repeat);
likeBtn.addEventListener("click", like);
// songListBtn.addEventListener("click", musicList);
