function showNode(node, doNodeUpdate) {
    //UpdateNavigation code
    if (node.type != "Slot") {
        Dajaxice.structure.getNavigationData(updateNavigation, {'node_id':node.dbId, 'node_type':node.type});
    }

    // reset all nodes
    var graphNode = document.getElementById('graph');
    for (var i = 0; i < graphNode.circles.length; i++) {
        // make circles clickable
        graphNode.circles[i].firstChild.nextSibling.nextSibling.firstChild.setAttribute("class", "linklike");
    }

    // mark centerCircle clicked
    node.firstChild.nextSibling.nextSibling.firstChild.setAttribute("class", "");

    graphNode.centerCircle = node;
    if (doNodeUpdate) {
        document.getElementById("text").waitForText = true;
        showText(node);
        Dajaxice.structure.getNodeInfo(updateNode, {'node_id':node.dbId, 'node_type':node.type});
    }
}


function updateNode(data) {
    var graphNode = document.getElementById('graph');

    var currentIndex = getIndexInCircles(graphNode.circles, data['id'], data['type']);
    var currentNode = graphNode.circles[currentIndex];
    currentNode.textPart = data['text'];
    document.getElementById("text").waitForText = false;
    Hyphenator.run();
}

