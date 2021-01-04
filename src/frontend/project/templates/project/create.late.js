(function() {
	window.people = new Set();
	window.pads = new Set();

	form = document.getElementById('project-main-form');
	
	window.actual_people = document.createElement('input');
	window.actual_people.name = 'people';
	window.actual_people.type = 'hidden';
	form.children[0].append(window.actual_people);

	window.actual_pad = document.createElement('input');
	window.actual_pad.name = 'pad';
	window.actual_pad.type = 'hidden';
	form.children[0].append(window.actual_pad);

	form.addEventListener('submit', function (e) {
		console.log(window.people);
		console.log(window.pads);
		window.actual_people.value = JSON.stringify([...window.people]);
		window.actual_pad.value = JSON.stringify([...window.pads]);
	});
})();

function addPadToList() {
	var pad = JSON.parse(this.responseText);
	var element = document.getElementById("{{form.pad.id_for_label}}")
	if (window.pads.has(pad.pk)) return;

	if (element.parentNode.getElementsByClassName('research-selected-choices').length == 0 ) {
		var target = document.createElement('div');
		target.classList.add('research-selected-choices');
		element.parentNode.append(target);
	} else {
		var target = element.parentNode.getElementsByClassName('research-selected-choices')[0];
	}
	
	var entry = document.createElement('a');
	entry.classList.add('research-choice');
	if (pad.url.length > 40) {
		entry.innerHTML = pad.url.slice(0, 35) + ' ...';
	} else {
		entry.innerHTML = pad.url;
	}
	entry.setAttribute('href', pad.url);
	target.append(entry);
	window.pads.add(pad.pk);
	
	console.log(window.pads);	
}

function addPersonToList() {
	var element = document.getElementById("{{form.people.id_for_label}}");
	var value = element.value;
	if (window.people.has(value)) return;
	
	if (element.parentNode.getElementsByClassName('research-selected-choices').length == 0 ) {
		var target = document.createElement('div');
		target.classList.add('research-selected-choices');
		element.parentNode.append(target);
	} else {
		var target = element.parentNode.getElementsByClassName('research-selected-choices')[0];
	}
	
	var entry = document.createElement('div');
	entry.classList.add('research-choice');
	entry.innerHTML = value;
	target.append(entry);
	window.people.add(value);
	element.value = '';
	
	console.log(window.people);
}

(function() {
	var el = document.createElement('a');
	el.innerHTML = 'Add';
	el.classList.add('pure-button');
	var pos = document.getElementById("{{form.people.id_for_label}}");
	pos.name = '';
	pos.parentNode.append(el);
	el.setAttribute('href', 'javascript:addPersonToList()');
})();

(function() {
	var el = document.createElement('a');
	el.innerHTML = 'Add';
	el.classList.add('pure-button');
	var pos = document.getElementById("{{form.pad.id_for_label}}");
	pos.name = '';
	pos.parentNode.append(el);
	el.setAttribute('href', 'javascript:addPad(addPadToList, {"url":document.getElementById("{{form.pad.id_for_label}}").value})');
})();

(function() {
    var el = document.createElement('a');
    el.innerHTML = 'New';
    el.classList.add('pure-button');
    document.getElementById('{{form.pad.id_for_label}}').parentNode.append(el);
    el.setAttribute('href', 'javascript:getPad(addPadToList, {"name":document.getElementById("{{form.title.id_for_label}}").value})');
})();

(function(){
	var peopleinput = document.getElementById("{{form.people.id_for_label}}");
	peoplelist = document.createElement("datalist");
	peoplelist.id = "people_list";
	peopleinput.parentNode.append(peoplelist);
	peopleinput.setAttribute("list", "people_list");
	getFriends(function() {
		friends = JSON.parse(this.responseText);
		friends.forEach(function(people) {
			peopleoption = document.createElement('option');
			peopleoption.label = people.name + ' (' + people.username + ') <' + people.mail + '>';
			peopleoption.value = people.mail;
			peoplelist.appendChild(peopleoption);
		});
	});
})();
