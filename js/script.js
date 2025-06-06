let loggedIn = false;
let settingPref = false;
let song = "";
const songFiles = new Map([
    ["song1", "./audio/2021--1H13.wav"],
    ["song2", "./audio/Aftertune - Travel The World (Original Mix).wav"],
    ["song3", "./audio/Little Sminke Pinkie.wav"],
    ["song4", "./audio/Mystagogue.wav"]
])

const songImgs = new Map([
    ["song1", "./images/song1.png"],
    ["song2", "./images/song2.png"],
    ["song3", "./images/song3.png"],
    ["song4", "./images/song4.png"]
])

const songNames = new Map([
    ["song1", "2021--1H13"],
    ["song2", "Aftertune - Travel The World (Original Mix)"],
    ["song3", "Little Sminke Pinkie"],
    ["song4", "Mystagogue"]
])

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
    document.getElementById("audioSource").src = songFiles.get(buttonid);
    document.getElementById("audioControl").load();
    document.getElementById("audioImage").src = songImgs.get(buttonid);
    document.getElementById("audioControl").play();
    document.getElementById("songName").innerHTML = "Playing Right Now: " + songNames.get(buttonid);
}


/*-------------------------------------------------------------------------------------------------------------*/


async function getMusicRecommendation(description) {
  try {
    // Replace with the full URL if calling from a different domain
    const response = await fetch('http://localhost:9004/api/recommend', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ musicDescription: description }),
    });

    if (!response.ok) {
      // Handle HTTP errors
      const errorData = await response.json();
      console.error('Error from API:', response.status, errorData);
      throw new Error(`API Error: ${response.status} ${errorData.details || response.statusText}`);
    }

    const data = await response.json();
    console.log('Recommendation:', data.recommendation);
    return data.recommendation;

  } catch (error) {
    console.error('Failed to send request or parse response:', error);
    // Handle other errors (e.g., network issues)
    throw error;
  }
}

function getRec(description) {
    getMusicRecommendation(description).then(recommendation => {
    // Do something with the recommendation, e.g., display it on your page
    alert(`Suggested for you: ${recommendation}`);
  })
  .catch(error => {
    // Handle any errors that occurred during the process
    alert(`Could not get recommendation: ${error.message}`);
  });
}
