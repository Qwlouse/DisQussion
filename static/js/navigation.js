function updateNavigation(data) {
    var navigationNode = document.getElementById('navbar');
    var graphNode = document.getElementById('graph');
    var outerList = document.createElement('ol');
    for (var i = 0; i < data.length; i++) {
        var outerListElement = document.createElement('li');
        var innerList = document.createElement('ol');
        for (var j = 0; j < data[i].length; j++) {
            var innerListElement = document.createElement('li');
            var link = document.createElement('a');
            link.setAttribute('href',data[i][j]['path']);
            link.setAttribute('onclick',"navigateTo(event,"+data[i][j]['id']+");");
            var title = document.createTextNode(data[i][j]['title']);
            link.appendChild(title);
            innerListElement.appendChild(link);
            innerList.appendChild(innerListElement);
        }
        outerListElement.appendChild(innerList);
        outerList.appendChild(outerListElement);
    }
    outerListElement = document.createElement('li');
    outerListElement.appendChild(graphNode);
    outerList.appendChild(outerListElement);
    //alert("xxx76364736.");
    while ( navigationNode.firstChild ) navigationNode.removeChild( navigationNode.firstChild );
    navigationNode.appendChild(outerList);
    //alert("ganuralischowuraka.");
}

function navigateTo(event, id) {
    event.preventDefault();
    alert(id);
}