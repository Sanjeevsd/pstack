var notifier = new Notifier();

// Success 
document.getElementById("ex1notify1").onclick = function () {
    console.log("fgh", notifier)
    notifier.notify("error", "Successfully logged in!");
};


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
document.getElementById("defaultOpen").click();
var modal = document.getElementById("uploadprojectModal");
var btn = document.getElementById("uploadprojectsvg");
var span = document.getElementsByClassName("mclose")[0];
btn.onclick = function () {
    modal.style.display = "block";
}
span.onclick = function () {
    modal.style.display = "none";
}
window.onclick = function (event) {
    if (event.target == modal) {
        modal.style.display = "none";
        document.getElementById("pfileupload").value = ""
    }
}
var avatar = document.getElementById("profileavatarshow")
avatar.onclick = function () {
    document.getElementById("profileavatarshowupload").click()
}
jQuery("#profileavatarshowupload").on("change", function () {
    console.log("test");
    console.log(this.files[0]);
    var d = new FormData()
    console.log(d.append("asdf", this.files[0]));
});
document.getElementById('profileavatarshowupload').addEventListener('change', handleFileSelect, false);
function handleFileSelect(evt) {
    var files = evt.target.files;
    var f = files[0];
    var reader = new FileReader();

    reader.onload = (function (theFile) {
        return function (e) {
            document.getElementById('profileavatarshow').src = e.target.result;
        };
    })(f);

    reader.readAsDataURL(f);
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
$(document).ready(function () {
    console.log("fgb")
    //upload ..update profile
    $('#svgsvgsvg').click(function () {
        console.log("sdfghj")
        var dataArray = $('#updateProfile').serializeArray();
        if (dataArray[1].value == "" || dataArray[2].value == "" || dataArray[3].value == "" || dataArray[4].value == "" || dataArray[5].value == "") {
            console.log("EMpty");
        }
        else {
            var serialData = JSON.stringify(dataArray);
            var image_form = $("#profileavatarshowupload").get(0).files;
            var datas = new FormData();
            datas.append("serialData", serialData);
            if (image_form[0] == null) {
                datas.append("ifimage", "none");
            }
            else {
                datas.append("image_form", image_form[0]);
            }
            var udauneho = document.getElementById("savepaths")
            udauneho.style.cssText = "transform-origin: center; transform:rotate(360deg); transition: transform 0.2s ease;"
            $.ajax({
                headers: { 'X-CSRFToken': '{{ csrf_token }}' },
                url: '/updateProfile/',
                data: datas,
                type: 'post',
                cache: false,
                enctype: 'multipart/form-data',
                contentType: false,
                processData: false,
                success: function (response) {
                    $('#contentsskills').html(response.userprofile.skills);
                    $('#contentsintrests').html(response.userprofile.interests);
                    $('#contentsfblink').html(response.userprofile.fblink);
                    $('#contentsgitlink').html(response.userprofile.gitlink);
                    $('#contentsaboutme').html(response.userprofile.aboutme);

                    $('#openfblinka').attr("href", "" + response.userprofile.fblink + "");
                    $('#opengitlinka').attr("href", "" + response.userprofile.gitlink + "");
                    udauneho.style.cssText = "transform-origin: center; transform:rotate(0deg); transition: transform 0.2s ease;"
                }

            });

        }

    });
    //select and display image

});