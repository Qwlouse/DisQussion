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

function referenceEntry(id,li) {
    Dajaxice.microblogging.reference(updateReferenceDisplay, {'id':id});

}

function updateReferenceDisplay(id_str) {
    var li =  document.getElementById("reference_link_"+id_str)
    li.innerHTML = "Weitergesagt";
    li.setAttribute("class", "reference_done");
}