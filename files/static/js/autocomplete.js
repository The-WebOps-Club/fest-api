all_list = null;
atwho_user_list = null;
atwho_subdept_list = null;
atwho_dept_list = null;
atwho_page_list = null;
atwho_file_list = null;
atwho_file_list_raw = [];
atwho_setup = false;

regex_emoticons = []
emoticons = {
    "like" : ["(Y)"],
    "colonthree" : [ ":3", ":-3" ],
    "cry" : [ ";(", ":'(", ":'-(", ";-(", ";_;" ],
    "frown" : [ ":(", ":-(", ":C", ":[", ":-[" ], 
    "gasp" : [":o", ":-o"],
    "grin" : [ ":D", ":-D", "XD", "X-D", "=D", ], 
    "grumpy" : [">_<", "&lt;_&gt;", ":-S", ], 
    "heart" : ["<3", "&lt;3"],
    "kiki" : ["^_^"],
    "kiss" : [":*", ":-*"],
    "pacman" : [":v", ":-v"],
    "smile" : [ ":)", ":-)", ":]", "=)", "=]", ":}" ], 
    "sunglasses" : ["B-)"],
    "tongue" : [":P", ":-P", "XP", "X-P",],
    "unsure" : [":/", ":-/", ":-\\"],
    "wink" : [";)", ";-)", "^_-", ";D", ";-D", ";]", ";-]"],
    "angel" : ["O:)", "O:-)", "o:-)", "o:)", "0:)", "0:-)"],
    "surprised" : ["o.o", "o_o", "0.o", "o.0", "0_0"],
    "devil" : ["}:)", "}:-)", "3:)", "3:-)"],
    "glasses" : ["8-)"],
    "penguin" : ["<(\")" ],
    "poop" : [":poop:"],
    "teeth" : [":E", ":-E"],
    "tears-of-joy" : [ ";D", ";-D"],
    "squint" : ["-_-"],
}

function get_autocomplete_lists(url1, url2, url3, url4) {
    atwho_user_list = null;
    atwho_subdept_list = null;
    atwho_dept_list = null;

    // Autocomplete for Users, Dept, Subdept
    $.getJSON(url1, function(json) {
        atwho_user_list = json;
        sync_autocomplete();
    });
    $.getJSON(url2, function(json) {
        atwho_subdept_list = json;
        sync_autocomplete();
    });
    $.getJSON(url3, function(json) {
        atwho_dept_list = json;
        sync_autocomplete();
    });
    $.getJSON(url4, function(json) {
        atwho_page_list = json;
        sync_autocomplete();
    });
}

function get_autocomplete_file_data(url1, url2, url3) {
    if (!gapi.client.drive) {
        atwho_file_list = null;
        return;
    }
    setup_autocomplete_files();
 }

function sync_autocomplete() {
    if (!atwho_setup && ( atwho_user_list && atwho_subdept_list && atwho_dept_list && atwho_page_list ) ) {
        atwho_setup = true
        // Fix the lists to my format :)
        if (atwho_user_list) {
            atwho_user_list = $.map(atwho_user_list, function(value, i) {
                if (value["first_name"] + " " + value["last_name"] != " " ) // To make sure no blank users are taken. eg : superusers
                    return {
                        "id": value["id"],
                        "name": value["first_name"] + " " + value["last_name"],
                        "type": "user"
                    };
            })
        }
        if (atwho_dept_list) {
            atwho_dept_list = $.map(atwho_dept_list, function(value, i) {
                return {
                    "id": value["id"],
                    "name": value["name"],
                    "type": "dept"
                };
            })
        }
        if (atwho_subdept_list) {
            atwho_subdept_list = $.map(atwho_subdept_list, function(value, i) {
                return {
                    "id": value["id"],
                    "name": value["name"],
                    "type": "subdept"
                };
            })
        }
        if (atwho_page_list) {
            atwho_page_list = $.map(atwho_page_list, function(value, i) {
                return {
                    "id": value["id"],
                    "name": value["name"],
                    "type": "page"
                };
            })
        }
        
        setup_autocomplete_lists();
        on_dom_change()
    }
}

