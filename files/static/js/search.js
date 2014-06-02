var user_result = "<li><a href='#'><img src='img/biyi.jpg' /><span class='text'>Biyi Adetunji</span><span class='category'>Lekki, Lagos, Nigeria</span></a></li>";

$('#topbar_search_input').focus(function(){
	$('#search-suggestion').show();
});

$('.below_topbar').click(function(){
	$('#search-suggestion').hide();
});

$('#search-button').click(function(){
	$('#topbar_search_input').focus();
});

$('#topbar_search_input').on('input', function(){
	var query = $(this).val().toLowerCase();
	if (query.length === 0) {
		$('#idle').show();
		$('#topbar_search_input_results').hide();
	} else {
		$('#idle').hide();
		$('#topbar_search_input_results').show();
	}

	var user_append_str = "";
	$.each(atwho_user_list, function(i, obj){
		if(obj.name.toLowerCase().indexOf(query) >= 0){
			user_append_str += "<li><a href='"+wall_base_url+"/"+obj.type+"/"+obj.id+"'><i class='icon-user'></i> <span class='text'>"+obj.name+"</span><span class='category'></span></a></li>";
		}
	});
	$('#user_results').html(user_append_str);

	var dept_append_str = "";
	$.each(atwho_dept_list, function(i, obj){
		if(obj.name.toLowerCase().indexOf(query) >= 0){
			dept_append_str += "<li><a href='"+wall_base_url+"/"+obj.type+"/"+obj.id+"'><i class='icon-dept'></i> <span class='text'>"+obj.name+"</span><span class='category'></span></a></li>";
		}
	});
	$('#dept_results').html(dept_append_str);

	var subdept_append_str = "";
	$.each(atwho_subdept_list, function(i, obj){
		if(obj.name.toLowerCase().indexOf(query) >= 0){
			subdept_append_str += "<li><a href='"+wall_base_url+"/"+obj.type+"/"+obj.id+"'><i class='icon-subdept'> </i><span class='text'>"+obj.name+"</span><span class='category'></span></a></li>";
		}
	});
	$('#subdept_results').html(subdept_append_str);
	$('#post_results').html("<li><i class='icon-loading-line'></i> Loading results</li>");
	var post_append_str = "";
	if (query.length < 3) { $('#post_results').html("<li>Type more than 3 characters to search</li>"); return;}
	Dajaxice.apps.search.query( 
		function(data){
			data = data.splice(0,3);
			if (data.length === 0) {post_append_str = '<li>No matching results</li>';}
			$.each(data, function(i, obj){
				if (!obj.subject) {
					obj.subject = "";
				} else {
					obj.subject = "<strong>"+obj.subject+"</strong>:<br>";
				}
				post_append_str += "<li class='post'><a href='"+obj.url+"'><span class='text'>"+obj.author+"</span> <i class='icon-right'> </i> <span class='text'>"+obj.wall+"</span><br>"+obj.created+"<br>"+obj.subject+obj.description+"</a></li>";
			});
			if (post_append_str === "") post_append_str = '<li>No matching results</li>';
			$('#post_results').html(post_append_str);
		},
		{'query': query}
	);
} );
