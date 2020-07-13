

$(document).ready(function () {
    $('#svgsvgsvg').click(function () {
        var serialData = $('#updateProfile').serialize();
        $.ajax({
            url: '/updateProfile/',
            data: serialData,
            type: 'post',
            success: function (response) {
                $('#contentsskills').html(response.userprofile.skills);
                $('#contentsintrests').html(response.userprofile.interests);
                $('#contentsfblink').html(response.userprofile.fblink);
                $('#contentsgitlink').html(response.userprofile.gitlink);
                $('#contentsaboutme').html(response.userprofile.aboutme);

                $('#openfblinka').attr("href", "" + response.userprofile.fblink + "");
                $('#opengitlinka').attr("href", "" + response.userprofile.gitlink + "");
            }

        });
    });
});
function updateprof() {
    var skills = document.forms["editprofile"]["skills"].values;
    var interests = document.forms["editprofile"]["interests"].values;
    var aboutme = document.forms["editprofile"]["aboutme"].values;
    var fblink = document.forms["editprofile"]["fblink"].values;
    var gitlink = document.forms["editprofile"]["gitlink"].values;
    if (skills != "" || interests != "" || fblink != "" || gitlink != "") {
        console.log("...")
    }
    else {
        var udauneho = document.getElementById("savepaths")
        udauneho.style.cssText = "transform-origin: center; transform:rotate(180deg); transition: transform 0.2s ease;"
        var upanimation = document.getElementById("editsecction")
        setTimeout(() => { upanimation.style.cssText = "transform-origin:top;  transform:translate(0,-50rem); transition: all 1s ease;" }, 500);
        setTimeout(() => { upanimation.style.cssText = "transform-origin:top;  transform:translate(0,0); transition: all 1s ease;" }, 2000);
        setTimeout(() => { udauneho.style.cssText = "transform-origin: center; transform:rotate(0deg); transition: transform 0.2s ease;" }, 2500);
    }
}


function openCity(evt, tabname) {
    var sidelist = { "home": "Home", "contacts": "Contacts", "profile": "Edit Profile", "projecttab": "My Projects", "notifications": "Notifications", "recommendations": "Recommendations", "popularprojects": "Popular Projects" }
    if (tabname === "home") {
        document.getElementById("filters").style.display = "block"
        document.getElementById("topics").style.visibility = "collapse"

    }
    else {
        document.getElementById("filters").style.display = "none"
        document.getElementById("topics").style.visibility = "visible"
        document.getElementById("topics").innerHTML = sidelist[tabname]
    }
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("main");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("side-item");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(tabname).style.display = "block";
    evt.currentTarget.className += " active";

    if (evt.currentTarget.className === "openerprofile active") {
        document.getElementById("mprofiles").classList.add("active")
        document.getElementById("openerprofile").classList.remove("active")

    }

}
document.getElementById("defaultOpen").click();

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