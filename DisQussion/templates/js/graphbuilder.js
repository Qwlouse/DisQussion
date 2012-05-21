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
    this.Fx = (Math.random()-0.5)*0.01;
    this.Fy = (Math.random()-0.5)*0.01;
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
        fullForce = 100 / (lenMassParticle+20);
        this.Fx += fullForce * factorX;
        this.Fy += fullForce * factorY;
    }
}

function HorizontalForce(mass) {
    this.mass = mass;
}

HorizontalForce.prototype.calcXY = function () {
    this.Fx = 0;
    this.Fy = this.mass.mass.y*-0.015;
}

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
    //circles[0].mass.setPosition(-1, 0);
    //circles[1].mass.setPosition(1, 0);
    circles[0].forces = new Array(
        new SpringForce(circles[0], circles[4], 120.0),
        new ChargeForce(circles[0],new Array(circles[1],circles[2],circles[3],circles[4])),
        new HorizontalForce(circles[0]));
    circles[1].forces = new Array(
        new SpringForce(circles[1], circles[4], 120.0),
        new ChargeForce(circles[1],new Array(circles[0],circles[2],circles[3],circles[4])),
        new HorizontalForce(circles[1]));
    circles[2].forces = new Array(
        new SpringForce(circles[2], circles[1], 120.0),
        new ChargeForce(circles[2],new Array(circles[0],circles[1],circles[3],circles[4])),
        new HorizontalForce(circles[2]));
    circles[3].forces = new Array(
        new SpringForce(circles[3], circles[1], 120.0),
        new ChargeForce(circles[3],new Array(circles[0],circles[1],circles[2],circles[4])),
        new HorizontalForce(circles[3]));
    graphNode.circles = circles;
    step();
}