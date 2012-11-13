function DarthFader(id, fade_in_callback, fade_out_callback, target) {
    target = target ? target : 100;
    var delay = 20;
    var fader = {
        fade_in:function () {
            this.elem = document.getElementById(id);
            this.alpha = this.elem.style.opacity ? parseFloat(this.elem.style.opacity) * 100 : 0;
            clearInterval(this.si);
            this.target = target;
            this.step = 1;
            this.callback = fade_in_callback;
            this.si = setInterval(function(){fader.tween()}, delay);
        },
        fade_out:function () {
            this.elem = document.getElementById(id);
            this.alpha = this.elem.style.opacity ? parseFloat(this.elem.style.opacity) * 100 : 0;
            clearInterval(this.si);
            this.target = 0;
            this.step = -1;
            this.callback = fade_out_callback;
            this.si = setInterval(function(){fader.tween()}, delay);
        },

        tween:function () {
            if (this.alpha == this.target) {
                clearInterval(this.si);
                if (this.callback) this.callback();
            } else {
                var value = Math.round(this.alpha + ((this.target - this.alpha) * .1)) + this.step;
                this.elem.style.opacity = value / 100;
                this.elem.style.filter = 'alpha(opacity=' + value + ')';
                this.alpha = value
            }
        }
    };

    return fader;
}

var login_fader = DarthFader("login",
    function(){},
    function() {
        document.getElementById("login").style.display = "none";
    });

var login_overlay_fader = DarthFader("login_overlay",
    function(){},
    function() {
        document.getElementById("login_overlay").style.display = "none";
    },
    50
);

function closelogin() {
    login_fader.fade_out();
    login_overlay_fader.fade_out();
}

function showlogin() {
    document.getElementById("login").style.display = "block";
    document.getElementById("login_overlay").style.display = "block";
    login_fader.fade_in();
    login_overlay_fader.fade_out();

}

function closepostfield() {
    document.getElementById("post_field").style.opacity = "1.0";
    closepostfield_step();
}

function closepostfield_step() {
    var opac = parseFloat(document.getElementById("post_field").style.opacity);
    document.getElementById("post_field").style.opacity = "" + (opac - 0.11);
    document.getElementById("post_field_overlay").style.opacity = "" + ((opac - 0.11)*0.5);
    if (opac >= 0.01) {
        setTimeout("closepostfield_step()", 25);
    } else {
        document.getElementById("post_field_overlay").style.display = "none";
        document.getElementById("post_field").style.display = "none";
    }
}

function showResponse(username) {
    document.getElementById("post_field_textarea").innerHTML = "@"+username+" ";
    showpostfield();
}

function showTwoResponses(username1, username2) {
    document.getElementById("post_field_textarea").innerHTML = "@"+username1+" @"+username2+" ";
    showpostfield();
}

function showEmptyPostField() {
    document.getElementById("post_field_textarea").innerHTML = "";
    showpostfield();
}

function showpostfield() {
    document.getElementById("post_field").style.display = "block";
    document.getElementById("post_field_overlay").style.display = "block";
    document.getElementById("post_field").style.opacity = "0.0";
    showpostfield_step();
}

function showpostfield_step() {
    var opac = parseFloat(document.getElementById("post_field").style.opacity);
    document.getElementById("post_field").style.opacity = "" + (opac + 0.11);
    document.getElementById("post_field_overlay").style.opacity = "" + ((opac + 0.11)*0.5);
    if (opac < 0.9) {
        setTimeout("showpostfield_step()", 25);
    } else {
        document.getElementById("post_field").style.opacity = "1.0";
        document.getElementById("post_field_overlay").style.opacity = "0.5";
    }
}

function hideText() {
    document.getElementById("text").waitForHiding = true;
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
        document.getElementById("text").waitForHiding = false;
    }
}

function showText(sourceNode) {
    document.getElementById("text").textSource = sourceNode;
    hideText();
    setTimeout("showText_intermission()", 425);
}

function showText_intermission() {
    if (document.getElementById("text").waitForText || document.getElementById("text").waitForHiding) {
        setTimeout("showText_intermission()", 25);
    } else {
        document.getElementById("text").innerHTML = document.getElementById("text").textSource.textPart;
        updateVoting(document.getElementById("text").textSource.votingInfo);
        Hyphenator.run();
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