all_list = []
atwho_user_list = [];
atwho_subdept_list = [];
atwho_dept_list = [];
atwho_file_list = [];
atwho_file_list_raw = [];
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
    "sunglasses" : ["B)", "B-)"],
    "tongue" : [":P", ":-P", "XP", "X-P",],
    "unsure" : [":/", ":-/", ":-\\"],
    "wink" : [";)", ";-)", "^_-", ";D", ";-D", ";]", ";-]"],
    "angel" : ["O:)", "O:-)", "o:-)", "o:)", "0:)", "0:-)"],
    "surprised" : ["o.o", "o_o", "0.0", "0_0"],
    "devil" : ["}:)", "}:-)", "3:)", "3:-)"],
    "glasses" : ["8)", "8-)"],
    "penguin" : ["<(\")" ],
    "poop" : [":poop:"],
    "teeth" : [":E", ":-E"],
    "tears-of-joy" : [ ";D", ";-D"],
    "squint" : ["-_-"],
}

function get_autocomplete_lists(url1, url2, url3) {
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
}

function get_autocomplete_file_data(url1, url2, url3) {
    if (!gapi.client.drive) {
        atwho_file_list = null;
        return;
    }
    console.log('get file lists from google.');
    gapi.client.drive.files.list({
        'fields': ['title', 'id', 'mimeType', 'iconLink']
    }).execute(function(response) {
        console.log('obtained response');
        console.log(response);
        atwho_file_list_raw = response.items;
        setup_autocomplete_files();
    });
}

function sync_autocomplete() {
    if (atwho_user_list && atwho_subdept_list && atwho_dept_list) {
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
                    "name": "",
                    "small": "Loading ...",
                    "iconlink": site_url + "static/img/loading-dice.gif",
                }]);
                console.log('refreshing list');
                /* check if gapi is loaded, authorized and linked with drive*/
                if ( gapi && gapi.client && gapi.client.drive) {
                    if (query != '') {
                        gapi.client.drive.files.list({
                            q: 'title contains \'' + query + '\'',
                            maxResults: 5
                        }).execute(function(response) {
  							if ( ! response.items ) {
  								callback([{
				                    "id": "",
				                    "name": "",
				                    "small": "Cannot connect to google. Please check your connection",
				                    "iconlink": site_url + "static/img/loading-dice.gif",
				                }]);
  								return 
  							}
                            if ( response.items.length == 0 ) {
                                callback($.map(response.items, function(value, i) {
                                    return {
                                        "id": "",
                                        "name": "",
                                        "small": "No files found !",
                                        "iconlink": site_url + "static/img/loading-dice.gif",
                                    }
                                }));
                            }
                            else {
                                callback($.map(response.items, function(value, i) {
                                    return {
                                        "id": value['id'],
                                        "name": value['title'],
                                        "small": value['mimeType'],
                                        "iconlink": value['iconLink'],
                                    }
                                }));
                            }
                        });
                    } else {
                        callback([{
                            "id": "",
                            "name": "",
                            "small": "Too many items. Please type more",
                            "iconlink": site_url + "static/img/loading-dice.gif",
                        }]);
                    }
                }
            },
            // before_insert: function(value, $li) {
            //     if (this.$inputor.parent().find(".textarea_atwho_list[value='" + value + "']").length == 0) {
            //         this.$inputor.after("<input class='textarea_atwho_list' name='atwho_files' value='" + $li.data("filename") + "--@@!@@--" + $li.data("id") + "--@@!@@--" + $li.data("icon") + "' type='hidden'/>");
            //     }
            //     return value;
            // },
        },
    }
    if(contentEditableActive)
        at_config_file.tpl = "<li data-value='<a href=\""+site_url+"docs/view/?id=${id}\"><img src=\"${iconlink}\" style=\"width:16px;height:16px\">${name}</a><span></span>'>${name} <small>${small}</small></li>";
    $('.atwho_at_config').atwho(at_config_file);
}

