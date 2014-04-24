(function ($, undefined) {
	$.fn.submit_form = function(v) {
		el = $(this).get(0); $el = $(this)
		if ( ! ( el.tagName == "INPUT" || el.tagName == "TEXTAREA" || 
			el.tagName == "SELECT" || el.tagName == "A") ) {
			console.log("Trying to submit form for an Invalid tag.")
			return;
		}
		if (! v) {
			my_form = $el.closest("form")
		} else {
			my_form = $el.closest("form" + str(v))
		}
		console.log(my_form)
        my_form.submit()
	}
})(jQuery)