function setup_autocomplete_files() {
    at_config_file = {
        at: "#",
        data: [],
        tpl: "<li data-value='[${name}](${iconlink} \"doc#${id}\")'><img src='${iconlink}' style='height:12px'> &nbsp; ${name} </li>",
        show_the_at: true,
        callbacks: {
            remote_filter: function(query, callback) {
                callback([{
                    "id": "",
                    "name": "Loading ...",
                    "iconlink": site_url + "static/img/loading_line.gif",
                }]);
                /* check if gapi is loaded, authorized and linked with drive*/
                if ( gapi && gapi.client && gapi.client.drive) {
                    if (query != '') {
                        gapi.client.drive.files.list({
                            q: 'title contains \'' + query + '\'',
                            maxResults: 5,
                            fields: 'items(title,id,iconLink)',
                        }).execute(function(response) {
                            if ( ! response.items ) {
  								callback([{
				                    "id": "",
				                    "name": "Cannot connect to google. Please check your connection",
				                    "iconlink": site_url + "static/img/loading_line.gif",
				                }]);
  								return 
  							}
                            if ( response.items.length == 0 ) {
                                callback($.map(response.items, function(value, i) {
                                    return {
                                        "id": "",
                                        "name": "No files found !",
                                        "iconlink": site_url + "static/img/loading_line.gif",
                                    }
                                }));
                            }
                            else {
                                callback($.map(response.items, function(value, i) {
                                    return {
                                        "id": value['id'],
                                        "name": value['title'],
                                        "iconlink": value['iconLink'],
                                    }
                                }));
                            }
                        });
                    } else {
                        callback([{
                            "id": "",
                            "name": "Too many items. Please type more",
                            "iconlink": site_url + "static/img/loading_line.gif",
                        }]);
                    }
                }
            },
        },
    }
    if(contentEditableActive)
        at_config_file.tpl = "<li data-value='<a href=\""+site_url+"docs/view/?id=${id}\"><img src=\"${iconlink}\" style=\"width:16px;height:16px\">${name}</a><span></span>'>${name}</li>";
    $('.atwho_at_config').atwho(at_config_file);
}

function setup_autocomplete_lists() {

    goto_wall = {
        before_insert: function(value, $li) {
            owner_type = $li.data("type")
            document.location.href = site_url + "wall/" + owner_type + "/" + $li.data("id")
            return value;
        },
    }

    all_list = atwho_user_list.concat(atwho_dept_list).concat(atwho_subdept_list).concat(atwho_page_list)
    at_config = {
        at: "@",
        data: all_list,
        tpl: "<li data-value='[${name}](${type}#${id} \"${type}#${id}\")'>${name}</li>",
        show_the_at: true,
        max_len: 20,
    }
    if(contentEditableActive)
        //at_config.tpl = "<li data-value='<a href=\""+site_url+"wall/${type}/${id}\" data-notify=\"${type}#${id}\"><img src=\""+site_url+"static/img/neutral.png\" style=\"width:16px;height:16px\">${name}</a><span></span>'>${name}</li>"
        at_config.tpl = "<li data-value='<a href=\""+site_url+"wall/${type}/${id}\" data-notify=\"${type}#${id}\"><i class=\"icon-user\"></i>${name}</a>'>${name}</li>"
  
    $("#topbar_search_input").atwho({
        at: "",
        data: all_list,
        tpl: "<li data-value='${name}' data-id='${id}' data-type='${type}'>${name}</li>",
        show_the_at: false,
        callbacks: goto_wall,
    })

    $(".atwho_at_config").atwho(at_config)

    var $select = $("select.select_all_list")
    for (var i in all_list) {
        var opt_val = all_list[i]['type'] + "_" + all_list[i]['id']
        if ( $select.find("[value=" + opt_val + "]").length == 0 ) {
            $select.append(
                "<option value='" + opt_val + "'>" +
                all_list[i]['name'] +
                "</option>")
        }
    }
    $(".right_search .searchbar input").keyup()
}

