function showMicroblogging(microbloggingHTML) {
    var microblogDIV = document.getElementById('microblog');
    if (microblogDIV) {
        microblogDIV.innerHTML = microbloggingHTML;
    }
}

function follow(name) {
    Dajaxice.microblogging.follow(updateFollowing, {'username':name});
}

function unfollow(name) {
    Dajaxice.microblogging.unfollow(updateFollowing, {'username':name});
}

function referenceEntry(id,li) {
    Dajaxice.microblogging.reference(updateReferenceDisplay, {'id':id});

}