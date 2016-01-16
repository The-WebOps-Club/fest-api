

function get_fbid_or_null( id ){
	if (!localStorage)
		return
	
	user_id = "user_" + id
	// console.log(id + "... " + localStorage[user_id])
	if ( ! localStorage[user_id] )
		return

	user_id_data = JSON.parse(localStorage[user_id])
	if( user_id_data.fbid )
		return user_id_data.fbid
}
function push_fbid( id, fbid ){
	if (!localStorage)
		return
	var user_id = "user_" + id
	var data = {"fbid" : fbid}
	// if (localStorage[user_id])
	// 	data = $.extend(true, {}, localStorage[user_id], data)
	localStorage[user_id] = JSON.stringify(data);
}