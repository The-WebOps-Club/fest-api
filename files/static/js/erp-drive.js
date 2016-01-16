var MIME_DIRECTORY = 'application/vnd.google-apps.folder'

function initDrive( authToken, developerKey, expiry, callback) {
    //alert('?');
    gapi.auth.setToken({
        access_token: authToken,
        expires_in: expiry
    }); // set the access token obtained from the server. OAuth2 automatically logs us in.
    gapi.client.setApiKey(developerKey); //set our public api key
    gapi.client.load('drive', 'v2', callback ); // ask gapi to load API details for the drive api.
}

function getFiles( callback ) {
    //alert('retreiving files');
    //files_of_interest = []
    gapi.client.drive.files.list().execute(function(response) {
        if (response.error) {
            if (response.error.code == 401)
                alert('ACCESS TOKEN expired. Please refresh the page. Note that the Token is active only for around 2000 seconds.');
            else
                alert('Unexpected error: ' + response.error.code);
        }
        callback(response.items);
    });

}

function renameFile( fileId, newTitle, callback, error) {
      var body = {'title': newTitle};
      var request = gapi.client.drive.files.patch({
        'fileId': fileId,
        'resource': body
    });
    request.execute( function(resp){
        if( resp.error ){ error(resp); }
        else callback(resp);
    } );
}
    /*
    function(resp) {
        $('#renamebox').css('display', 'none')
        console.log('New Title: ' + resp.title);
        getFiles();
    }
    */

/* NOT IMPLEMENTED DO NOT USE. To be implemented with special templates for presentation and documents. */
function uploadEmptyFile(mimetype, name, dir_id) {
    var text = "";
    var xhr2 = new XMLHttpRequest();
    xhr2.open('POST', 'https://content.googleapis.com/drive/v2/files?key=' + developerKey);
    xhr2.setRequestHeader('Authorization', 'Bearer ' + authToken);
    xhr2.setRequestHeader('Content-Type', 'application/json');
    xhr2.onreadystatechange = function() {
        var xhr = new XMLHttpRequest();
        xhr.open('PUT', 'https://www.googleapis.com/upload/drive/v2/files/' + JSON.parse(xhr2.responseText).id + '?uploadType=media');
        xhr.setRequestHeader('Authorization', 'Bearer ' + authToken);
        xhr.setRequestHeader('Content-Type', mimetype);
        xhr.onreadystatechange = function(res) {
            alert(JSON.stringify(res));
        }
        xhr.send(text);
    }
    xhr2.send(JSON.stringify({
        'title': name,
        'mimeType': mimetype,
        'parents': [{
            'id': dir_id,
            'kind': 'drive#parentReference'
        }]
    }));
}


function uploadEmptyFolder(name, dir_id, callback) {
    var xhr2 = new XMLHttpRequest();
    xhr2.open('POST', 'https://content.googleapis.com/drive/v2/files?key=' + developerKey);
    xhr2.setRequestHeader('Authorization', 'Bearer ' + authToken);
    xhr2.setRequestHeader('Content-Type', 'application/json');
    xhr2.onreadystatechange = callback;
    xhr2.send(JSON.stringify({
        'title': name,
        'mimeType': MIME_DIRECTORY,
        'parents': [{
            'id': dir_id,
            'kind': 'drive#parentReference'
        }]
    }));
}


function insertFile( fileData, dir_id, callback ) {
    const boundary = '-------314159265358979323846';
    const delimiter = "\r\n--" + boundary + "\r\n";
    const close_delim = "\r\n--" + boundary + "--";

    var reader = new FileReader();
    reader.readAsBinaryString(fileData);
    reader.onload = function(e) {
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
        if (!callback) {
            callback = function(file) {
                console.log(file)
            };
        }
        request.execute(callback);
    }
}

// this function can also be used to delete folders.
function deleteFile( fileId, callback ) {
    var request = gapi.client.drive.files.delete({
        'fileId': fileId
    });
    request.execute(callback);
}

// note: accesstype has two possible values : 'reader' and 'writer' ;their meanings are self-implied. 
function shareFile( fileId, dest_email, accesstype, callback ) {
    var body = {
        'value': dest_email,
        'type': 'user',
        'role': accesstype
    };
    var request = gapi.client.drive.permissions.insert({
        'fileId': fileId,
        'resource': body
    });
    request.execute(callback);
}
