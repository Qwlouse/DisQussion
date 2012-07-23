/////////////////////// Graph Construction /////////////////////////////////
function createCircleStructure(title, id, type) {
    var newText = document.createTextNode(title);
    var linkDIV = document.createElement("div");
    linkDIV.appendChild(newText);
    linkDIV.setAttribute("class", "linklike");
    //linkDIV.setAttribute("onClick", "showslot(this.parentNode.parentNode);");
    var innerDIV = document.createElement("div");
    innerDIV.appendChild(linkDIV);
    innerDIV.setAttribute("class", "circle");
    innerDIV.setAttribute("onClick", "showNode(this.parentNode);");
    var outerDIV = document.createElement("div");
    outerDIV.setAttribute("class", "masspoint");
    outerDIV.appendChild(innerDIV);
    outerDIV.particle = new Particle();
    outerDIV.particle.targetY = 0.0;
    //outerDIV.setAttribute("id", "circle_"+title.replace(/^\s+|\s+$/g, ''));
    outerDIV.dbId = id;
    outerDIV.type = type;
    return outerDIV;
}


function createArrowStructure(parentCircle, childCircle) {
    var innerArrow = document.createElement("div");
    innerArrow.setAttribute("class", "arrow");
    var outerArrow = document.createElement("div");
    outerArrow.setAttribute("class", "fixpoint");
    outerArrow.appendChild(innerArrow);
    outerArrow.spring = new Spring(parentCircle.particle, childCircle.particle, 80.0);
    outerArrow.A = parentCircle;
    outerArrow.B = childCircle;
    return outerArrow
}


function buildGraph(node_id, title) {
    var graphNode = document.getElementById('graph');
    graphNode.centerCircle = createCircleStructure(title, node_id, "StructureNode");
    graphNode.circles = new Array(graphNode.centerCircle);
    document.getElementById('graph').appendChild(graphNode.centerCircle);
    graphNode.arrows = new Array();
    Dajaxice.structure.getNodeInfo(amendGraph, {'node_id' : node_id, 'node_type' : 'StructureNode'});
    // TODO: setTimeout("showText(graphNode.circles[1])", 500);
}


function amendGraph(data) {
    var graphNode = document.getElementById('graph');
    var circles = graphNode.circles;
    var arrows = graphNode.arrows;
    var currentIndex = getIndexInCircles(circles, data['id'], data['type']);
    var parent = circles[currentIndex];
    // set text
    document.getElementById("text").innerHTML = data['text'];
    showText_step();
    // add new nodes + arrows
    for (var i = 0; i < data['children'].length; i++) {
        var child_data = data['children'][i];
        var childIndex = getIndexInCircles(circles, child_data['id'], child_data['type']);
        if (childIndex == -1) {
            var child = createCircleStructure(child_data['short_title'], child_data['id'], child_data['type']);
            circles.push(child);
            document.getElementById('graph').appendChild(child);
            var arrow = createArrowStructure(parent, child);
            arrows.push(arrow);
            graphNode.insertBefore(arrow, graphNode.firstChild);
        }
    }
    graphNode.circles = circles;
    graphNode.arrows = arrows;
    step(); //TODO: Check if step is running

}


/////////////////////// Simulation /////////////////////////////////
function step() {

    var circles = document.getElementById('graph').circles;
    var arrows = document.getElementById('graph').arrows;
    var particles = new Array();
    for (var i = 0; i < circles.length; ++i)
        particles.push(circles[i].particle);
    var springs = new Array();
    for (i = 0; i < arrows.length; ++i)
        springs.push(arrows[i].spring);
    var particleMovement = updateParticles(particles, springs);

    // set new position
    for (i = 0; i < circles.length; ++i) {
        circles[i].style.left = Math.round(particles[i].x - circles[i].style.width / 2 - 30) + "px";
        circles[i].style.top = Math.round(particles[i].y - circles[i].style.height / 2) + "px";
    }
    // draw arrows
    for (i = 0; i < arrows.length; i++) {
        drawArrow(arrows[i]);
    }

    // adjust graph height
    var minHeight = 0;
    var maxHeight = 0;
    for (i = 0; i < particles.length; i++) {
        minHeight = Math.min(particles[i].y, minHeight);
        maxHeight = Math.max(particles[i].y, maxHeight);
    }
    document.getElementById('graph').style.height = Math.round(maxHeight) + "px";
    document.getElementById('graph').style.marginTop = Math.round(minHeight * -1 + 20) + "px";

    // iterate
    if (particleMovement > 0.2) {
        setTimeout("step()", 25);
    }
}


/////////////////////// Drawing /////////////////////////////////
function drawArrow(arrowdiv) {
    var particleA = arrowdiv.A.particle;
    var particleB = arrowdiv.B.particle;
    var dx = particleA.x - particleB.x;
    var dy = particleA.y - particleB.y;
    var lenAB = Math.sqrt(dx * dx + dy * dy);
    // set length
    arrowdiv.firstChild.style.width = Math.round(lenAB)+"px";
    // set position
    arrowdiv.style.left = Math.round(particleA.x - 30)+"px";
    arrowdiv.style.top = Math.round(particleA.y - arrowdiv.style.height / 2)+"px";
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
    arrowdiv.style.msTransform = "rotate("+(alpha/Math.PI*180)+"deg)";
    arrowdiv.style.OTransform = "rotate("+(alpha/Math.PI*180)+"deg)";
    arrowdiv.style.MozTransform = "rotate("+(alpha/Math.PI*180)+"deg)";
    arrowdiv.style.transform = "rotate("+(alpha/Math.PI*180)+"deg)";
}


/////////////////////// Helpers ///////////////////////////////////////////////////
function getIndexInCircles(circles, id, type) {
    for (var i = 0; i < circles.length; i++) {
        if ((circles[i].dbId == id) && (circles[i].type == type)) return i;
    }
    return -1;
}
