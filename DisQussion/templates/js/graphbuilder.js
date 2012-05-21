function Mass() {
    this.x = 0.0;
    this.y = 0.0;
    this.vx = 0.0;
    this.vy = 0.0;
}

Mass.prototype.setPosition = function (newX, newY) {
    this.x = newX;
    this.y = newY;
};

Mass.prototype.setVelocity = function (newX, newY) {
    this.vx = newX;
    this.vy = newY;
};

function SpringForce(mass1, mass2, len) {
    this.massA = mass1;
    this.massB = mass2;
    this.len = len;
    this.k = 0.03;
}

SpringForce.prototype.calcXY = function () {
    var dx = this.massA.mass.x - this.massB.mass.x;
    var dy = this.massA.mass.y - this.massB.mass.y;
    var lenAB = Math.sqrt(dx * dx + dy * dy);
    var factorX;
    var factorY;
    if (lenAB == 0) {
        factorX = 1;
        factorY = 1;
    } else {
        factorX = dx / lenAB;
        factorY = dy / lenAB;
    }
    this.Fx = this.k * (this.len - lenAB) * factorX;
    this.Fy = this.k * (this.len - lenAB) * factorY;
};

function step() {
    var masses = document.getElementById('graph').circles;
    for (var i = 0; i < masses.length; i++) {
        // neue Position berechnen
        masses[i].mass.setPosition(masses[i].mass.x + masses[i].mass.vx, masses[i].mass.y + masses[i].mass.vy);
        masses[i].style.left = Math.round(masses[i].mass.x) + "px";
        masses[i].style.top = Math.round(masses[i].mass.y) + "px";
        // neue Geschwindigkeit berechnen
        var ax = 0;
        var ay = 0;
        if (masses[i].forces) {
            for (var j = 0; j < masses[i].forces.length; j++) {
                masses[i].forces[j].calcXY();
                ax += masses[i].forces[j].Fx;
                ay += masses[i].forces[j].Fy;
            }
        }
        masses[i].mass.setVelocity(masses[i].mass.vx * 0.7 + ax, masses[i].mass.vy * 0.7 + ay);
    }
    //alert((masses[0].mass.vx) + " " + (masses[1].mass.vx) + " " + (masses[2].mass.vx));
    setTimeout("step()", 25);
}

function runSimulation() {
    var graphNode = document.getElementById('graph');
    var circles = new Array();
    var i;
    for (i = 0; i < graphNode.childNodes.length; i++) {
        var isCircle = false;
        if (graphNode.childNodes[i].attributes) {
            for (var j = 0; j < graphNode.childNodes[i].attributes.length; j++) {
                if ((graphNode.childNodes[i].attributes[j].nodeName == "class") &&
                    (graphNode.childNodes[i].attributes[j].nodeValue == "masspoint")) {
                    isCircle = true;
                }
            }
        }
        if (isCircle) {
            circles.push(graphNode.childNodes[i]);
        }
    }
    for (i = 0; i < circles.length; i++) {
        circles[i].mass = new Mass();
    }
    circles[0].mass.setPosition(-1, 0);
    circles[1].mass.setPosition(1, 0);
    circles[0].forces = new Array(new SpringForce(circles[0], circles[2], 120.0));
    circles[1].forces = new Array(new SpringForce(circles[1], circles[2], 120.0));
    graphNode.circles = circles;
    step();
}