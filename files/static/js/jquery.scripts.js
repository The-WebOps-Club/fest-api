(function ($, undefined) {
	$.fn.getCursorPosition = function() {
		var el = $(this).get(0)
		var pos = 0
		if ( 'selectionStart' in el ) {
			pos = el.selectionStart;
		} else if ( "selection" in document ) {
			el.focus()
			var Sel = document.selection.createRange();
			var SelLength = document.selection.createRange().text.length
			Sel.moveStart("character", -el.value.length)
			pos = Sel.text.length - SelLength;
		} else {
			console.log("Ouch : Cannot find selection !")
		}
		return pos
	}            

	$.fn.submit_form = function() {
		el = this; $el = $(this)
		if ( ! ( el.tagName == "INPUT" || el.tagName == "TEXTAREA" || 
			el.tagName == "SELECT" || el.tagName == "A") ) {
			console.log("Trying to submit form for an Invalid tag.")
			return;
		}
		my_form = $el.closest("form")
        my_form.submit()
	}

	$.fn.add_to_textarea = function(v) {
		el = this; $el = $(this); 
    	var cur_val = $el.val(), 
    		cur_pos = $el.getCursorPosition(),
    		append_str = v;
    	$el.val(cur_val.substr(0, cur_pos) + append_str + cur_val.substr(cur_pos))
     	$el.focus()
     	el.selectionStart = el.selectionEnd = cur_pos + append_str.length
	}

	
})(jQuery)
