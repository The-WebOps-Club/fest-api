all_list = []
atwho_user_list = [];
atwho_subdept_list = [];
atwho_dept_list = [];
atwho_file_list = [];
atwho_file_list_raw = [];
var emoticons = {
    "like" : [],
    "colonthree" : [ ":3", ":-3" ],
    "cry" : [ ":'(", ":'-(", ";(", ";-(" ],
    "frown" : [ ":(", ":-(", ":C", ":c", ":[", ":-[" ], 
    "gasp" : [":o", ],
    "grin" : [ ":D", ":-D", "XD", "X-D", "=D", "xD" ], 
    "grumpy" : [":S", ":-S"], 
    "heart" : ["<3"],
    "kiki" : ["^_^"],
    "kiss" : [":*", ":-*"],
    "pacman" : [],
    "smile" : [ ":)", ":-)", ":]", "=)", "=]", ":}" ], 
    "sunglasses" : ["B)", "B-)"],
    "tongue" : [":P", ":-P", "XP", "X-P", "xP", "xp", ":p", ":-p"],
    "unsure" : [],
    "wink" : [";)", ";-)", "^_-", ";D", ";-D", ";]", ";-]"],
    "angel" : ["O:)", "O:-)", "o:-)", "o:)", "0:)", "0:-)"],
    "surprised" : ["0_0", "o.o", "o.O", "O.o", "O.O", "o_o", "o_O", "O_o", "O_O", "0.0", "0_0"],
    "devil" : ["}:)", "}:-)", "3:)", "3:-)"],
    "glasses" : [""],
    "penguin" : [],
    "poop" : [],
    "teeth" : [],
    "tears-of-joy" : [],
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
        tpl: "<li data-value=':${name}' data-filename='${name}' data-id='${id}' data-small='${small}' data-icon='${iconlink}'><img src='${iconlink}' style='height:12px'> &nbsp; ${name} <small>${small}</small></li>",
        show_the_at: true,
        callbacks: {
            remote_filter: function(query, callback) {
                callback([{
                    "id": "",
                    "name": "",
                    "small": "Loading ...",
                    "iconlink": "/static/img/loading-dice.gif",
                }]);
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
                            "iconlink": "/static/img/loading-dice.gif",
                        }]);
                    }
                }
            },
            before_insert: function(value, $li) {
                if (this.$inputor.parent().find(".textarea_atwho_list[value='" + value + "']").length == 0) {
                    this.$inputor.after("<input class='textarea_atwho_list' name='atwho_files' value='" + $li.data("filename") + "--@@!@@--" + $li.data("id") + "--@@!@@--" + $li.data("icon") + "' type='hidden'/>");
                }
                return value;
            },
        },
    }
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
                    "small": value["email"]
                };
        })
    }
    if (atwho_dept_list) {
        atwho_dept_list = $.map(atwho_dept_list, function(value, i) {
            return {
                "id": value["id"],
                "name": value["name"],
                "small": "Department"
            };
        })
    }
    if (atwho_subdept_list) {
        atwho_subdept_list = $.map(atwho_subdept_list, function(value, i) {
            return {
                "id": value["id"],
                "name": value["name"],
                "small": "Subdept"
            };
        })
    }

    at_config = {
        at: "@",
        data: atwho_user_list.concat(atwho_dept_list).concat(atwho_subdept_list),
        tpl: "<li data-value='@${name}' data-id='${id}' data-small='${small}'>${name} <small>${small}</small></li>",
        show_the_at: true,
        max_len: 20,
        callbacks: {
            before_insert: function(value, $li) {
                console.log($li);
                console.log(value);
                if (this.$inputor.parent().find(".textarea_atwho_list[value='" + value + "']").length == 0) {
                    this.$inputor.after("<input class='textarea_atwho_list' name='atwho_list' value='" + $li.data("small").toLowerCase() + "_" + $li.data("id") + "' type='hidden'/>");
                }
                console.log($li);
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
    if ( emoticon_config )
        $(".atwho_at_config").atwho(emoticon_config);

    for (var i in all_list) {
        $(".select_all_list").append(
            "<option value='" + all_list[i]['small'] + "_" + all_list[i]['id'] + "'>" +
            all_list[i]['name'] +
            "</option>")
    }
    $(".right_search .searchbar input").keyup()
}



(function($){
    $.fn.emoticon = function(els){
        // NEED TO WRITE CODE TO FIND AND REPLACE EMOTES

        this.each(function(){
            $.each(emoticons, function(i, v) {
                console.log(v)
                v.join("|")
                init_string = $(this).html

                var regex = new RegExp("")
            })
        })

        var symbols = '\\+1|-1|100|109|1234|8ball|a|ab|abc|abcd|accept|aerial_tramway|airplane|alarm_clock|alien|ambulance|anchor|angel|anger|angry|anguished|ant|apple|aquarius|aries|arrow_backward|arrow_double_down|arrow_double_up|arrow_down|arrow_down_small|arrow_forward|arrow_heading_down|arrow_heading_up|arrow_left|arrow_lower_left|arrow_lower_right|arrow_right|arrow_right_hook|arrow_up|arrow_up_down|arrow_up_small|arrow_upper_left|arrow_upper_right|arrows_clockwise|arrows_counterclockwise|art|articulated_lorry|astonished|atm|b|baby|baby_bottle|baby_chick|baby_symbol|baggage_claim|balloon|ballot_box_with_check|bamboo|banana|bangbang|bank|bar_chart|barber|baseball|basketball|bath|bathtub|battery|bear|bee|beer|beers|beetle|beginner|bell|bento|bicyclist|bike|bikini|bird|birthday|black_circle|black_joker|black_nib|black_square|black_square_button|blossom|blowfish|blue_book|blue_car|blue_heart|blush|boar|boat|bomb|book|bookmark|bookmark_tabs|books|boom|boot|bouquet|bow|bowling|bowtie|boy|bread|bride_with_veil|bridge_at_night|briefcase|broken_heart|bug|bulb|bullettrain_front|bullettrain_side|bus|busstop|bust_in_silhouette|busts_in_silhouette|cactus|cake|calendar|calling|camel|camera|cancer|candy|capital_abcd|capricorn|car|card_index|carousel_horse|cat|cat2|cd|chart|chart_with_downwards_trend|chart_with_upwards_trend|checkered_flag|cherries|cherry_blossom|chestnut|chicken|children_crossing|chocolate_bar|christmas_tree|church|cinema|circus_tent|city_sunrise|city_sunset|cl|clap|clapper|clipboard|clock1|clock10|clock1030|clock11|clock1130|clock12|clock1230|clock130|clock2|clock230|clock3|clock330|clock4|clock430|clock5|clock530|clock6|clock630|clock7|clock730|clock8|clock830|clock9|clock930|closed_book|closed_lock_with_key|closed_umbrella|cloud|clubs|cn|cocktail|coffee|cold_sweat|collision|computer|confetti_ball|confounded|confused|congratulations|construction|construction_worker|convenience_store|cookie|cool|cop|copyright|corn|couple|couple_with_heart|couplekiss|cow|cow2|credit_card|crocodile|crossed_flags|crown|cry|crying_cat_face|crystal_ball|cupid|curly_loop|currency_exchange|curry|custard|customs|cyclone|dancer|dancers|dango|dart|dash|date|de|deciduous_tree|department_store|diamond_shape_with_a_dot_inside|diamonds|disappointed|dizzy|dizzy_face|do_not_litter|dog|dog2|dollar|dolls|dolphin|door|doughnut|dragon|dragon_face|dress|dromedary_camel|droplet|dvd|e-mail|ear|ear_of_rice|earth_africa|earth_americas|earth_asia|egg|eggplant|eight|eight_pointed_black_star|eight_spoked_asterisk|electric_plug|elephant|email|end|envelope|es|euro|european_castle|european_post_office|evergreen_tree|exclamation|expressionless|eyeglasses|eyes|facepunch|factory|fallen_leaf|family|fast_forward|fax|fearful|feelsgood|feet|ferris_wheel|file_folder|finnadie|fire|fire_engine|fireworks|first_quarter_moon|first_quarter_moon_with_face|fish|fish_cake|fishing_pole_and_fish|fist|five|flags|flashlight|floppy_disk|flower_playing_cards|flushed|foggy|football|fork_and_knife|fountain|four|four_leaf_clover|fr|free|fried_shrimp|fries|frog|frowning|fuelpump|full_moon|full_moon_with_face|game_die|gb|gem|gemini|ghost|gift|gift_heart|girl|globe_with_meridians|goat|goberserk|godmode|golf|grapes|green_apple|green_book|green_heart|grey_exclamation|grey_question|grimacing|grin|grinning|guardsman|guitar|gun|haircut|hamburger|hammer|hamster|hand|handbag|hankey|hash|hatched_chick|hatching_chick|headphones|hear_no_evil|heart|heart_decoration|heart_eyes|heart_eyes_cat|heartbeat|heartpulse|hearts|heavy_check_mark|heavy_division_sign|heavy_dollar_sign|heavy_exclamation_mark|heavy_minus_sign|heavy_multiplication_x|heavy_plus_sign|helicopter|herb|hibiscus|high_brightness|high_heel|hocho|honey_pot|honeybee|horse|horse_racing|hospital|hotel|hotsprings|hourglass|hourglass_flowing_sand|house|house_with_garden|hurtrealbad|hushed|ice_cream|icecream|id|ideograph_advantage|imp|inbox_tray|incoming_envelope|information_desk_person|information_source|innocent|interrobang|iphone|it|izakaya_lantern|jack_o_lantern|japan|japanese_castle|japanese_goblin|japanese_ogre|jeans|joy|joy_cat|jp|key|keycap_ten|kimono|kiss|kissing|kissing_cat|kissing_closed_eyes|kissing_face|kissing_heart|kissing_smiling_eyes|koala|koko|kr|large_blue_circle|large_blue_diamond|large_orange_diamond|last_quarter_moon|last_quarter_moon_with_face|laughing|leaves|ledger|left_luggage|left_right_arrow|leftwards_arrow_with_hook|lemon|leo|leopard|libra|light_rail|link|lips|lipstick|lock|lock_with_ink_pen|lollipop|loop|loudspeaker|love_hotel|love_letter|low_brightness|m|mag|mag_right|mahjong|mailbox|mailbox_closed|mailbox_with_mail|mailbox_with_no_mail|man|man_with_gua_pi_mao|man_with_turban|mans_shoe|maple_leaf|mask|massage|meat_on_bone|mega|melon|memo|mens|metal|metro|microphone|microscope|milky_way|minibus|minidisc|mobile_phone_off|money_with_wings|moneybag|monkey|monkey_face|monorail|moon|mortar_board|mount_fuji|mountain_bicyclist|mountain_cableway|mountain_railway|mouse|mouse2|movie_camera|moyai|muscle|mushroom|musical_keyboard|musical_note|musical_score|mute|nail_care|name_badge|neckbeard|necktie|negative_squared_cross_mark|neutral_face|new|new_moon|new_moon_with_face|newspaper|ng|nine|no_bell|no_bicycles|no_entry|no_entry_sign|no_good|no_mobile_phones|no_mouth|no_pedestrians|no_smoking|non-potable_water|nose|notebook|notebook_with_decorative_cover|notes|nut_and_bolt|o|o2|ocean|octocat|octopus|oden|office|ok|ok_hand|ok_woman|older_man|older_woman|on|oncoming_automobile|oncoming_bus|oncoming_police_car|oncoming_taxi|one|open_file_folder|open_hands|open_mouth|ophiuchus|orange_book|outbox_tray|ox|page_facing_up|page_with_curl|pager|palm_tree|panda_face|paperclip|parking|part_alternation_mark|partly_sunny|passport_control|paw_prints|peach|pear|pencil|pencil2|penguin|pensive|performing_arts|persevere|person_frowning|person_with_blond_hair|person_with_pouting_face|phone|pig|pig2|pig_nose|pill|pineapple|pisces|pizza|plus1|point_down|point_left|point_right|point_up|point_up_2|police_car|poodle|poop|post_office|postal_horn|postbox|potable_water|pouch|poultry_leg|pound|pouting_cat|pray|princess|punch|purple_heart|purse|pushpin|put_litter_in_its_place|question|rabbit|rabbit2|racehorse|radio|radio_button|rage|rage1|rage2|rage3|rage4|railway_car|rainbow|raised_hand|raised_hands|ram|ramen|rat|recycle|red_car|red_circle|registered|relaxed|relieved|repeat|repeat_one|restroom|revolving_hearts|rewind|ribbon|rice|rice_ball|rice_cracker|rice_scene|ring|rocket|roller_coaster|rooster|rose|rotating_light|round_pushpin|rowboat|ru|rugby_football|runner|running|running_shirt_with_sash|sa|sagittarius|sailboat|sake|sandal|santa|satellite|satisfied|saxophone|school|school_satchel|scissors|scorpius|scream|scream_cat|scroll|seat|secret|see_no_evil|seedling|seven|shaved_ice|sheep|shell|ship|shipit|shirt|shit|shoe|shower|signal_strength|six|six_pointed_star|ski|skull|sleeping|sleepy|slot_machine|small_blue_diamond|small_orange_diamond|small_red_triangle|small_red_triangle_down|smile|smile_cat|smiley|smiley_cat|smiling_imp|smirk|smirk_cat|smoking|snail|snake|snowboarder|snowflake|snowman|sob|soccer|soon|sos|sound|space_invader|spades|spaghetti|sparkler|sparkles|sparkling_heart|speak_no_evil|speaker|speech_balloon|speedboat|squirrel|star|star2|stars|station|statue_of_liberty|steam_locomotive|stew|straight_ruler|strawberry|stuck_out_tongue|stuck_out_tongue_closed_eyes|stuck_out_tongue_winking_eye|sun_with_face|sunflower|sunglasses|sunny|sunrise|sunrise_over_mountains|surfer|sushi|suspect|suspension_railway|sweat|sweat_drops|sweat_smile|sweet_potato|swimmer|symbols|syringe|tada|tanabata_tree|tangerine|taurus|taxi|tea|telephone|telephone_receiver|telescope|tennis|tent|thought_balloon|three|thumbsdown|thumbsup|ticket|tiger|tiger2|tired_face|tm|toilet|tokyo_tower|tomato|tongue|top|tophat|tractor|traffic_light|train|train2|tram|triangular_flag_on_post|triangular_ruler|trident|triumph|trolleybus|trollface|trophy|tropical_drink|tropical_fish|truck|trumpet|tshirt|tulip|turtle|tv|twisted_rightwards_arrows|two|two_hearts|two_men_holding_hands|two_women_holding_hands|u5272|u5408|u55b6|u6307|u6708|u6709|u6e80|u7121|u7533|u7981|u7a7a|uk|umbrella|unamused|underage|unlock|up|us|v|vertical_traffic_light|vhs|vibration_mode|video_camera|video_game|violin|virgo|volcano|vs|walking|waning_crescent_moon|waning_gibbous_moon|warning|watch|water_buffalo|watermelon|wave|wavy_dash|waxing_crescent_moon|waxing_gibbous_moon|wc|weary|wedding|whale|whale2|wheelchair|white_check_mark|white_circle|white_flower|white_square|white_square_button|wind_chime|wine_glass|wink|wink2|wolf|woman|womans_clothes|womans_hat|womens|worried|wrench|x|yellow_heart|yen|yum|zap|zero|zzz';

        //var keys = '\\' + emojis.join("|")
    
        return 
            var regex = new RegExp(':(' + keys + '):', 'g');
            $(this).html($(this).html().replace(regex, $.fn.emoji.replace));
        });
    };

    $.fn.emoticon.replace = function(name){
        return '<i class="icon-' + name + '"></i>';
    };
})(jQuery);

