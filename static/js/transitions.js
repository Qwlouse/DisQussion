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
    var newGraph = false;

    var currentIndex = getIndexInCircles(graphNode.circles, data['id'], data['type']);
    if (currentIndex < 0) {
        buildAnchorGraph(JSON.parse(data['graph_data']));
        currentIndex = getIndexInCircles(graphNode.circles, data['id'], data['type']);
        newGraph = true;
    }
    var currentNode = graphNode.circles[currentIndex];
    currentNode.textPart = data['text'];
    currentNode.votingInfo = data['voting'];
    document.getElementById("text").waitForText = false;
    if (!history.state || history.state['url'] == data['url']) {
        history.replaceState(data,data['url'],data['url']);
    } else {
        history.pushState(data,data['url'],data['url']);
    }
    if (newGraph) {
        showNode(currentNode, true);
    }
}

window.onpopstate = function(event) {
    if (event.state) {
        //UpdateNavigation code
        Dajaxice.structure.getNavigationData(updateNavigation, {'node_id':event.state['id'], 'node_type':event.state['type']});
        var graphNode = document.getElementById('graph');
        var currentIndex = getIndexInCircles(graphNode.circles, event.state['id'], event.state['type']);
        if (currentIndex < 0) {
            buildAnchorGraph(JSON.parse(event.state['graph_data']));
            currentIndex = getIndexInCircles(graphNode.circles, event.state['id'], event.state['type']);
        }
        var currentNode = graphNode.circles[currentIndex];
        // reset all nodes
        for (var i = 0; i < graphNode.circles.length; i++) {
            // make circles clickable
            graphNode.circles[i].firstChild.nextSibling.nextSibling.firstChild.setAttribute("class", "linklike");
        }

        // mark centerCircle clicked
        currentNode.firstChild.nextSibling.nextSibling.firstChild.setAttribute("class", "");

        graphNode.centerCircle = currentNode;
        document.getElementById("text").waitForText = true;
        showText(currentNode);
        updateNode(event.state);
    }
};