(function($){
    $.fn.markdown = function(){
        var $els = this
        $.each($els, function(i, el){
            var $el = $(el)
            // EMOTICONS
            $.each(emoticons, function(i, v) {
                if ( v.length ) {
                    if ( ! regex_emoticons[i] ) {
                        var replace_str = "(^|\\s|>)(" + v.join("~~@~~")
                            .replace(/[\-\[\]\/\{\}\(\)\*\+\?\.\\\^\$\|]/gi, "\\$&")
                            .replace(/~~@~~/gi, "|") + ")(\\s|$|<)";
                        var regex = new RegExp(replace_str, "gi")    

                        regex_emoticons[i] = regex
                    }
                    var regex = regex_emoticons[i]
                    init_string = $el.html()
                    $el.html( init_string.replace(regex, "$1<i class='icon-" + i + "'></i>$3") )
                }
            })
            // USER RENDER
        })
    };


    $.fn.get_dp = function(size){
        var $els = this
        $.each($els, function(i, v) {
            var $v = $(v)
            var id = $.trim($v.data("id"))
            var fbid = $.trim($v.data("fbid"))
            var size = size || $v.data("size") || 60
            if ( ! id )
                return

            if( fbid.length < 2 )
                fbid = get_fbid_or_null(id);

            if( fbid && fbid.length > 2 ) {
                var pic_src = "http://graph.facebook.com/" + fbid +  "/picture?height=" + size + "&width=" + size;
                $v.prop("src", pic_src);

            } else {

                if ( ! atwho_user_list ) {
                    // As some places have these in templates
                    return
                } else {
                    Dajaxice.apps.users.get_info(function(data) {
                        var $v = $(v);
                        if ( ! data["fbid"] || data["fbid"] == "" ) {
                            data["fbid"] = fest_fbid;
                        }
                        var pic_src = "http://graph.facebook.com/" + data["fbid"] +  "/picture?height=" + size + "&width=" + size;
                        $v.prop("src", pic_src);
                        //var filter_users = $.grep(atwho_user_list, function(a) { return a.id == data["id"] } )
                        //filter_users[0].fbid = data["fbid"];
                        $v.data("fbid", data["fbid"])
                        push_fbid(data['id'], data['fbid']);

                    }, {"id" : $v.data("id") } )
                }
            }
        })
    }

    $.fn.get_link_preview = function() {
	    var $els = $(this);
	    var elarray = {};
	    $.each($els, function(i, v) {
	        var $v = $(v);
	        var service = $v.data("service");
	        var id = $v.data("link-id");

	        if ( service == "youtube" ) {
	            var url = "http://gdata.youtube.com/feeds/api/videos/" + id + "?v=2&alt=jsonc";
	            $.ajax({url:url, dataType:'json', success:function(json) {
	                //var json = JSON.parse( data );
	                var $el = $('a[data-link-id=\''+json.data.id+'\']');
	                if ( ! $el.hasClass("comment_link_render") )
	                    return

	                $el.append("<div class='row-fluid video_comment'>" +
	                    "<div class='span4 left'>" +
	                        "<img src='" + json.data.thumbnail.sqDefault + "' width='100%' height='auto' />" +
	                    "</div>" +
	                    "<div class='span8 right'>" +
	                        "<h5 class='title'>" + json.data.title + "</h5>" +
	                        "<p class='desc'>" + json.data.description + "</p>" +
	                    "</div>" +
	                "</div>");
	                $el.removeClass("comment_link_render");
	            }});

	        } else if ( service == "vimeo") {

	        }
	        
	    })
	}


})(jQuery);

