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
    //create arrow svg
    var svgDocument = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svgDocument.setAttribute("version", "1.2");
    svgDocument.setAttribute("width", "10");
    svgDocument.setAttribute("height", "10");
    var defsTag = document.createElementNS("http://www.w3.org/2000/svg", "defs");
    var marker = document.createElementNS("http://www.w3.org/2000/svg", "marker");
    marker.setAttribute("refX", "13");
    marker.setAttribute("refY", "0");
    marker.setAttribute("id", "arrow");
    marker.setAttribute("orient", "auto");
    marker.setAttribute("style", "overflow:visible;");
    var markerPath = document.createElementNS("http://www.w3.org/2000/svg", "path");
    markerPath.setAttribute("d", "M -1,-3 7,0 -1,3 0,0 z");
    markerPath.setAttribute("fill", "black");
    markerPath.setAttribute("transform", "scale(0.5)");
    marker.appendChild(markerPath);
    defsTag.appendChild(marker);
    svgDocument.appendChild(defsTag);
    var arrowLine = document.createElementNS("http://www.w3.org/2000/svg", "line");
    arrowLine.setAttribute("x1", "0");
    arrowLine.setAttribute("y1", "0");
    arrowLine.setAttribute("x2", "10");
    arrowLine.setAttribute("y2", "0");
    arrowLine.setAttribute("stroke", "black");
    arrowLine.setAttribute("stroke-width", "3");
    arrowLine.setAttribute("style", "marker-end:url(#arrow)");
    svgDocument.appendChild(arrowLine);
    //create container
    var outerArrow = document.createElement("div");
    outerArrow.setAttribute("class", "fixpoint");
    outerArrow.appendChild(svgDocument);
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
    if (document.getElementById('graph')) {
        document.getElementById('graph').paddingTop = 30.0;
        document.getElementById('graph').paddingLeft = 30.0;
        document.getElementById('graph').paddingRight = 30.0;
        document.getElementById('graph').paddingBottom = 30.0;
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
    updateNavigation(JSON.parse(navigationData));
    Hyphenator.config({useCSS3hyphenation: true, minwordlength : 4, defaultlanguage: 'de', displaytogglebox: false});
    Hyphenator.run();
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

function updateGraph(data) {
    var graphNode = document.getElementById('graph');
    var Anchors = data["graph_data"]["Anchors"];
    // draw voting
    updateVoting(data["voting_data"]);

    //alert("0");
    var newCircles = new Array();
    for (var i = 0; i < Anchors.length; ++i) {
        var anchor = Anchors[i];
        var old_circle = getNodeById(graphNode.circles, anchor['id'], anchor['type']);
        var anchor_circle = createCircleStructure(anchor['nr_in_parent'], anchor['id'], anchor['type'], anchor['consent']);
        anchor_circle.particle.x = i*80;
        if (old_circle != -1) {
            anchor_circle.particle.x = old_circle.particle.x;
            anchor_circle.particle.y = old_circle.particle.y;
        }
        anchor_circle.particle.targetX = i*80;
        anchor_circle.particle.targetForce = 0.05;
        newCircles.push(anchor_circle);
    }
    alert("1");

    // add related nodes
    var relatedNodes = data["graph_data"]['related_nodes'];
    for (i = 0; i < relatedNodes.length; ++i) {
        var node = relatedNodes[i];
        var node_circle = createCircleStructure(node['nr_in_parent'], node['id'], node['type'], anchor['consent']);
        node_circle.particle.y = -160;
        node_circle.particle.x = i*80;
        old_circle = getNodeById(graphNode.circles, node['id'], node['type']);
        if (old_circle != -1) {
            node_circle.particle.x = old_circle.particle.x;
            node_circle.particle.y = old_circle.particle.y;
        }
        newCircles.push(node_circle);
    }
    // clear graphNode and (re-)insert nodes
    while ( graphNode.firstChild ) graphNode.removeChild( graphNode.firstChild );
    graphNode.circles = newCircles;
    for (i = 0; i < newCircles.length; ++i) {
        graphNode.appendChild(newCircles[i]);
    }
    alert("2");

    // add connections
    var connections = data["graph_data"]['connections'];
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
    var svg = arrowdiv.firstChild;
    var arrowLine = svg.firstChild.nextSibling;
    var particleA = arrowdiv.A.particle;
    var particleB = arrowdiv.B.particle;
    svg.setAttribute("width", Math.max(Math.round(Math.abs(particleB.x-particleA.x))+10,10));
    svg.setAttribute("height", Math.max(Math.round(Math.abs(particleB.y-particleA.y))+10,10));
    if (particleB.x - particleA.x < 0) {
        arrowLine.setAttribute("x2", "5");
        arrowLine.setAttribute("x1", particleA.x-particleB.x+5);
        //alert(arrowdiv.style.width);
        arrowdiv.style.left = Math.round(particleA.x - 28)+Math.round(particleB.x - particleA.x)-5+"px";
    } else {
        arrowLine.setAttribute("x1", "5");
        arrowLine.setAttribute("x2", particleB.x-particleA.x+5);
        arrowdiv.style.left = Math.round(particleA.x - 28 - 5)+"px";
    }
    if (particleB.y - particleA.y < 0) {
        arrowLine.setAttribute("y2", "5");
        arrowLine.setAttribute("y1", particleA.y-particleB.y+5);
        arrowdiv.style.top = Math.round(particleA.y - arrowdiv.style.height / 2)+Math.round(particleB.y - particleA.y)-5+"px";
    } else {
        arrowLine.setAttribute("y1", "5");
        arrowLine.setAttribute("y2", particleB.y-particleA.y+5);
        arrowdiv.style.top = Math.round(particleA.y - arrowdiv.style.height / 2 - 5)+"px";
    }
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