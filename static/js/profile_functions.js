function follow(name) {
    Dajaxice.microblogging.follow(updateFollowing, {'username':name});
}

function unfollow(name) {
    Dajaxice.microblogging.unfollow(updateFollowing, {'username':name});
}

function updateFollowing(str) {
    if (str.charAt(0) == "1") {
        document.getElementById("follow_button").innerHTML = "Entfolgen";
        document.getElementById("follow_button").setAttribute("onClick","unfollow('"+str.substr(1)+"');");
    } else {
        document.getElementById("follow_button").innerHTML = "Folgen";
        document.getElementById("follow_button").setAttribute("onClick","follow('"+str.substr(1)+"');");
    }
}