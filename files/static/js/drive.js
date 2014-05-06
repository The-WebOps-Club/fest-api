var defaults = {
    "authToken": null,
    "developerKey": null,
    "rootFolder": null,
    "fest_name": null,
    "fileAddCallback": function(el) {},
},
    MIME_TYPES = {
        "audio": "application/vnd.google-apps.audio",
        "doc": "application/vnd.google-apps.document",
        "drawing": "application/vnd.google-apps.drawing",
        "file": "application/vnd.google-apps.file",
        "folder": "application/vnd.google-apps.folder",
        "form": "application/vnd.google-apps.form",
        "fusion_table": "application/vnd.google-apps.fusiontable",
        "photo": "application/vnd.google-apps.photo",
        "slide": "application/vnd.google-apps.presentation",
        "app_script": "application/vnd.google-apps.script",
        "site": "application/vnd.google-apps.sites",
        "sheet": "application/vnd.google-apps.spreadsheet",
        "unknown": "application/vnd.google-apps.unknown",
        "video": "application/vnd.google-apps.video",
    }, STANDARD_META_LIST = ["id", "title", "modifiedDate", // to allow other modules to take advantage of the drive function.
        "mimeType", "lastModifyingUser",
        "thumbnail", "thumbnailLink", "iconLink"
    ]


