function getPad(fun, data) {
	var csrftoken = getCookie('csrftoken');
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/p/create/pad', true);
    xhr.setRequestHeader('X-CSRFToken', csrftoken);
    xhr.onload = fun;
    xhr.send(JSON.stringify(data));
}

function addPad(fun, data) {
	var csrftoken = getCookie('csrftoken');
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/p/add/pad', true);
    xhr.setRequestHeader('X-CSRFToken', csrftoken);
    xhr.onload = fun;
    xhr.send(JSON.stringify(data));
}
