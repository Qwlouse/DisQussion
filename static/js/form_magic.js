/**
 * @param frm The VotingForm used to vote for this node
 *
 */
function submit_vote_for_text_node(frm) {
    var consent = 0;
    for (var i = 0; i < frm.consent.length; i++) {
        if (frm.consent[i].checked) {
            consent = frm.consent[i].value;
        }
    }
    var wording = 0;
    for (var j = 0; j < frm.wording.length; j++) {
        if (frm.wording[j].checked) {
            wording = frm.wording[j].value;
        }
    }
    var text_id = frm.text_id.value;
    // alert('User voted consent: ' + consent + ", wording: " + wording + " for text " + text_id );
    // now the ajax stuff
    Dajaxice.structure.submitVoteForTextNode(updateGraph, {'text_id' : text_id, 'consent' : consent, 'wording' : wording});
}

function getOffset(el) {
    var _x = 0;
    var _y = 0;
    while (el && !isNaN(el.offsetLeft) && !isNaN(el.offsetTop)) {
        _x += el.offsetLeft - el.scrollLeft;
        _y += el.offsetTop - el.scrollTop;
        el = el.offsetParent;
    }
    return { top:_y, left:_x };
}

function process_vote(subEvent, vote_field, text_id) {
    var mainEvent = subEvent ? subEvent : window.event;
    var offset = getOffset(vote_field);
    var X = mainEvent.pageX - offset.left;
    var Y = mainEvent.pageY - offset.top;
    //alert("This button click occurred at: X(" + X + ") and Y(" + Y + ")");
    var vote_points = {0:[50, 70], 1:[36, 57], 2:[63, 57], 3:[22, 43], 4:[50, 43], 5:[77, 43], 6:[36, 29], 7:[63, 29], 8:[50, 16]};
    var nearest_point = 4;
    var nearest_dist = 1000;
    for (var i = 0; i <= 8; i++) {
        var dist = Math.sqrt((X - vote_points[i][0]) * (X - vote_points[i][0]) + (Y - vote_points[i][1]) * (Y - vote_points[i][1]))
        if (dist < nearest_dist) {
            nearest_dist = dist;
            nearest_point = i;
        }
    }
    //alert(nearest_point);
    var match_consent = {0:-1, 1:0, 2:-1, 3:1, 4:0, 5:-1, 6:1, 7:0, 8:1};
    var match_wording = {0:-1, 1:-1, 2:0, 3:-1, 4:0, 5:1, 6:0, 7:1, 8:1};
    Dajaxice.structure.submitVoteForTextNode(updateGraph, {'text_id':text_id, 'consent':match_consent[nearest_point], 'wording':match_wording[nearest_point]});
}

function updateVoting(data) {
    var vote_field = document.getElementById("vote_field_"+data["id"]);
    while ( vote_field.firstChild ) vote_field.removeChild( vote_field.firstChild );
    var dot = document.createElement("div");
    dot.style.width = "5px";
    dot.style.height = "5px";
    dot.style.position = "relative";
    var positions = {0:[50, 70], 1:[36, 57], 3:[63, 57], 2:[22, 43], 4:[50, 43], 6:[77, 43], 5:[36, 29], 7:[63, 29], 8:[50, 16]};
    dot.style.top = positions[(3*(data["wording"]+1)+data["consent"]+1)][1]-4+"px";
    dot.style.left = positions[(3*(data["wording"]+1)+data["consent"]+1)][0]-4+"px";
    dot.style.backgroundColor = "red";
    vote_field.appendChild(dot);
}

function submit_vote_for_structure_node(frm) {
    var consent = 0;
    for (var i = 0; i < frm.consent.length; i++) {
        if (frm.consent[i].checked) {
            consent = frm.consent[i].value;
        }
    }
    var wording = 0;
    for (var j = 0; j < frm.wording.length; j++) {
        if (frm.wording[j].checked) {
            wording = frm.wording[j].value;
        }
    }

    var node_id = frm.text_id.value;
    if (frm.consistent.value == 'False') {
        alert('Du zerstörst gerade deine abstimmung...');
    }
    //alert('User voted consent: ' + consent + ", wording: " + wording + ", node: " + node_id);
    // now the ajax stuff

    Dajaxice.structure.submitVoteForStructureNode(updateGraph, {'node_id' : node_id, 'consent' : consent, 'wording' : wording});
}