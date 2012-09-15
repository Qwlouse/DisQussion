function insert_tag(aTag, eTag) {
    var input = document.forms["text_form"].elements["text"];
    /* für Internet Explorer */
    if(typeof document.selection != 'undefined') {
        /* Einfügen des Formatierungscodes */
        var range = document.selection.createRange();
        var insText = range.text;
        range.text = aTag + insText + eTag;
        /* Anpassen der Cursorposition */
        range = document.selection.createRange();
        if (insText.length == 0) {
            range.move('character', -eTag.length);
        } else {
            range.moveStart('character', aTag.length + insText.length + eTag.length);
        }
        range.select();
    }
    /* für neuere auf Gecko basierende Browser */
    else if(typeof input.selectionStart != 'undefined')
    {
        /* Einfügen des Formatierungscodes */
        var start = input.selectionStart;
        var end = input.selectionEnd;
        var insText = input.value.substring(start, end);
        input.value = input.value.substr(0, start) + aTag + insText + eTag + input.value.substr(end);
        /* Anpassen der Cursorposition */
        var pos;
        if (insText.length == 0) {
            pos = start + aTag.length;
        } else {
            pos = start + aTag.length + insText.length + eTag.length;
        }
        input.selectionStart = pos;
        input.selectionEnd = pos;
    }
    /* für die übrigen Browser */
    else
    {
        /* Abfrage der Einfügeposition */
        var pos;
        var re = new RegExp('^[0-9]{0,3}$');
        while(!re.test(pos)) {
            pos = prompt("Einfügen an Position (0.." + input.value.length + "):", "0");
        }
        if(pos > input.value.length) {
            pos = input.value.length;
        }
        /* Einfügen des Formatierungscodes */
        var insText = prompt("Bitte geben Sie den zu formatierenden Text ein:");
        input.value = input.value.substr(0, pos) + aTag + insText + eTag + input.value.substr(pos);
    }
}

function insert_line_tag(aTag) {
    var input = document.forms["text_form"].elements["text"];
    /* für Internet Explorer */
    if(typeof document.selection != 'undefined') {
        /* Einfügen des Formatierungscodes */
        var range = document.selection.createRange();
        range.setStart(input, 0);
        var insText = range.text;
        range.text = aTag + insText;
        /* Anpassen der Cursorposition */
        range = document.selection.createRange();
        if (insText.length == 0) {
            range.move('character', 0);
        } else {
            range.moveStart('character', aTag.length + insText.length);
        }
        range.select();
    }
    /* für neuere auf Gecko basierende Browser */
    else if(typeof input.selectionStart != 'undefined')
    {
        /* Einfügen des Formatierungscodes */
        var start = 0;
        var end = input.selectionEnd;
        var insText = input.value.substring(start, end);
        input.value = input.value.substr(0, start) + aTag + insText + input.value.substr(end);
        /* Anpassen der Cursorposition */
        var pos;
        if (insText.length == 0) {
            pos = start + aTag.length;
        } else {
            pos = start + aTag.length + insText.length;
        }
        input.selectionStart = 0;
        input.selectionEnd = pos;
    }
    /* für die übrigen Browser */
    else
    {
        var pos = 0;
        /* Einfügen des Formatierungscodes */
        var insText = prompt("Bitte geben Sie den zu formatierenden Text ein:");
        input.value = input.value.substr(0, pos) + aTag + insText + input.value.substr(pos);
    }
}