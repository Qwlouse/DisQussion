/////////////////////// Graph Construction /////////////////////////////////
function createCircleStructure(title, id, type, consent) {
    var newText = document.createTextNode(title);
    var linkDIV = document.createElement("div");
    linkDIV.appendChild(newText);
    linkDIV.setAttribute("class", "linklike");
    var innerDIV = document.createElement("div");
    innerDIV.appendChild(linkDIV);
    innerDIV.setAttribute("class", "circle");
    innerDIV.setAttribute("onClick", "showNode(this.parentNode, true);");
    var outerDIV = document.createElement("div");
    outerDIV.setAttribute("class", "masspoint");
    var diagramDIV = document.createElement("div");
    diagramDIV.setAttribute("class", "diagram_container");
    var whiteContainerDIV = document.createElement("div");
    var whitenerDIV = document.createElement("div");
    whitenerDIV.setAttribute("class", "whitener");
    whiteContainerDIV.appendChild(whitenerDIV);
    whiteContainerDIV.setAttribute("style", "width: 0; height: 0; overflow: visible;")
    outerDIV.appendChild(whiteContainerDIV);
    outerDIV.appendChild(diagramDIV);
    outerDIV.appendChild(innerDIV);
    outerDIV.particle = new Particle();
    outerDIV.particle.targetY = 0.0;
    //outerDIV.setAttribute("id", "circle_"+title.replace(/^\s+|\s+$/g, ''));
    outerDIV.dbId = id;
    outerDIV.type = type;

    var data = [consent, 1.0-consent];

    var r = 40,
        h = 2*r,
        w = 2*r,
        color = ["#00ff00","#ff0000", "#0000ff"],
        donut = d3.layout.pie().sort(null),
        arc = d3.svg.arc().innerRadius(r - 20).outerRadius(r - 10);

    var svg = d3.select(diagramDIV).append("svg:svg")
        .attr("width", w)
        .attr("height", h)
        .attr("transform", "translate(-100, -50)")
        .append("svg:g")
        .attr("transform", "translate(" + w / 2 + "," + h / 2 + ")");

    var arcs = svg.selectAll("path")
        .data(donut(data))
        .enter().append("svg:path")
        .attr("fill", function(d, i) { return color[i]; })
        .attr("d", arc)
        .each(function(d) { this._current = d; });
    //d3.select(svg).attr("transform", "translate(200,0)");

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


function buildGraph(node_id, node_title, node_type) {
    var graphNode = document.getElementById('graph');
    graphNode.stepRuns = false;
    graphNode.centerCircle = createCircleStructure(node_title, node_id, node_type);
    graphNode.appendChild(graphNode.centerCircle);
    graphNode.circles = new Array(graphNode.centerCircle);
    graphNode.arrows = new Array();
    showNode(graphNode.centerCircle, true);
    //Dajaxice.structure.getNodeInfo(amendGraph, {'node_id' : node_id, 'node_type' : node_type});
    // TODO: setTimeout("showText(graphNode.circles[1])", 500);
}


function initPage(anchorGraphData, navigationData, selected_id, doNodeUpdate) {
    document.getElementById('graph').paddingTop = 30.0;
    document.getElementById('graph').paddingLeft = 30.0;
    document.getElementById('graph').paddingRight = 30.0;
    document.getElementById('graph').paddingBottom = 30.0;
    updateNavigation(JSON.parse(navigationData));
    buildAnchorGraph(JSON.parse(anchorGraphData));
    // get selected Node:
    var graphNode = document.getElementById('graph');
    for (var i = 0; i < graphNode.circles.length; ++i) {
        var node = graphNode.circles[i];
        if ((node.dbId == selected_id) && node.type != "Slot") {
            showNode(node, doNodeUpdate);
            break;
        }
    }
}


function buildAnchorGraph(data) {
    var Anchors = data["Anchors"];
    var graphNode = document.getElementById('graph');
    graphNode.stepRuns = false;
    while ( graphNode.firstChild ) graphNode.removeChild( graphNode.firstChild );
    graphNode.circles = new Array();
    graphNode.arrows = new Array();

    for (var i = 0; i < Anchors.length; ++i) {
        var anchor = Anchors[i];
        var anchor_circle = createCircleStructure(anchor['nr_in_parent'], anchor['id'], anchor['type'], anchor['consent']);
        anchor_circle.particle.x = i*80;
        anchor_circle.particle.targetX = i*80;
        anchor_circle.particle.targetForce = 0.05;
        graphNode.circles.push(anchor_circle);
        graphNode.appendChild(anchor_circle);
    }

    // add related nodes
    var relatedNodes = data['related_nodes'];
    for (i = 0; i < relatedNodes.length; ++i) {
        var node = relatedNodes[i];
        var node_circle = createCircleStructure(node['nr_in_parent'], node['id'], node['type'], anchor['consent']);
        node_circle.particle.y = -160;
        node_circle.particle.x = i*80;
        graphNode.circles.push(node_circle);
        graphNode.appendChild(node_circle);
    }

    // add connections
    var connections = data['connections'];
    for (i = 0; i < connections.length; ++i) {
        var connection = connections[i];
        var source_node = getNodeById(graphNode.circles, connection[0], "TextNode");
        var target_node = getNodeById(graphNode.circles, connection[1], "TextNode");
        var arrow = createArrowStructure(source_node, target_node);
        graphNode.arrows.push(arrow);
        graphNode.insertBefore(arrow, graphNode.firstChild);
    }
    if (!(graphNode.stepRuns)) {
        graphNode.stepRuns = true;
        step();
    }
}


/////////////////////// Simulation /////////////////////////////////
function step() {
    var graphNode = document.getElementById('graph');
    var circles = graphNode.circles;
    var arrows = graphNode.arrows;
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

    // adjust graph dimensions
    var minPosY = 0;
    var maxPosY = 0;
    var minPosX = 0;
    var maxPosX = 0;
    for (i = 0; i < particles.length; i++) {
        minPosY = Math.min(particles[i].y, minPosY);
        maxPosY = Math.max(particles[i].y, maxPosY);
        minPosX = Math.min(particles[i].x - 30, minPosX);
        maxPosX = Math.max(particles[i].x - 30, maxPosX);
    }
    var paddingRight = Math.max(maxPosX + 36, graphNode.paddingRight - 1);
    graphNode.paddingRight = paddingRight;
    var paddingBottom = Math.max(maxPosY + 36, graphNode.paddingBottom - 1);
    graphNode.paddingBottom = paddingBottom;
    var paddingTop = Math.max(minPosY * -1 + 31, graphNode.paddingTop - 1);
    graphNode.paddingTop = paddingTop;
    var paddingLeft = Math.max(minPosX * -1 + 31, graphNode.paddingLeft - 1);
    //var paddingLeft = Math.max(minPosX * -1, 0);
    graphNode.paddingLeft = paddingLeft;
    graphNode.style.paddingRight = Math.round(paddingRight) + "px";
    graphNode.style.paddingBottom = Math.round(paddingBottom) + "px";
    graphNode.style.paddingTop = Math.round(paddingTop) + "px";
    graphNode.style.paddingLeft = Math.round(paddingLeft) + "px";
    //graphNode.style.width = Math.round(paddingRight+paddingLeft) + "px";
    //graphNode.style.height = Math.round(paddingTop+paddingBottom) + "px";
    // iterate
    if (particleMovement > 0.2) {
        setTimeout("step()", 25);
    } else {
        document.getElementById('graph').stepRuns = false;
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

function getNodeById(circles, id, type) {
    for (var i = 0; i < circles.length; i++) {
        if ((circles[i].dbId == id) && (circles[i].type == type)) return circles[i];
    }
    return -1;
}