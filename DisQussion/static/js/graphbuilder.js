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

function ChargeForce(mass, particles) {
    this.mass = mass;
    this.particles = particles;
}

ChargeForce.prototype.calcXY = function () {
    this.Fx = (Math.random() - 0.5) * 0.01;
    this.Fy = (Math.random() - 0.5) * 0.01;
    var dx;
    var dy;
    var lenMassParticle;
    var fullForce;
    var factorX;
    var factorY;
    for (var i = 0; i < this.particles.length; i++) {
        dx = this.mass.mass.x - this.particles[i].mass.x;
        dy = this.mass.mass.y - this.particles[i].mass.y;
        lenMassParticle = Math.sqrt(dx * dx + dy * dy);
        if (lenMassParticle == 0) {
            factorX = 1;
            factorY = 1;
        } else {
            factorX = dx / lenMassParticle;
            factorY = dy / lenMassParticle;
        }
        fullForce = 100 / (lenMassParticle + 20);
        this.Fx += fullForce * factorX;
        this.Fy += fullForce * factorY;
    }
}

function HorizontalForce(mass) {
    this.mass = mass;
}

HorizontalForce.prototype.calcXY = function () {
    this.Fx = 0;
    this.Fy = this.mass.mass.y * -0.015;
}

function step() {
    var masses = document.getElementById('graph').circles;
    var arrows = document.getElementById('graph').arrows;
    var i;
    for (i = 0; i < masses.length; i++) {
        // calculate new position
        masses[i].mass.setPosition(masses[i].mass.x + masses[i].mass.vx, masses[i].mass.y + masses[i].mass.vy);
        masses[i].style.left = Math.round(masses[i].mass.x - masses[i].style.width / 2) + "px";
        masses[i].style.top = Math.round(masses[i].mass.y - masses[i].style.height / 2) + "px";
        // calculate new velocity
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
    // adjust graph height
    var minHeight = 0;
    var maxHeight = 0;
    for (i = 0; i < masses.length; i++) {
        if (masses[i].mass.y < minHeight) {
            minHeight = masses[i].mass.y;
        }
        if (masses[i].mass.y > maxHeight) {
            maxHeight = masses[i].mass.y;
        }
    }
    document.getElementById('graph').style.height = Math.round(maxHeight) + "px";
    document.getElementById('graph').style.marginTop = Math.round(minHeight * -1 + 20) + "px";
    // draw arrows
    for (i = 0; i < arrows.length; i++) {
        drawArrow(arrows[i],masses[arrows[i].A],masses[arrows[i].B]);
    }
    // iterate
    setTimeout("step()", 25);
}

function drawArrow(arrowdiv, circleA, circleB) {
    var dx = circleA.mass.x - circleB.mass.x;
    var dy = circleA.mass.y - circleB.mass.y;
    var lenAB = Math.sqrt(dx * dx + dy * dy);
    // set length
    arrowdiv.firstChild.style.width = Math.round(lenAB)+"px";
    // set position
    arrowdiv.style.left = Math.round(circleA.mass.x)+"px";
    arrowdiv.style.top = Math.round(circleA.mass.y - arrowdiv.style.height / 2)+"px";
    // set rotation
    var alpha;
    if (dy > 0) {
        if (dx > 0) {
            alpha = Math.PI+Math.atan(Math.abs(dy) / Math.abs(dx));
        } else {
            if (dx < 0) {
                alpha = 2*Math.PI - Math.atan(Math.abs(dy) / Math.abs(dx));
            } else {
                alpha = Math.PI/2*3;
            }
        }
    } else {
        if (dx > 0) {
            alpha = Math.PI - Math.atan(Math.abs(dy) / Math.abs(dx));
        } else {
            if (dx < 0) {
                alpha = 2*Math.PI + Math.atan(Math.abs(dy) / Math.abs(dx));
            } else {
                alpha = Math.PI/2;
            }
        }
    }
    arrowdiv.style.webkitTransform = "rotate("+(alpha/Math.PI*180)+"deg)";
    arrowdiv.style.MozTransform = "rotate("+(alpha/Math.PI*180)+"deg)";
    arrowdiv.style.transform = "rotate("+(alpha/Math.PI*180)+"deg)";
}

function runSimulation() {
    var preGraph = document.getElementById('pregraph');
    for (i=0; i < preGraph.childNodes.length; i++) {
        if (graphNode.childNodes[i].nodeType == 1) {
            var b = "blubb";
        }
    }
    var graphNode = document.getElementById('graph');
    var circles = new Array();
    var arrows = new Array();
    var i;
    for (i = 0; i < graphNode.childNodes.length; i++) {
        var isCircle = false;
        var isArrow = false;
        if (graphNode.childNodes[i].attributes) {
            for (var j = 0; j < graphNode.childNodes[i].attributes.length; j++) {
                if ((graphNode.childNodes[i].attributes[j].nodeName == "class") &&
                    (graphNode.childNodes[i].attributes[j].nodeValue == "masspoint")) {
                    isCircle = true;
                }
                if ((graphNode.childNodes[i].attributes[j].nodeName == "class") &&
                    (graphNode.childNodes[i].attributes[j].nodeValue == "fixpoint")) {
                    isArrow = true;
                }
            }
        }
        if (isCircle) { circles.push(graphNode.childNodes[i]); }
        if (isArrow) { arrows.push(graphNode.childNodes[i]); }
    }
    for (i = 0; i < circles.length; i++) {
        circles[i].mass = new Mass();
    }
    //circles[0].mass.setPosition(-1, 0);
    //circles[1].mass.setPosition(1, 0);
    circles[0].forces = new Array(
        new SpringForce(circles[0], circles[4], 120.0),
        new ChargeForce(circles[0], new Array(circles[1], circles[2], circles[3], circles[4])),
        new HorizontalForce(circles[0]));
    circles[1].forces = new Array(
        new SpringForce(circles[1], circles[4], 120.0),
        new ChargeForce(circles[1], new Array(circles[0], circles[2], circles[3], circles[4])),
        new HorizontalForce(circles[1]));
    circles[2].forces = new Array(
        new SpringForce(circles[2], circles[1], 120.0),
        new ChargeForce(circles[2], new Array(circles[0], circles[1], circles[3], circles[4])),
        new HorizontalForce(circles[2]));
    circles[3].forces = new Array(
        new SpringForce(circles[3], circles[1], 120.0),
        new ChargeForce(circles[3], new Array(circles[0], circles[1], circles[2], circles[4])),
        new HorizontalForce(circles[3]));
    graphNode.circles = circles;
    arrows[0].A = "4";
    arrows[0].B = "0";
    arrows[1].A = "4";
    arrows[1].B = "1";
    arrows[2].A = "1";
    arrows[2].B = "2";
    arrows[3].A = "1";
    arrows[3].B = "3";
    graphNode.arrows = arrows;
    step();
}