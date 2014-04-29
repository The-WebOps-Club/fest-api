
function display_pic(el, size) {
	$el = $(el)
	$.each($el, function(i, v) {
		var $v = $(v)
		var fbid = $.trim($v.data("fbid"))
		var size = size || $v.data("size") || 60
		if ( fbid.length > 2  ) {
			
			var pic_src = "http://graph.facebook.com/" + fbid +  "/picture?height=" + size + "&width=" + size;
	        $v.prop("src", pic_src);

		} else {

			console.log($v.data("id"))

			Dajaxice.apps.users.get_info(function(data) {
		    	var $v = $(v);

		    	if ( ! data["fbid"] ) {
		    		data["fbid"] = "Shaastra"
		    	}
		    	var pic_src = "http://graph.facebook.com/" + data["fbid"] +  "/picture?height=" + size + "&width=" + size;
		       	$v.prop("src", pic_src);
		        var filter_users = $.grep(atwho_user_list, function(a) { return a.id == data["id"] } )
				filter_users[0].fbid = data["fbid"];
			}, {"id" : $v.data("id") } )

		}
	})
}

$( document ).load(function() {
	display_pic($(".display_pic"))
})