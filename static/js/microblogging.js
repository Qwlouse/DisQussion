function showMicroblogging(data) {
    var microblogDIV = document.getElementById('microblog');
    if (microblogDIV) {
        microblogDIV.innerHTML = data['html'];
        microblogDIV.untilNo = data['until_no'];
        microblogDIV.loading = false;
    }
}

function appendMicroblogging(data) {
    var microblogDIV = document.getElementById('microblog');
    if (microblogDIV) {
        microblogDIV.innerHTML += "\n" + data['html'];
        microblogDIV.untilNo = data['until_no'];
        microblogDIV.loading = false;
    }
}

function reloadTest() {
    var microblogDIV = document.getElementById('microblog');
    if (!microblogDIV.loading) {
        if ((microblogDIV.scrollHeight - 1300) <= document.body.scrollTop) {
            var graphNode = document.getElementById('graph');
            if (graphNode) {
                microblogDIV.loading = true;
                Dajaxice.microblogging.getNodeActivities(appendMicroblogging, {'id':graphNode.currentID,
                    'type':graphNode.currentType,
                    'no':microblogDIV.untilNo});
            } else {
                microblogDIV.loading = true;
                Dajaxice.microblogging.getAllActivities(appendMicroblogging, {'no':microblogDIV.untilNo});
            }
        }
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