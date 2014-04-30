

function get_fbid_or_null( id ){
	if(!localStorage.fbids)
		return null;

	fbids = JSON.parse(localStorage.fbids);
	if( fbids[id] != undefined )
		return fbids[id];
	else
		return null;
}

function push_fbid( id, fbid ){
	if( !localStorage.fbids )
		storage = {}
	else
		storage = JSON.stringify(localStorage.fbids);

	storage[id] = fbid;

	localStorage.fbids = JSON.parse(storage);
}