var Drive = function(options) {

    self = this // To use in callback functions to avoid this confusion

    self.chunkSize = 262144 // Has to be multiple of 262144
    self.options = $.extend({}, defaults, options || {});
    self.dir_contents = null
    self.finish_progress = 1
    self.current_progress = 0

    self.init = function() {
        if (!self.options.authToken || !self.options.developerKey) {
            console.log("Auth token, DeveloperKey was invalid")
            return
        }

        gapi.auth.setToken({
            access_token: self.options.authToken,
            expires_in: 2000
        }); // set the access token obtained from the server. OAuth2 automatically logs us in.

        gapi.client.setApiKey(this.options.developerKey); //set our public api key
        gapi.client.load('drive', 'v2', self.gapi_drive_callback); // ask gapi to load API details for the drive api.
    }

    self.check_error = function(r) {
        if (r.error) {
            if (r.error.code == 401)
                alert('ACCESS TOKEN expired. Please refresh the page.');
            else if (r.error.code == 400) // comes while uploading files....
                return
            else
                alert('Unexpected error: ' + r.error.code);
            console.log(r)
        }
    }

    self.gapi_drive_callback = function() {
        // Default action
        self.get_dir_contents()
    }

    self.get_dir_contents = function(fid, callback) {
        fid = fid || $(".drive_parent").data("id") || self.options.rootFolder
        gapi.client.drive.children.list({
            "folderId": fid,
        }).execute(function(response) {
            self.check_error(response)
            self.dir_contents = response.items
            if (response.items.length) {
                self.finish_progress = response.items.length
                self.current_progress = 0
                callback = callback || self.show_dir_contents
            } else {
                callback = callback || self.show_empty_dir
            }
            callback();
        });
        gapi.client.drive.files.get({
            "fileId": fid,
            "fields": ["id", "title", ],
        }).execute(function(response) {
            self.check_error(response)
            self.set_drive_parent(response)
        });
    }

    self.get_file_meta = function(fid, callback) {
        gapi.client.drive.files.get({
            "fileId": fid,
            "fields": STANDARD_META_LIST,
        }).execute(function(response) {
            self.check_error(response)
            self.current_progress += 1
            self.progress()
            callback = callback || self.show_file
            callback(response);
        });
    }
    self.rename_files = function(file_details, callback) {
        $.each(file_details, function(i, v) {
            gapi.client.drive.files.patch({
                'fileId': v.id,
                'resource': {
                    'title': v.title,
                },
            }).execute(function(resp) {
                self.check_error(response)
                callback = callback || self.get_dir_contents
                callback();
                $(".drive_rename").prop("disabled", false).removeClass("disabled")
            });
        })
    }

    self.delete_files = function(file_details, callback) {
        $.each(file_details, function(i, v) {
            gapi.client.drive.files.trash({
                'fileId': v.id
            }).execute(function(response) {
                self.check_error(response)
                callback = callback || self.get_dir_contents
                callback();
            });
        })
    }

    self.move_files = function(file_details, callback) {
        self.finish_progress = file_details.length * 2
        self.current_progress = 0

        $.each(file_details, function(i, v) {
            gapi.client.drive.parents.insert({
                'fileId': v.id,
                'resource': {
                    'id': v.new_parent_id,
                }
            }).execute(function(response) {
                self.check_error(response)
                self.current_progress += 1;
                self.progress()
                if (v.old_parent_id == "") {
                    gapi.client.drive.parents.delete({
                        'fileId': v.id,
                        'parentId': v.old_parent_id,
                    }).execute(function(response) {
                        self.check_error(response)
                        self.current_progress += 1;
                        self.progress()
                        callback = callback || self.get_dir_contents
                        callback();
                    });
                } else {
                    self.current_progress += 1;
                    self.progress()
                    callback = callback || self.get_dir_contents
                    callback();
                }
            });
        })
    }

    self.upload_file = function(fileData, dir_id, callback) {
        const boundary = '-------314159265358979323846';
        const delimiter = "\r\n--" + boundary + "\r\n";
        const close_delim = "\r\n--" + boundary + "--";

        self.progress("10")
        var reader = new FileReader();
        reader.readAsBinaryString(fileData);
        reader.onload = function(e) {
            self.progress("20")
            var contentType = fileData.type || 'application/octet-stream';
            var metadata = {
                'title': fileData.name,
                'mimeType': contentType,
                'parents': [{
                    'id': dir_id,
                    'kind': 'drive#parentReference'
                }]
            };

            var base64Data = btoa(reader.result);
            var multipartRequestBody =
                delimiter +
                'Content-Type: application/json\r\n\r\n' +
                JSON.stringify(metadata) +
                delimiter +
                'Content-Type: ' + contentType + '\r\n' +
                'Content-Transfer-Encoding: base64\r\n' +
                '\r\n' +
                base64Data +
                close_delim;
            self.progress("25")
            var request = gapi.client.request({
                'path': '/upload/drive/v2/files',
                'method': 'POST',
                'params': {
                    'uploadType': 'multipart'
                },
                'headers': {
                    'Content-Type': 'multipart/mixed; boundary="' + boundary + '"'
                },
                'body': multipartRequestBody
            });
            callback = callback || function(){}
            request.execute(function(file) {
                self.progress("100");
                callback(file)
            });
        }
    }

    self.upload_file_resumable = function(fileData, dir_id, callback) {

        self.finish_progress = Math.ceil(fileData.size / self.chunkSize) + 3
        self.current_progress = 1
        self.progress()
        
        file = fileData

        if (!fileData.type)
            fileData.type = 'application/octet-stream';

        var metadata = {
            'title': fileData.name,
            'mimeType': fileData.type
        };

        var url = 'https://www.googleapis.com/upload/drive/v2/files/?uploadType=resumable';

        xhr = new XMLHttpRequest();

        xhr.open("POST", url, true);
        xhr.setRequestHeader('Authorization', 'Bearer ' + self.options.authToken);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.setRequestHeader('X-Upload-Content-Length', fileData.size);
        xhr.setRequestHeader('X-Upload-Content-Type', fileData.type);
        xhr.onreadystatechange = function(e) {
            self.current_progress += 1
            self.progress();
            self.upload_file_resumable_part(
                e.target.getResponseHeader('Location'), fileData,
                0, dir_id, callback)
        }
        xhr.send(JSON.stringify(metadata));
    }

    self.upload_file_resumable_part = function(location, fileData, offset, dir_id, callback) {
        url = location;
        console.log("sending part ....")

        var content = fileData;
        var end = fileData.size;
        var chunkSize = self.chunkSize

        if (offset || chunkSize) {
            if (chunkSize) {
                end = Math.min(offset + chunkSize, fileData.size);
            }
            content = content.slice(offset, end);
        }

        var xhr = new XMLHttpRequest();
        xhr.open('PUT', url, true);
        xhr.setRequestHeader('Content-Type', fileData.type);
        //xhr.setRequestHeader('Content-Range', "bytes " + offset + "-" + (end - 1) + "/" + fileData.size);
        //xhr.setRequestHeader('X-Upload-Content-Type', fileData.type);
        xhr.onreadystatechange = function(e) {
            self.current_progress += 1
            self.progress();
            f = e;
            console.log(e.target.responseText)
            //console.log(self.current_progress)
            if (end == fileData.size) { // done
                var this_file = JSON.parse(e.target.responseText)
                self.move_files([{
                    "id": this_file.id,
                    "new_parent_id": dir_id,
                    "old_parent_id": "",
                }], callback(e));
            } else { // incomplete
                self.upload_file_resumable_part(location, fileData, end, dir_id, callback)
            }
        };
        xhr.send(content);
    }
    /* ------------------------ DISPLAY FUNCTIONS ------------------ */
    self.show_dir_contents = function(folder_items, clear) {
        clear = clear || true
        folder_items = folder_items || self.dir_contents
        if (clear) {
            $(".drive_file").not(".template").remove()
            $(".empty_dir").hide()
        }
        $.each(folder_items, function(i, v) {
            self.get_file_meta(v.id)
        })
        $(".drive_refresh").prop("disabled", false).removeClass("disabled")
        $(".drive_back").prop("disabled", false).removeClass("disabled")
        self.progress()
    }
    self.show_empty_dir = function(folder_items, clear) {
        $(".empty_dir").show()
        $(".drive_refresh").prop("disabled", false).removeClass("disabled")
        $(".drive_back").prop("disabled", false).removeClass("disabled")
    }

    self.show_file = function(file_data, clear) {
        clear = clear || true
        if (clear) {
            $.each($(".drive_file").not(".template"), function(v, i) {
                var $v = $(v)
                if ($v.data("id") == file_data.id)
                    $v.remove()
            })
        }
        if (file_data.labels.trashed) { // dont make the file
            return
        }
        $el = $(".drive_list .drive_parent .template.file_template").clone()
            .removeClass("template").removeClass("file_template")
        $el.data("id", file_data.id)
        $el.find(".title").text(file_data.title)
        if (!file_data.labels.viewed) {
            //$el.find(".title").addClass("bold") // This viewswed is for fest-api acct. Not other junta
        } else if (file_data.labels.trashed) {
            $el.find(".title").addClass("strike")
            $el.find(".title").prepend("<i class='icon-trash drive_icon'></i>")
        }
        $el.find(".drive_icon").prop("src", file_data.iconLink)
        if (moment)
            last_mod = moment.duration(moment(file_data.modifiedDate) - moment()).humanize(true)
        else
            last_mod = file_data.modifiedDate
        $el.find(".last_modified").text(last_mod)

        if (file_data.mimeType == MIME_TYPES["folder"]) {
            $el.data("folder", "yes")
            $el.find(".info a").prop("href", "javascript:void(0)")
            $el.find(".info a").click(function(e) {
                e.stopPropogation()
                self.get_dir_contents($(this).closest(".drive_file").data("id"))
            })
        } else {
            $el.data("folder", "no")
            $el.find(".info a").prop("href", $el.find(".info a").prop("href") + "?id=" + $el.data("id"))
        }

        self.options.fileAddCallback($el)

        $el.show()
        $(".drive_parent").append($el)
        self.progress()
    }

    self.show_parent = function(fid, num) {
        num = num || 0
        self.get_file_meta(fid, function(r) {
            if (r.parents.length) {
                if (r.parents.length > num + 1)
                    num = 0
                self.get_dir_contents(r.parents[num].id)
            }
        })
    }

    self.progress = function(val) {
        val = val || (self.current_progress / self.finish_progress * 100).toFixed(0);
        val = "" + val
        $(".progress").css({
            "width": val + "%",
        })
        $(".progress_val").text(val + "%")
        if ($.trim(val) == "100") {
            $(".progress").html("&nbsp;&nbsp;&nbsp;&nbsp;DONE LOADING")
            $(".meter").removeClass("animate")
        } else {
            $(".progress").html("&nbsp;&nbsp;&nbsp;&nbsp;LOADING ...")
            $(".meter").addClass("animate")
        }
    }

    self.set_drive_parent = function(file_details) {
        $(".drive_parent_title").text("folder : " + file_details.title)
            .data("folder", "yes").data("id", file_details.id)
        $("title").text(self.options.fest_name + " Docs - " + file_details.title)
        $(".drive_parent").data("id", file_details.id).data("folder", "yes")
        if (file_details.parents && file_details.parents.length)
            $(".drive_back").removeClass("disabled").prop("disabled", false)
                .data("id", file_details.parents[0].id)
        else
            $(".drive_back").addClass("disabled").prop("disabled", true)
    }
    /* Execution */
    self.init()

    return this
}

    function GetURLParameter(sURL, sParam) {
        var sPageURL = sURL.split("?")[1];
        var sURLVariables = sParam.split("&")
        for (var i = 0; i < sURLVariables.length; i++) {
            var sParameterName = sURLVariables[i].split('=');
            if (sParameterName[0] == sParam) {
                return sParameterName[1];
            }
        }
    }
