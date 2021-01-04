function getFriends(fun) {
	var csrftoken = getCookie('csrftoken');
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/u/get/friends', true);
    xhr.setRequestHeader('X-CSRFToken', csrftoken);
    xhr.onload = fun;
    xhr.send();
}
