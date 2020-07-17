var notifier = new Notifier({
    pSuccess: {
        textColor: "#E5E5E5",
        borderColor: "#424249",
        backgroundColor: "#060608",
        progressColor: "#D0AC6E",
        iconColor: "#D0AC6E",
        position: "top-right",
        icon: "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"8\" height=\"8\" viewBox=\"0 0 8 8\"><path d=\"M6.41 0l-.69.72-2.78 2.78-.81-.78-.72-.72-1.41 1.41.72.72 1.5 1.5.69.72.72-.72 3.5-3.5.72-.72-1.44-1.41z\" transform=\"translate(0 1)\" /></svg>"
    },
    pError: {
        textColor: "#E5E5E5",
        borderColor: "#424249",
        backgroundColor: "#060608",
        progressColor: "#CE6D6E",
        iconColor: "#CE6D6E",
        position: "top-right",
        icon: "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"8\" height=\"8\" viewBox=\"0 0 8 8\"><path d=\"M1.41 0l-1.41 1.41.72.72 1.78 1.81-1.78 1.78-.72.69 1.41 1.44.72-.72 1.81-1.81 1.78 1.81.69.72 1.44-1.44-.72-.69-1.81-1.78 1.81-1.81.72-.72-1.44-1.41-.69.72-1.78 1.78-1.81-1.78-.72-.72z\"/></svg>"
    },
    pWarn: {
        textColor: "#E5E5E5",
        borderColor: "#424249",
        backgroundColor: "#060608",
        progressColor: "#74C19C",
        iconColor: "#74C19C",
        position: "top-right",
        icon: "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"8\" height=\"8\" viewBox=\"0 0 8 8\"><path d=\"M3.09 0c-.06 0-.1.04-.13.09l-2.94 6.81c-.02.05-.03.13-.03.19v.81c0 .05.04.09.09.09h6.81c.05 0 .09-.04.09-.09v-.81c0-.05-.01-.14-.03-.19l-2.94-6.81c-.02-.05-.07-.09-.13-.09h-.81zm-.09 3h1v2h-1v-2zm0 3h1v1h-1v-1z\" /></svg>"
    },
    pInfo: {
        textColor: "#E5E5E5",
        borderColor: "#424249",
        backgroundColor: "#060608",
        progressColor: "#74C19C",
        iconColor: "#74C19C",
        position: "top-right",
        icon: "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"8\" height=\"8\" viewBox=\"0 0 8 8\"><path d=\"M3 0c-.55 0-1 .45-1 1s.45 1 1 1 1-.45 1-1-.45-1-1-1zm-1.5 2.5c-.83 0-1.5.67-1.5 1.5h1c0-.28.22-.5.5-.5s.5.22.5.5-1 1.64-1 2.5c0 .86.67 1.5 1.5 1.5s1.5-.67 1.5-1.5h-1c0 .28-.22.5-.5.5s-.5-.22-.5-.5c0-.36 1-1.84 1-2.5 0-.81-.67-1.5-1.5-1.5z\" transform=\"translate(2)\" /></svg>"
    },
    position: "top-right",

});
function norify(types, mess, time = 3000) {
    notifier.notify("" + types + "", "" + mess + "", time);
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

document.getElementById("defaultOpen").click();
$(document).ready(function () {
    console.log("fgb")
    //upload ..update profile
    $('#svgsvgsvg').click(function () {
        console.log("sdfghj")
        var dataArray = $('#updateProfile').serializeArray();
        if (dataArray[1].value == "" || dataArray[2].value == "" || dataArray[3].value == "" || dataArray[4].value == "" || dataArray[5].value == "") {
            norify("pError", "Fill out all the information", 1000);
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
                    norify("pSuccess", "Profile Updated", 1500)
                },
                fail: function () {
                    norify("pError", "Couldn't Update your profile", 1500)
                }
            });

        }

    });
    //select and display image

});