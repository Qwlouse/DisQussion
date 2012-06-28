function closelogin() {
    document.getElementById("login").style.opacity = "1.0";
    closelogin_step();
}

function closelogin_step() {
    var opac = parseFloat(document.getElementById("login").style.opacity);
    document.getElementById("login").style.opacity = "" + (opac - 0.11);
    document.getElementById("login_overlay").style.opacity = "" + ((opac - 0.11)*0.5);
    if (opac >= 0.01) {
        setTimeout("closelogin_step()", 25);
    } else {
        document.getElementById("login_overlay").style.display = "none";
        document.getElementById("login").style.display = "none";
    }
}

function showlogin() {
    document.getElementById("login").style.display = "block";
    document.getElementById("login_overlay").style.display = "block";
    document.getElementById("login").style.opacity = "0.0";
    showlogin_step()
}

function showlogin_step() {
    var opac = parseFloat(document.getElementById("login").style.opacity);
    document.getElementById("login").style.opacity = "" + (opac + 0.11);
    document.getElementById("login_overlay").style.opacity = "" + ((opac + 0.11)*0.5);
    if (opac < 0.9) {
        setTimeout("showlogin_step()", 25);
    } else {
        document.getElementById("login").style.opacity = "1.0";
        document.getElementById("login_overlay").style.opacity = "0.5";
    }
}

function hideText() {
    document.getElementById("hauptText").firstChild.nextSibling.style.opacity = "1.0";
    hideText_step();
}

function hideText_step() {
    //alert(document.getElementById("hauptText").childNodes[1].style.opacity);
    var opac = parseFloat(document.getElementById("hauptText").childNodes[1].style.opacity);
    var i;
    for (i = 0; i < document.getElementById("hauptText").childNodes.length; i++) {
        if (document.getElementById("hauptText").childNodes[i].nodeType == 1) {
            document.getElementById("hauptText").childNodes[i].style.opacity = "" + (opac - 0.11);
        }
    }
    if (opac >= 0.01) {
        setTimeout("hideText_step()", 25);
    } else {
        for (i = 0; i < document.getElementById("hauptText").childNodes.length; i++) {
            if (document.getElementById("hauptText").childNodes[i].nodeType == 1) {
                document.getElementById("hauptText").childNodes[i].style.display = "none";
            }
        }
    }
}

function showText(sourceNode) {
    document.getElementById("hauptText").textSource = sourceNode;
    Dajaxice.structure.getNodeText(Dajax.process,{'node_id': sourceNode.getAttribute('id')});
    hideText();
    setTimeout("showText_intermission()", 425);
}

function showText_intermission() {
    var textHTML = document.getElementById("hauptText").textSource.textPart;
    var i, j;
    for (i = 0; i < document.getElementById("hauptText").childNodes.length; i++) {
        if (document.getElementById("hauptText").childNodes[i].nodeType == 1) {
            for (j = 0; j < document.getElementById("hauptText").childNodes[i].attributes.length; j++) {
                if (document.getElementById("hauptText").childNodes[i].attributes[j].name == "class") {
                    if (document.getElementById("hauptText").childNodes[i].attributes[j].value == "text") {
                        document.getElementById("hauptText").childNodes[i].innerHTML = textHTML;
                    }
                }
            }
        }
    }
    showText_step();
}

function showText_step() {
    var i, j;
    for (i = 0; i < document.getElementById("hauptText").childNodes.length; i++) {
        if (document.getElementById("hauptText").childNodes[i].nodeType == 1) {
            for (j = 0; j < document.getElementById("hauptText").childNodes[i].attributes.length; j++) {
                if (document.getElementById("hauptText").childNodes[i].attributes[j].name == "class") {
                    if (document.getElementById("hauptText").childNodes[i].attributes[j].value == "text") {
                        document.getElementById("hauptText").childNodes[i].style.display = "block";
                        var opac = parseFloat(document.getElementById("hauptText").childNodes[i].style.opacity);
                        document.getElementById("hauptText").childNodes[i].style.opacity = "" + (opac + 0.11);
                        if (opac < 0.9) {
                            setTimeout("showText_step()", 25);
                        } else {
                            document.getElementById("hauptText").childNodes[i].style.opacity = "1.0";
                        }
                    }
                }
            }
        }
    }
}

function showNewProposal() {
    hideText();
    setTimeout("showNewProposal_step()", 425);
}

function showNewProposal_step() {
    document.getElementById("inputText").style.display = "block";
    var opac = parseFloat(document.getElementById("inputText").style.opacity);
    document.getElementById("inputText").style.opacity = "" + (opac + 0.11);
    if (opac < 0.9) {
        setTimeout("showNewProposal_step()", 25);
    } else {
        document.getElementById("inputText").style.opacity = "1.0";
    }
}