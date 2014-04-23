all_list = []
function setup_autocomplete_lists() {
    goto_wall = {
        before_insert: function(value, $li) {
            console.log($li)
            owner_type = "user"
            if ( $li.data("small") == "Department" ) {
                owner_type = "dept"
            } else if ( $li.data("small") == "Subdept" ) {
                owner_type = "subdept"
            }
            document.location.href="/wall/" + owner_type + "/" + $li.data("id")
            console.log("/wall/" + owner_type + $li.data("id"))
            return value;
        },
    }

    if ( atwho_user_list ) {
        atwho_user_list = $.map(atwho_user_list, function(value, i) {
            return {"id" : value["id"], 
                "name" : value["first_name"] + "_" + value["last_name"], 
                "small" : value["email"]
            };
        })
    }
    if ( atwho_dept_list ) {
        atwho_dept_list = $.map(atwho_dept_list, function(value, i) {
            return {"id" : value["id"], 
                "name" : value["name"], 
                "small":"Department"
            };
        })
    }
    if ( atwho_subdept_list ) {
        atwho_subdept_list = $.map(atwho_subdept_list, function(value, i) {
            return {"id" : value["id"], 
                "name" : value["name"], 
                "small" : "Subdept"
            };
        })
    }   

    at_config = {
        at: "@",
        data: atwho_user_list.concat(atwho_dept_list).concat(atwho_subdept_list),
        tpl: "<li data-value='@${name}' data-id='${id}' data-small='${small}'>${name} <small>${small}</small></li>",
        show_the_at: true,
        callbacks: {
            before_insert: function(value, $li) {
                console.log($li)
                if ( this.$inputor.parent().find(".textarea_atwho_list[value='" + value + "']").length == 0 ) {
                    this.$inputor.after("<input class='textarea_atwho_list' name='atwho_list' value='" + $li.data("small").toLowerCase() + "_" + $li.data("id") + "' type='hidden'/>")
                }
                return value;
            },
        },
    }
    all_list = atwho_user_list.concat(atwho_dept_list).concat(atwho_subdept_list)
    $("#topbar_search_input").atwho({
        at: "",
        data: all_list,
        tpl: "<li data-value='${name}' data-id='${id}' data-small='${small}'>${name} <small>${small}</small></li>",
        show_the_at: false,
        callbacks : goto_wall,
    }).atwho({
        at: "u:",
        data: atwho_user_list,
        tpl: "<li data-value='${name}' data-id='${id}' data-small='${small}'>${name} <small>${small}</small></li>",
        show_the_at: false,
        callbacks : goto_wall,
    }).atwho({
        at: "d:",
        data: atwho_dept_list,
        tpl: "<li data-value='${name}' data-id='${id}' data-small='${small}'>${name} <small>${small}</small></li>",
        show_the_at: false,
        callbacks : goto_wall,
    }).atwho({
        at: "s:",
        data: atwho_subdept_list,
        tpl: "<li data-value='${name}' data-id='${id}' data-small='${small}'>${name} <small>${small}</small></li>",
        show_the_at: false,
        callbacks : goto_wall,
    })

    $(".atwho_at_config").atwho(at_config) 

    for ( var i in all_list ) {
        $(".select_all_list").append(
                "<option value='" + all_list[i]['small'] + "_" + all_list[i]['id'] + "'>" + 
                all_list[i]['name'] + 
                "</option>")
    }

}

function sync_autocomplete() {
    if ( atwho_user_list && atwho_subdept_list && atwho_dept_list ) {
        setup_autocomplete_lists();
    }
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

