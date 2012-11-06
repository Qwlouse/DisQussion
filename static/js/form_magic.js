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

function relMouseCoords(event){
    var totalOffsetX = 0;
    var totalOffsetY = 0;
    var divX = 0;
    var divY = 0;
    var currentElement = this;

    do{
        totalOffsetX += currentElement.offsetLeft - currentElement.scrollLeft;
        totalOffsetY += currentElement.offsetTop - currentElement.scrollTop;
    }
    while(currentElement = currentElement.offsetParent)

    divX = event.pageX - totalOffsetX;
    divY = event.pageY - totalOffsetY;

    if (event.offsetX !== undefined && event.offsetY !== undefined) { return {x:event.offsetX, y:event.offsetY}; }
    return {x:divX, y:divY}
}
HTMLDivElement.prototype.relMouseCoords = relMouseCoords;

function process_vote(subEvent, vote_field, is_structure_node, db_id) {
    var mainEvent = subEvent ? subEvent : window.event;
    var coords = vote_field.relMouseCoords(mainEvent);
    var X = coords.x;
    var Y = coords.y;
    //alert("This button click occurred at: X(" + X + ") and Y(" + Y + ")");
    var vote_points = {0:[50, 70], 1:[36, 56], 2:[64, 56], 3:[23, 43], 4:[50, 43], 5:[77, 43], 6:[36, 29], 7:[64, 29], 8:[50, 16]};
    var nearest_point = 4;
    var nearest_dist = 1000;
    for (var i = 0; i <= 8; i++) {
        var dist = Math.sqrt((X - vote_points[i][0]) * (X - vote_points[i][0]) + (Y - vote_points[i][1]) * (Y - vote_points[i][1]))
        if (dist < nearest_dist) {
            nearest_dist = dist;
            nearest_point = i;
        }
    }
    var match_consent = {0:-1, 1:0, 2:-1, 3:1, 4:0, 5:-1, 6:1, 7:0, 8:1};
    var match_wording = {0:-1, 1:-1, 2:0, 3:-1, 4:0, 5:1, 6:0, 7:1, 8:1};
    if (is_structure_node) {
        Dajaxice.structure.submitVoteForStructureNode(updateGraph, {'node_id':db_id, 'consent':match_consent[nearest_point], 'wording':match_wording[nearest_point]});
    } else {
        Dajaxice.structure.submitVoteForTextNode(updateGraph, {'text_id':db_id, 'consent':match_consent[nearest_point], 'wording':match_wording[nearest_point]});
    }
}

function updateVoting(data) {
    var vote_field = document.getElementById("vote_field_" + data["id"]);
    if (data["wording"] <= 1 && data["consent"] <= 1 && vote_field) {
        while (vote_field.firstChild) vote_field.removeChild(vote_field.firstChild);
        var dot = document.createElement("div");
        dot.style.width = "6px";
        dot.style.height = "6px";
        dot.style.borderRadius = "3px";
        dot.style.border = "1px solid #AF0000";
        dot.style.position = "relative";
        var positions = {0:[50, 70], 1:[36, 56], 3:[64, 56], 2:[23, 43], 4:[50, 43], 6:[77, 43], 5:[36, 29], 7:[64, 29], 8:[50, 16]};
        dot.style.top = positions[(3 * (Math.round(data["wording"]) + 1) + Math.round(data["consent"]) + 1)][1] - 6 + "px";
        dot.style.left = positions[(3 * (Math.round(data["wording"]) + 1) + Math.round(data["consent"]) + 1)][0] - 5 + "px";
        dot.style.backgroundColor = "red";
        vote_field.appendChild(dot);
    }
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