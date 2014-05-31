$('#topbar_search_input').focus(function(){
	$('#search-suggestion').show();
});

$('#topbar_search_input').focusout(function(){
	$('#search-suggestion').hide();
});

$('#search-button').click(function(){
	$('#topbar_search_input').focus();
});

$('#topbar_search_input').on('input', function(){
	console.log('changed');
	var query = $(this).val();
	console.log(query);
	Dajaxice.apps.search.hello( 
		function(data){
			console.log(data);
		},
		{'query': query}
	);
} );
