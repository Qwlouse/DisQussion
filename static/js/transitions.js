function showNode(node) {
    //UpdateNavigation code
    if (node.type != "Slot") {
        alert(node.type);
        Dajaxice.structure.getHistory(updateNavigation, {'node_id':node.dbId, 'node_type':node.type});
    }
    //ShowNode code
    var graphNode = document.getElementById('graph');
    while ( graphNode.firstChild ) graphNode.removeChild( graphNode.firstChild );
    graphNode.appendChild(node);
    var newCircles = new Array(node);
    if (node.parent != null)
    {
        newCircles.push(node.parent);
        graphNode.appendChild(node.parent);
        graphNode.arrows = new Array(createArrowStructure(node.parent, node));
        graphNode.insertBefore(graphNode.arrows[0], graphNode.firstChild);
    }
    graphNode.circles = newCircles;
    var circles = graphNode.circles;
    //var i = 1;
    // remove ALL other nodes TODO: keep parent for back-navigation
    /*while (circles.length > 3) {
     if (circles[i] == node) {
     i++;
     } else {
     if (circles[i] == node.forces[0].massB) {
     i++;
     } else {
     circles.splice(i, 1);
     }
     }
     }*/
    // reset all nodes
    for (var i = 0; i < circles.length; i++) {
        // make circles clickable
        graphNode.circles[i].firstChild.firstChild.setAttribute("class", "linklike");
        // remove force to center
        graphNode.circles[i].particle.targetY = 0.0;
        graphNode.circles[i].particle.targetX = null;
        graphNode.circles[i].particle.targetForce = 0.003;
    }
    // pull node to center
    node.particle.targetX = 0.0;
    node.particle.targetForce = 0.02;

    // mark centerCircle clicked
    for (i = 0; i < node.firstChild.firstChild.attributes.length; i++){
        if (node.firstChild.firstChild.attributes[i].name == "class"){
            node.firstChild.firstChild.attributes[i].value = "";
        }
    }

    graphNode.centerCircle = node;
    document.getElementById("text").waitForText = true;
    Dajaxice.structure.getNodeInfo(amendGraph, {'node_id':node.dbId, 'node_type':node.type});
    showText(node);
}