function setup_autocomplete_lists() {
    goto_wall = {
        before_insert: function(value, $li) {
            console.log($li)
            owner_type = "user"
            if ($li.data("small") == "Department") {
                owner_type = "dept"
            } else if ($li.data("small") == "Subdept") {
                owner_type = "subdept"
            }
            document.location.href = site_url + "wall/" + owner_type + "/" + $li.data("id")
            return value;
        },
    }

    if (atwho_user_list) {
        atwho_user_list = $.map(atwho_user_list, function(value, i) {
            if (value["first_name"] + " " + value["last_name"] != " " ) // To make sure no blank users are taken. eg : superusers
                return {
                    "id": value["id"],
                    "name": value["first_name"] + " " + value["last_name"],
                    "small": value["email"],
                    "type": "user"
                };
        })
    }
    if (atwho_dept_list) {
        atwho_dept_list = $.map(atwho_dept_list, function(value, i) {
            return {
                "id": value["id"],
                "name": value["name"],
                "small": "Department",
                "type": "dept"
            };
        })
    }
    if (atwho_subdept_list) {
        atwho_subdept_list = $.map(atwho_subdept_list, function(value, i) {
            return {
                "id": value["id"],
                "name": value["name"],
                "small": "Subdept",
                "type": "subdept"
            };
        })
    }

    at_config = {
        at: "@",
        data: atwho_user_list.concat(atwho_dept_list).concat(atwho_subdept_list),
        tpl: "<li data-value='[${name}](${type}#${id} \"${type}#${id}\")'>${name} <small>${small}</small></li>",
        show_the_at: true,
        max_len: 20,
        // callbacks: {
            // before_insert: function(value, $li) {
            //     if (this.$inputor.parent().find(".textarea_atwho_list[value='" + value + "']").length == 0) {
            //         this.$inputor.after("<input class='textarea_atwho_list' name='atwho_list' value='" + $li.data("small").toLowerCase() + "_" + $li.data("id") + "' type='hidden'/>");
            //     }
            //     return value;
            // },
        // },
    }
    if(contentEditableActive)
        at_config.tpl = "<li data-value='<a href=\""+site_url+"wall/${type}/${id}\" data-notify=\"${type}#${id}\"><img src=\""+site_url+"static/img/neutral.png\" style=\"width:16px;height:16px\">${name}</a><span></span>'>${name} <small>${small}</small></li>"

    all_list = atwho_user_list.concat(atwho_dept_list).concat(atwho_subdept_list)
    $("#topbar_search_input").atwho({
        at: "",
        data: all_list,
        tpl: "<li data-value='${name}' data-id='${id}' data-small='${small}'>${name} <small>${small}</small></li>",
        show_the_at: false,
        callbacks: goto_wall,
    }).atwho({
        at: "u:",
        data: atwho_user_list,
        tpl: "<li data-value='${name}' data-id='${id}' data-small='${small}'>${name} <small>${small}</small></li>",
        show_the_at: false,
        callbacks: goto_wall,
    }).atwho({
        at: "d:",
        data: atwho_dept_list,
        tpl: "<li data-value='${name}' data-id='${id}' data-small='${small}'>${name} <small>${small}</small></li>",
        show_the_at: false,
        callbacks: goto_wall,
    }).atwho({
        at: "s:",
        data: atwho_subdept_list,
        tpl: "<li data-value='${name}' data-id='${id}' data-small='${small}'>${name} <small>${small}</small></li>",
        show_the_at: false,
        callbacks: goto_wall,
    })  

    

    // emoticon_config = {
    //   at: ":",
    //   data: $.map(emojis, function(value, i) {return {name: i, symbol:value}}),
    //   tpl:"<li data-value='${symbol}'><i class='icon-${name}'></i> &nbsp; ${name} </li>",
    // }

    $(".atwho_at_config").atwho(at_config)
    // if ( emoticon_config )
    //     $(".atwho_at_config").atwho(emoticon_config);

    for (var i in all_list) {
        $(".select_all_list").append(
            "<option value='" + all_list[i]['small'] + "_" + all_list[i]['id'] + "'>" +
            all_list[i]['name'] +
            "</option>")
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
                        console.log(".." + data["fbid"] + "..")
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

	        console.log(v);
	        if ( service == "youtube" ) {
	            var url = "http://gdata.youtube.com/feeds/api/videos/" + id + "?v=2&alt=jsonc";
	            console.log("TRY UTUBE");
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

