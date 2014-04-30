var defaults = {
    "authToken": null,
    "developerKey": null,
    "rootFolder": null,
    "fileAddCallback": function(el) {},
},
MIME_TYPES = {
	"audio" : "application/vnd.google-apps.audio",
	"doc" : "application/vnd.google-apps.document",
	"drawing" : "application/vnd.google-apps.drawing",
	"file" : "application/vnd.google-apps.file",
	"folder" : "application/vnd.google-apps.folder",
	"form" : "application/vnd.google-apps.form",
	"fusion_table" : "application/vnd.google-apps.fusiontable",
	"photo" : "application/vnd.google-apps.photo",
	"slide" : "application/vnd.google-apps.presentation",
	"app_script" : "application/vnd.google-apps.script",
	"site" : "application/vnd.google-apps.sites",
	"sheet" : "application/vnd.google-apps.spreadsheet",
	"unknown" : "application/vnd.google-apps.unknown",
	"video" : "application/vnd.google-apps.video",
},STANDARD_META_LIST = 	[ "id", "title", "modifiedDate", 	// to allow other modules to take advantage of the drive function.
        "mimeType", "lastModifyingUser",
        "thumbnail", "thumbnailLink", "iconLink"
]


var Drive = function(options) {

	self = this // To use in callback functions to avoid this confusion

    self.options = $.extend({}, defaults, options || {});
    self.dir_contents = null
    self.finish_progress = 1
    self.current_progress = 0

    self.init = function() {
        console.log("Init Drive")
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
            if ( response.items.length ) {
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
            "fields": [ "id", "title", ],
        }).execute(function(response) {
            self.check_error(response)
            self.set_drive_parent(response)
        });
    }
    
    self.get_file_meta = function(fid, callback ) {
        gapi.client.drive.files.get({
            "fileId": fid,
            "fields": STANDARD_META_LIST ,
        }).execute(function(response) {
            self.check_error(response)
            self.current_progress += 1
            self.progress()
            callback = callback || self.show_file
            callback(response);
            f = response
        });
    }
    self.rename_files = function(file_details, callback) {
    	$.each(file_details, function(i,v) {
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
    	$.each(file_details, function(i,v) {
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
                gapi.client.drive.parents.delete({
                    'fileId': v.id,
                    'parentId': v.old_parent_id,
                }).execute(function(response) {
                    self.check_error(response)
                    callback = callback || self.get_dir_contents
                    callback();
                    self.current_progress += 1;
                    self.progress()
                    $(".drive_move").prop("disabled", false).removeClass("disabled")
                });
                self.check_error(response)
                self.current_progress += 1;
                self.progress()
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
            callback = callback || function(file) { console.log(file) };
            request.execute(function(file) { self.progress("100"); callback(file) });
        }
    }

    self.upload_file_resumable = function(fileData, dir_id, callback) {
        var reader = new FileReader();
        reader.readAsBinaryString(fileData);
        // NOTE : Currently it creates a broken file in no parent. UNUSABLE RIGHT NOW
        reader.onload = function(e) {
            
            gapi.client.request({
                'path': '/upload/drive/v2/files',
                'method': 'POST',
                'params': {
                    'uploadType': 'resumable'
                },
                'headers': {
                    'X-Upload-Content-Type': fileData.type
                },
                'body': {       
                    "title": fileData.name, 
                    "mimeType": fileData.type,
                    "Content-Lenght": fileData.size,
                }
            }).execute( function (response, raw_response) {
                raw_response = JSON.parse(raw_response)

                self.uploading_file_token = GetURLParameter(raw_response.gapi.data.headers.location, "upload_id")

                gapi.client.request({
                    'path': '/upload/drive/v2/files',
                    'method': 'PUT',
                    'params': {
                        'uploadType': 'resumable',
                        'upload_id': self.uploading_file_token,
                    },
                    'headers': {
                        'Content-Length': fileData.size,
                        'Content-Type': fileData.type
                    },
                    'body': reader.result
                });
            })
        }
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
    
}

function GetURLParameter(sURL, sParam) {
    var sPageURL = sURL.split("?")[1];
    var sURLVariables = sPageURL.split('&');
    for (var i = 0; i < sURLVariables.length; i++) 
    {
        var sParameterName = sURLVariables[i].split('=');
        if (sParameterName[0] == sParam) 
        {
            return sParameterName[1];
        }
    }
}​