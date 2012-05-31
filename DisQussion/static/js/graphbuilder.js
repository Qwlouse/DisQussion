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

SpringForce.prototype.setLen = function (newLen) {
    this.len = newLen;
};

SpringForce.prototype.getB = function () {
    return this.massB;
};

SpringForce.prototype.forceType = function () {
    return 1;
};

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

ChargeForce.prototype.forceType = function () {
    return 2;
};

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
        //this.Fx += Math.atan(fullForce / 300) * 500 * factorX;
        //this.Fy += Math.atan(fullForce / 300) * 500 * factorY;
        this.Fx += fullForce * factorX;
        this.Fy += fullForce * factorY;
    }
};

function HorizontalForce(mass) {
    this.mass = mass;
}

HorizontalForce.prototype.forceType = function () {
    return 3;
};

HorizontalForce.prototype.calcXY = function () {
    this.Fx = 0;
    this.Fy = this.mass.mass.y * -0.015;
};

function step() {
    var masses = document.getElementById('graph').circles;
    var arrows = document.getElementById('graph').arrows;
    //alert("We have "+masses.length+" masses and "+arrows.length+" arrows.")
    var i;
    var sum_v = 0;
    for (i = 0; i < masses.length; i++) {
        // calculate new position
        masses[i].mass.setPosition(masses[i].mass.x + masses[i].mass.vx, masses[i].mass.y + masses[i].mass.vy);
        masses[i].style.left = Math.round(masses[i].mass.x - masses[i].style.width / 2 - 30) + "px";
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
        sum_v += Math.abs(masses[i].mass.vx) + Math.abs(masses[i].mass.vy);
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
    if (sum_v > 0.2) {
        setTimeout("step()", 25);
    }
}

function drawArrow(arrowdiv, circleA, circleB) {
    var dx = circleA.mass.x - circleB.mass.x;
    var dy = circleA.mass.y - circleB.mass.y;
    var lenAB = Math.sqrt(dx * dx + dy * dy);
    // set length
    arrowdiv.firstChild.style.width = Math.round(lenAB)+"px";
    // set position
    arrowdiv.style.left = Math.round(circleA.mass.x - 30)+"px";
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
    var rawGraph = document.getElementById('rawgraph');
    var graphNode = document.getElementById('graph');
    var i;
    var rootDIV = document.createElement("div");
    rootDIV.setAttribute("class", "masspoint");
    rootDIV.mass = new Mass();
    graphNode.appendChild(rootDIV);
    var circles = new Array(rootDIV);
    var arrows = new Array();
    var nodeCount = 0;
    for (i = 0; i < rawGraph.childNodes.length; i++) {
        if (rawGraph.childNodes[i].nodeType == 1) {
            nodeCount++;
            var newText = document.createTextNode(rawGraph.childNodes[i].firstChild.data);
            var linkDIV = document.createElement("div");
            linkDIV.appendChild(newText);
            if (nodeCount > 1) {
                linkDIV.setAttribute("class", "linklike");
            }
            linkDIV.setAttribute("onClick", "showslot(this.parentNode.parentNode);");
            var innerDIV = document.createElement("div");
            innerDIV.appendChild(linkDIV);
            innerDIV.setAttribute("class", "circle");
            innerDIV.setAttribute("onClick", "showslot(this.parentNode);");
            var outerDIV = document.createElement("div");
            outerDIV.setAttribute("class", "masspoint");
            outerDIV.appendChild(innerDIV);
            outerDIV.mass = new Mass();
            if (nodeCount == 1) {
                outerDIV.forces = new Array(
                    new SpringForce(outerDIV, rootDIV, 0.0),
                    new HorizontalForce(outerDIV));
            }
            if (nodeCount > 1) {
                outerDIV.forces = new Array(
                    new SpringForce(outerDIV, circles[1], 120.0),
                    new HorizontalForce(outerDIV));
            }
            circles.push(outerDIV);
            graphNode.appendChild(outerDIV);
            if (nodeCount > 1) {
                var innerArrow = document.createElement("div");
                innerArrow.setAttribute("class", "arrow");
                var outerArrow = document.createElement("div");
                outerArrow.setAttribute("class", "fixpoint");
                outerArrow.appendChild(innerArrow);
                outerArrow.A = ""+1;
                outerArrow.B = ""+(circles.length-1);
                arrows.push(outerArrow);
                graphNode.insertBefore(outerArrow, graphNode.firstChild);
            }
        }
    }
    for (i = 1; i < circles.length; i++) {
        var a = new Array();
        for (var j = 1; j < circles.length; j++) {
            if (j != i) {
                a.push(circles[j]);
            }
            if (circles[j].forces[0].getB() == circles[i]) {
                circles[i].forces.push(new SpringForce(circles[i],circles[j], 120.0));
            }
        }
        circles[i].forces.push(new ChargeForce(circles[i], a));
    }
    graphNode.circles = circles;
    graphNode.arrows = arrows;
    rawGraph.style.display = "none";
    step();
}

function showslot(slotNode) {
    var graphNode = document.getElementById('graph');
    for (var i = 1; i < graphNode.circles.length; i++) {
        graphNode.circles[i].forces[0].setLen(120.0);
        graphNode.circles[i].firstChild.firstChild.setAttribute("class", "linklike");
        if (graphNode.circles[i].forces[(graphNode.circles[i].forces.length - 1)].forceType() == 1) {
            graphNode.circles[i].forces.pop();
        }
    }
    slotNode.forces.push(new SpringForce(slotNode, graphNode.circles[0], 0.0));
    for (i = 0; i < slotNode.firstChild.firstChild.attributes.length; i++){
        if (slotNode.firstChild.firstChild.attributes[i].name == "class"){
            slotNode.firstChild.firstChild.attributes[i].value = "";
        }
    }
    step();
}