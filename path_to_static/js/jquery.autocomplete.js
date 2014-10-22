(function ($) {

    $.fn.AutoComplete = function (searchUrl) {
        setAutoComplete($(this).attr("id"), searchUrl);
        return true
    }
})(jQuery);

var result_Count   =  0;
var result_Selected = -1;
var delay = 500;
var searchPage = null;
var divResultsID = "divAutoCompleteResults";
var divSearchID = "divAutoCompleteSearch";
var hdnSelectedUrlID = "hdnUrl";
var hdnSelecetedTextID = "hdnValue";
var txtSearchBox = null;
var divResults  = null;

function setAutoComplete(searchBoxID, searchUrl) {

	// initialize vars
    searchPage = searchUrl;
    
	// register mostly used vars
	txtSearchBox = $("#" + searchBoxID);
    
	// create the results div
	createResultsDiv();
	
	// on blur listener
	txtSearchBox.blur(function(){ setTimeout("clearResults()", 200) });

	// on key up listener
	txtSearchBox.keyup(function (e) {

	    // get keyCode (window.event is for IE)
	    var keyCode = e.keyCode || window.event.keyCode;
	    var lastSearch = txtSearchBox.val();

	    // check for an ENTER 
	    if (keyCode == 13) {
	        OnEnterClick();
	        return;
	    }

	    // check an treat up and down arrows
	    if (OnUpDownClick(keyCode)) {
	        return;
	    }

	    // check for an ESC
	    if (keyCode == 27) {
	        clearResults();
	        return;
	    }

	    // if is text, call with delay
	    setTimeout(function () { updateResults(lastSearch) }, delay);
	});
}

// treat the auto-complete action (delayed function)
function updateResults(lastSearchWord)
{
	// get the field value
	var searchWord = txtSearchBox.val();

	// if it's empty clear the resuts box and return
	if(searchWord == ''){
		clearResults();
		return;
	}

	// if it's equal the value from the time of the call, allow
	if(lastSearchWord != searchWord){
		return;
	}

	$.ajax({
	    type: "GET",
	    //ToDo: relative url
	    url: searchPage + searchWord,
	    cache: false,
	    success: function (html) {
	        var $response = $(html);

	        // get the total of results
	        var ansLength = $response.length;
            
	        if (ansLength > 0) {

	            var newData = $response.find("#" + divSearchID).html();

	            // update the results div
	            divResults.html(newData);
	            divResults.highlight(searchWord);
	            divResults.css("display", "block");

	            // for all divs in results
	            var divs = $("#" + divResultsID + " > div");
                
                //setting the number of suggested items
                result_Count = divs.size();

	            // on mouse over clean previous selected and set a new one
	            divs.mouseover(function () {
	                divs.each(function () { this.className = "unselected"; });
	                this.className = "selected";
	            })

	            // on click copy the result text to the search field and hide
	            divs.click(function () {
	                txtSearchBox.val($(this).find("#" + hdnSelecetedTextID)[0].value);
	                window.location = $(this).find("#" + hdnSelectedUrlID)[0].value;
	                clearResults();
	            });
	        }
	        else {
	            clearResults();
	        }
	    }
	});
}

// clear auto complete box
function clearResults()
{
	divResults.html('');
	divResults.css("display","none");
}

// create the results div accordingly to the search field
function createResultsDiv() {

    //  create the div results
    $("body").append('<div id="' + divResultsID + '"></div>');
    divResults = $("#" + divResultsID);
    
	// get the field position
	var searchBox_Position    = txtSearchBox.offset();
	var searchBox_Top    = searchBox_Position.top;
	var searchBox_Left   = searchBox_Position.left;

	// get the field size
	var searchBox_Height = txtSearchBox.height();
	var searchBox_Width  = txtSearchBox.width();

	// apply the css styles - optimized for Firefox
	divResults.css("position","absolute");
	divResults.css("left", searchBox_Left - 2);
	divResults.css("top", searchBox_Top + searchBox_Height );
	divResults.css("width", searchBox_Width - 2);
}


// treat up and down key strokes defining the next selected element
function OnUpDownClick(keyCode) {
	if(keyCode == 40 || keyCode == 38){

		if(keyCode == 38){ // keyUp
			if(result_Selected == 0 || result_Selected == -1){
				result_Selected = result_Count-1;
			}else{
				result_Selected--;
			}
		} else { // keyDown
			if(result_Selected == result_Count-1){
				result_Selected = 0;
			}else {
				result_Selected++;
			}
		}

		// loop through each result div applying the correct style
		divResults.children().each(function(i){
		    if (i == result_Selected) {
		        txtSearchBox.val($(this).find("#" + hdnSelecetedTextID)[0].value);
				this.className = "selected";
			} else {
				this.className = "unselected";
			}
		});

		return true;
	} else {
		// reset
		result_Selected = -1;
		return false;
	}
}
function OnEnterClick() {
    divResults.children().each(function (i) {
        if (i == result_Selected) {
            window.location = $(this).find("#" + hdnSelectedUrlID)[0].value;
        }
    });
    clearResults();
}