function closelogin() {
    document.getElementById("login").style.opacity = "1.0";
    closelogin_step();
}

function closelogin_step() {
    var opac = parseFloat(document.getElementById("login").style.opacity);
    document.getElementById("login").style.opacity = "" + (opac - 0.1);
    document.getElementById("login_overlay").style.opacity = "" + ((opac - 0.1)*0.5);
    if (opac > 0) {
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
    document.getElementById("login").style.opacity = "" + (opac + 0.1);
    document.getElementById("login_overlay").style.opacity = "" + ((opac + 0.1)*0.5);
    if (opac < 0.9) {
        setTimeout("showlogin_step()", 25);
    }
}