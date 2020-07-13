


document.getElementById("heartrate").addEventListener("click", glowheart);
function glowheart() {
    if (document.getElementById("heartrate").classList.contains("liked")) {
        document.getElementById("heartrate").style.stroke = "#424249"
        document.getElementById("heartrate").style.strokeWidth = "1"
        document.getElementById("heartrate").style.fill = "none"
        document.getElementById("heartrate").classList.remove("liked")
    }
    else {
        document.getElementById("heartrate").style.stroke = "none"
        document.getElementById("heartrate").style.fill = "#d19c42"
        document.getElementById("heartrate").classList.add("liked")
    }
}