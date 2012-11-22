function updateNavigation(data) {
    var navigationNode = document.getElementById('navbar');
    var outerList = document.createElement('ol');
    var noGraph = false;
    if (!document.getElementById('graph')) {
        noGraph = true;
    }
    for (var i = 0; i < data['history'].length; i++) {
        var outerListElement = document.createElement('li');
        outerListElement.setAttribute('onmouseover',"this.parentNode.parentNode.style.overflow = 'visible'; this.parentNode.parentNode.style.zIndex = 2;");
        outerListElement.setAttribute('onmouseout',"this.parentNode.parentNode.style.overflow = 'auto'; this.parentNode.parentNode.style.zIndex = 1;");
        var innerList = document.createElement('ol');
        for (var j = 0; j < data['history'][i].length; j++) {
            var innerListElement = document.createElement('li');
            var link = document.createElement('a');
            if (noGraph) {
                link.setAttribute('href',data['history'][i][j]['path']);
            } else {
                link.style.cursor = "pointer";
                link.setAttribute('onclick',"navigateTo(event," + data['history'][i][j]['id'] + ",'" + data['history'][i][j]['type'] + "');");
            }
            var title = document.createTextNode(data['history'][i][j]['title']);
            link.appendChild(title);
            innerListElement.appendChild(link);
            innerList.appendChild(innerListElement);
        }
        outerListElement.appendChild(innerList);
        outerList.appendChild(outerListElement);
    }
    outerListElement = document.createElement('li');
    outerListElement.setAttribute('onmouseover',"this.parentNode.parentNode.style.overflow = 'visible'; this.parentNode.parentNode.style.zIndex = 2;");
    outerListElement.setAttribute('onmouseout',"this.parentNode.parentNode.style.overflow = 'auto'; this.parentNode.parentNode.style.zIndex = 1;");
    outerListElement.style.minHeight = "85px";
    if (document.getElementById('graph')) {
        outerListElement.appendChild(document.getElementById('graph'));
    }
    outerList.appendChild(outerListElement);
    if (data['slot_list'].length > 0) {
        outerListElement = document.createElement('li');
        outerListElement.setAttribute('onmouseover',"this.parentNode.parentNode.style.overflow = 'visible'; this.parentNode.parentNode.style.zIndex = 2;");
        outerListElement.setAttribute('onmouseout',"this.parentNode.parentNode.style.overflow = 'auto'; this.parentNode.parentNode.style.zIndex = 1;");
        innerList = document.createElement('ol');
        for (i = 0; i < data['slot_list'].length; i++) {
            innerListElement = document.createElement('li');
            link = document.createElement('a');
            if (noGraph) {
                link.setAttribute('href', data['slot_list'][i]['path']);
            } else {
                link.style.cursor = "pointer";
                link.setAttribute('onclick',"navigateTo(event," + data['slot_list'][i]['id'] + ",'" + data['slot_list'][i]['type'] + "');");
            }
            title = document.createTextNode(data['slot_list'][i]['title']);
            link.appendChild(title);
            innerListElement.appendChild(link);
            innerList.appendChild(innerListElement);
        }
        outerListElement.appendChild(innerList);
        outerList.appendChild(outerListElement);
    }
    while ( navigationNode.firstChild ) navigationNode.removeChild( navigationNode.firstChild );
    navigationNode.appendChild(outerList);
}

function navigateTo(event, id, type) {
    event.preventDefault();
    Dajaxice.structure.getNavigationData(updateNavigation, {'node_id':id, 'node_type':type});
    document.getElementById("text").waitForText = id;
    showText("<p>Text noch nicht geladen.</p>");
    Dajaxice.structure.getNodeInfo(updateNode, {'node_id':id, 'node_type':type});
}