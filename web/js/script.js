let loggedIn = false;
let settingPref = false;
let song = "";

let data;

const types = ["excite", "relax", "sad", "happy", "intense", "moody"]
const excite = ["Wonderwall", "Somebody Told Me", "Supermassive Black Hole", "Dani California", "Paint It Black"]
const relax = ["Let It Be", "Another Brick in the Wall (Part 2)", "Bookends", "Sweet Thing", "Been Down So Long"]
const sad = ["Creep", "The Scientist", "Fix You", "Bohemian Rhapsody", "No Surprises"]
const happy = ["Feel Good Inc.", "Song 2", "Reptilia", "Back in Black", "No One Knows"]
const intense = ["Mr. Brightside", "Clocks", "Chop Suey!", "In the End", "When You Were Young"]
const moody = ["Take Me Out", "Karma Police", "Under the Bridge", "Seven Nation Army", "Lithium"]


document.getElementById("updatePreferences").style.visibility = "hidden";
document.getElementById("preferences").style.visibility = "hidden";

function updateUser() {
    loggedIn = !loggedIn;

    if (loggedIn) {
        document.getElementById("user").innerHTML = "logged in!";
        document.getElementById("preferences").style.visibility = "visible";

    }
    else {
        document.getElementById("user").innerHTML = "not logged in!";
        document.getElementById("preferences").style.visibility = "hidden";
        document.getElementById("updatePreferences").style.visibility = "hidden";
    }
}

function preferenceVisibility() {
    if (settingPref == false) {
        settingPref = true;
        document.getElementById("updatePreferences").style.visibility = "visible";
    }

    else {
        settingPref = false;
        document.getElementById("updatePreferences").style.visibility = "hidden";
    }
}

function updateSongChoice(id, songName) {
    document.getElementById(id).innerHTML = songName;
}

function updateSong(i) {
    document.getElementById("audioSource").src = data.preview[i];
    document.getElementById("audioControl").load();
    document.getElementById("audioControl").play();
    document.getElementById("songName").innerHTML = "Playing Right Now: " + data.song_name[i] + " by " + data.artist[i];
}

/*-------------------------------------------------------------------------------------------------------------*/
function pickTypeAndSong(buttonid) {
    switch (buttonid) {
        case "energetic":
            type = "excite";
        case "relaxed":
            type = "relax";
        case "sad":
            type = "sad";
        case "happy":
            type = "happy";
        case "intense":
            type = "intense";
        default: //moody
            type = "moody";
    }
    let song = "";
    switch (type) {
        case "excite":
            song = excite[Math.floor(Math.random()*5)];
        case "relax":
            song = relax[Math.floor(Math.random()*5)];
        case "sad":
            song = sad[Math.floor(Math.random()*5)];
        case "happy":
            song = happy[Math.floor(Math.random()*5)];
        case "intense":
            song = intense[Math.floor(Math.random()*5)];
        default: //moody
            song = moody[Math.floor(Math.random()*5)];
    }
    return [type, song]
}

async function getRec(buttonid) {
    let songName = pickTypeAndSong(buttonid)[1];
    const url = `/get_rec?song_name=${encodeURIComponent(songName)}`;
    const response = await fetch(url);

    data = await response.json();

    updateSongChoice("song1", data.song_name[0]);
    updateSongChoice("song2", data.song_name[1]);
    updateSongChoice("song3", data.song_name[2]);
    updateSongChoice("song4", data.song_name[3]);
}
