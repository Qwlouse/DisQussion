function updateNavigation(data) {
    var navigationNode = document.getElementById('navbar');
    var outerList = document.createElement('ol');
    for (var i = 0; i < data['history'].length; i++) {
        var outerListElement = document.createElement('li');
        var innerList = document.createElement('ol');
        for (var j = 0; j < data['history'][i].length; j++) {
            var innerListElement = document.createElement('li');
            var link = document.createElement('a');
            link.setAttribute('href',data['history'][i][j]['path']);
            link.setAttribute('onclick',"navigateTo(event,"+data['history'][i][j]['id']+");");
            var title = document.createTextNode(data['history'][i][j]['title']);
            link.appendChild(title);
            innerListElement.appendChild(link);
            innerList.appendChild(innerListElement);
        }
        outerListElement.appendChild(innerList);
        outerList.appendChild(outerListElement);
    }
    outerListElement = document.createElement('li');
    if (document.getElementById('graph')) {
        outerListElement.appendChild(document.getElementById('graph'));
    }
    outerList.appendChild(outerListElement);
    if (data['slot_list'].length > 0) {
        outerListElement = document.createElement('li');
        innerList = document.createElement('ol');
        for (i = 0; i < data['slot_list'].length; i++) {
            innerListElement = document.createElement('li');
            link = document.createElement('a');
            link.setAttribute('href', data['slot_list'][i]['path']);
            link.setAttribute('onclick', "navigateTo(event," + data['slot_list'][i]['id'] + ");");
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

function navigateTo(event, id) {
    //event.preventDefault();
    //alert(id);
}