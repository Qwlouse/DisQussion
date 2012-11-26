function DarthFader(id, fade_in_callback, fade_out_callback, target) {
    target = target ? target : 100;
    fade_in_callback = fade_in_callback ? fade_in_callback : function(){};
    fade_out_callback = fade_out_callback ? fade_out_callback : function(){};
    var delay = 25;
    var stepsize = 1;
    var rel_stepsize = 0.2;
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
                this.callback();
            } else {
                var value = Math.round(this.alpha + ((this.target - this.alpha) * rel_stepsize)) + this.step * stepsize;
                this.elem.style.opacity = value / 100;
                this.elem.style.filter = 'alpha(opacity=' + value + ')';
                this.alpha = value
            }
        }
    };

    return fader;
}

var login_fader = DarthFader("login",
    false,
    function() {
        document.getElementById("login").style.display = "none";
    });

var login_overlay_fader = DarthFader("login_overlay",
    false,
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
    login_overlay_fader.fade_in();
}

var post_field_fader = DarthFader("post_field",
    false,
    function() {
        document.getElementById("post_field").style.display = "none";
    }
);

var post_field_overlay_fader = DarthFader("post_field_overlay",
    false,
    function() {
        document.getElementById("post_field_overlay").style.display = "none";
    },
    50
);

function closepostfield() {
    post_field_fader.fade_out();
    post_field_overlay_fader.fade_out();
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
    post_field_fader.fade_in();
    post_field_overlay_fader.fade_in();
}

var text_fader = DarthFader("text",
    function(){},
    function() {
        document.getElementById("text").waitForHiding = false;
        showText_intermission();
    }
);

function showText(sourceNode) {
    document.getElementById("text").textSource = sourceNode;
    document.getElementById("text").waitForHiding = true;
    text_fader.fade_out();
    var gif = document.createElement("div");
    gif.setAttribute("class","busy_gif");
    var gif_container = document.createElement("div");
    gif_container.appendChild(gif);
    gif_container.style.height = "0px";
    gif_container.style.overflow = "visible";
    gif_container.style.position = "relative";
    gif_container.style.top = "-50px";
    document.getElementById("floatblock").insertBefore(gif_container,document.getElementById("floatblock").firstChild);
}

function showText_intermission() {
    if (document.getElementById("text").waitForText || document.getElementById("text").waitForHiding) {
        setTimeout("showText_intermission()", 25);
    } else {
        document.getElementById("text").innerHTML = document.getElementById("text").textSource.textPart;
        updateVoting(document.getElementById("text").textSource.votingInfo);
        document.getElementById("floatblock").removeChild(document.getElementById("floatblock").firstChild);
        text_fader.fade_in();
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