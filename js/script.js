let loggedIn = false;
let settingPref = false;

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

function updateSong(buttonid) {
    document.getElementById(buttonid).innerHTML = document.getElementById(buttonid).innerHTML;
}
