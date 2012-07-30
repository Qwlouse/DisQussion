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
    document.getElementById("text").style.opacity = "1.0";
    hideText_step();
}

function hideText_step() {
    //alert(document.getElementById("hauptText").childNodes[1].style.opacity);
    var opac = parseFloat(document.getElementById("text").style.opacity);
    document.getElementById("text").style.opacity = "" + (opac - 0.11);
    if (opac >= 0.01) {
        setTimeout("hideText_step()", 20);
    } else {
        document.getElementById("text").childNodes[i].style.display = "none";
    }
}

function showText(sourceNode) {
    document.getElementById("text").textSource = sourceNode;
    hideText();
    setTimeout("showText_intermission()", 425);
}

function showText_intermission() {
    if (document.getElementById("text").waitForText) {
        setTimeout("showText_intermission()", 25);
    } else {
        document.getElementById("text").innerHTML = document.getElementById("text").textSource.textPart;
        showText_step();
    }
}

function showText_step() {
    document.getElementById("text").style.display = "block";
    var opac = parseFloat(document.getElementById("text").style.opacity);
    document.getElementById("text").style.opacity = "" + (opac + 0.11);
    if (opac < 0.9) {
        setTimeout("showText_step()", 25);
    } else {
        document.getElementById("text").style.opacity = "1.0";
    }
}

function fadeOutElement() {
    var node = document.body.elementToHide;
    node.style.display = "block";
    var opacity = parseFloat(node.style.opacity);
    if (opacity > 0.1) {
        node.style.opacity = "" + (opacity - 0.11);
        setTimeout("fadeOutElement()", 25);
    } else {
        node.style.opacity = "0.0";
        node.style.display = "none";
    }
}

function fadeInElement() {
    var node = document.body.elementToShow;
    node.style.display = "block";
    var opacity = parseFloat(node.style.opacity);
    if (opacity < 0.9) {
        node.style.opacity = "" + (opacity + 0.11);
        setTimeout("fadeInElement()", 25);
    } else {
        node.style.opacity = "1.0";
    }
}

function showNextNode(node) {
    //alert("STUB!"+node);
    document.body.elementToHide = node.parentNode;
    document.body.elementToHide.style.opacity = 1.0;
    fadeOutElement();
    document.body.elementToShow = node.parentNode.nextSibling.nextSibling;
    document.body.elementToShow.style.opacity = 0.0;
    setTimeout("fadeInElement()", 300);
}