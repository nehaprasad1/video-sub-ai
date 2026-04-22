let video = document.getElementById("videoPlayer");
let subtitleBox = document.getElementById("subtitleBox");
let segments = [];

// upload video + get subtitles
async function uploadVideo() {

    let file = document.getElementById("videoInput").files[0];

    if (!file) {
        alert("Please select a video");
        return;
    }

    let formData = new FormData();
    formData.append("file", file);

    // call backend
    let res = await fetch("http://127.0.0.1:8000/transcribe", {
        method: "POST",
        body: formData
    });

    let data = await res.json();

    console.log("Backend response:", data);

    // show video
    video.src = URL.createObjectURL(file);
    video.load();
    video.play();

    // fetch subtitles
    let subRes = await fetch(`http://127.0.0.1:8000/subtitle?file=${data.srt_file}`);
    let subData = await subRes.json();

    segments = parseSRT(subData.srt);
}


// convert SRT → JS format
function parseSRT(srt) {
    let blocks = srt.trim().split("\n\n");
    let result = [];

    for (let block of blocks) {
        let lines = block.split("\n");

        if (lines.length >= 3) {
            let time = lines[1].split(" --> ");

            result.push({
                start: toSeconds(time[0]),
                end: toSeconds(time[1]),
                text: lines.slice(2).join(" ")
            });
        }
    }

    return result;
}


// convert timestamp → seconds
function toSeconds(time) {
    let [h, m, s] = time.split(":");
    let [sec, ms] = s.split(",");

    return (
        parseInt(h) * 3600 +
        parseInt(m) * 60 +
        parseInt(sec) +
        parseInt(ms) / 1000
    );
}


// sync subtitles with video
video.addEventListener("timeupdate", () => {

    let current = video.currentTime;
    let text = "";

    for (let i = 0; i < segments.length; i++) {
        if (current >= segments[i].start && current <= segments[i].end) {
            text = segments[i].text;
            break;
        }
    }

    subtitleBox.innerText = text;
});