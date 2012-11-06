/**
 * @param frm The VotingForm used to vote for this node
 *
 */
//                          wording
//                 ----------------------------->
var vote_points = [[[49, 69], [62, 55], [76, 42]],  //  |
                   [[35, 55], [49, 41], [62, 28]],  //  |  consent
                   [[22, 41], [35, 29], [49, 14]]]; //  V


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

function calculate_coordinates(consent, wording){
    var p1 = vote_points[1][1];
    var p2, p3, cons_v, word_v, x, y;
    if (Math.abs(consent) > Math.abs(wording)) {
        if (consent >= 0) {
            p3 = vote_points[2][1];
            if (wording >= 0) {
                p2 = vote_points[2][2];
            } else {
                p2 = vote_points[2][0];
            }
        } else {
            p3 = vote_points[0][1];
            if (wording >= 0) {
                p2 = vote_points[0][2];

            } else {
                p2 = vote_points[0][0];
            }
        }
        cons_v = [p3[0] - p1[0], p3[1] - p1[1]];
        word_v = [p2[0] - p3[0], p2[1] - p3[1]];
    } else {
        if (wording >= 0) {
            p3 = vote_points[1][2];
            if (consent >= 0) {
                p2 = vote_points[2][2];
            } else {
                p2 = vote_points[0][2];
            }
        } else {
            p3 = vote_points[1][0];
            if (consent >= 0) {
                p2 = vote_points[2][0];
            } else {
                p2 = vote_points[0][0];
            }
        }
        cons_v = [p2[0] - p3[0], p2[1] - p3[1]];
        word_v = [p3[0] - p1[0], p3[1] - p1[1]];
    }
    x = p1[0] + Math.abs(consent)*cons_v[0] + Math.abs(wording)*word_v[0];
    y = p1[1] + Math.abs(consent)*cons_v[1] + Math.abs(wording)*word_v[1];
    return [x, y];
}

function process_vote(subEvent, vote_field, is_structure_node, db_id) {
    var mainEvent = subEvent ? subEvent : window.event;
    var coords = vote_field.relMouseCoords(mainEvent);
    var X = coords.x;
    var Y = coords.y;
    //alert("This button click occurred at: X(" + X + ") and Y(" + Y + ")");
    var nearest_point = 4;
    var nearest_dist = 1000;
    for (var c = -1; c <= 1; ++c) {
        for (var w = -1; w <= 1; ++w) {
            var dist = Math.sqrt(Math.pow(X - vote_points[c+1][w+1][0], 2) + Math.pow(Y - vote_points[c+1][w+1][1], 2));
            if (dist < nearest_dist) {
                nearest_dist = dist;
                nearest_point = [c, w];
            }
        }
    }
    if (is_structure_node) {
        if (!document.getElementById("text").textSource.votingInfo["consistent"]) {
            if (!confirm("Du hast Textknoten unterhalb dieser Ebene unterschiedlich abgestimmt. Wenn du jetzt zustimmst, werden alle Textknoten so abgestimmt, wie du eben entschieden hast. Diese Aktion kann nicht rückgängig gemacht werden.")) {
                return;
            }
        }
        document.getElementById("text").textSource.votingInfo["consistent"] = true;
        Dajaxice.structure.submitVoteForStructureNode(updateGraph, {'node_id':db_id, 'consent':nearest_point[0], 'wording':nearest_point[1]});
    } else {
        Dajaxice.structure.submitVoteForTextNode(updateGraph, {'text_id':db_id, 'consent':nearest_point[0], 'wording':nearest_point[1]});
    }
}

function updateVoting(data) {
    var vote_field = document.getElementById("vote_field_" + data["id"]);
    if (vote_field) {
        while (vote_field.firstChild) vote_field.removeChild(vote_field.firstChild);
        var all_dot = document.createElement("div");
        all_dot.style.width = "6px";
        all_dot.style.height = "6px";
        all_dot.style.borderRadius = "3px";
        all_dot.style.border = "1px solid #00AF00";
        all_dot.style.backgroundColor = "green";
        all_dot.style.position = "relative";
        var all_pos = calculate_coordinates(data["total_consent"], data["total_wording"]);
        all_dot.style.top = all_pos[1] - 4 + "px";
        all_dot.style.left = all_pos[0] - 4 + "px";
        vote_field.appendChild(all_dot);
        if (data["wording"] <= 1 && data["consent"] <= 1) {
        var own_dot = document.createElement("div");
        own_dot.style.width = "6px";
        own_dot.style.height = "6px";
        own_dot.style.borderRadius = "3px";
        if (data["consistent"]) {
            own_dot.style.border = "1px solid #0000AF";
            own_dot.style.backgroundColor = "blue";
        } else {
            own_dot.style.border = "1px solid #AF0000";
            own_dot.style.backgroundColor = "red";
        }
        own_dot.style.position = "relative";
        var own_pos = calculate_coordinates(data["consent"], data["wording"]);
        own_dot.style.top = own_pos[1] - 4 + "px";
        own_dot.style.left = own_pos[0] - 4 + "px";
        vote_field.appendChild(own_dot);
        }
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