

var FileMetaCache = function(){
	self = this;
	// set files variable to null
	self.files = null;
	self.lastUpdated = null;
	self.fileIds = null;

	self.prototype.initCache = function(){
		if(localStorage.files != undefined)
			self.files = localStorage.files;
			self.fileIds = localStorage.fileIds;
			self.lastUpdated = localStorage.lastUpdated;
		else
			self.files = [];
			self.lastUpdated = null;
			self.fileIds = [];
	}

	// cache files using the date parameter
	self.prototype.cacheFiles = function( datetime ){
		localStorage.files = self.files;
		localStorage.fileIds = self.fileIds;
		localStorage.lastUpdated = datetime;
	}

	self.prototype.syncFiles = function(){
		self.files = localStorage.files;
		self.fileIds = localStorage.fileIds;
		self.lastUpdated = localStorage.lastUpdated;
	}

	self.prototype.pushFiles = function( fileList ){
		fileList.forEach(function(e){
			if(self.fileIds.contains(e.id)){
				self.files[self.fileIds.indexOf(e.id)] = e;
			}
			else{
				self.files.push(e);
				self.fileIds.push(e.id);
			}
		});
	}
	self.prototype.getCacheDate = function(){
		return localStorage.lastUpdated;
	}

}

var DriveFileRetreival = function(){
	self = this;
	self.cache = FileMetaCache();
	self.prototype.init = function(){
		self.cache.initCache();
	}
	self.prototype.loadByDir = function( folderId, callback, datetime ){
		if(!self.cache.lastUpdated)
			q = 'modifiedDate >= \''+self.cache.lastUpdated+'\'';
		else
			q=null;

		gapi.client.drive.children.list({
            "folderId": folderId,
            "q":q,
        }).execute(function(response) {
            self.cache.pushFiles( response.items );
            self.cache.cacheFiles( datetime );
            callback( response );
        });
	}
	self.prototype.loadAllBG = function( callbacks, stepSize ){
		var numFilesLoaded = 0;
		gapi.client.drive.files.list({
            "maxResults":stepSize,
        }).execute(function loadNext( response ) {
            self.cache.pushFiles( response.items );
            
            if( response.items )
            	numFilesLoaded += response.items.length;
            	callbacks['progress'](numFilesLoaded);

            if( response.pageToken ){
            	gapi.client.drive.files.list({
            	"pageToken":response.pageToken,
            	}).execute(loadNext);
            	
            }else{
            	self.cache.cacheFiles( callbacks['datetime']() );
            	callbacks['finish']();
            }

        });

	}
	self.prototype.loadChangesBG = function( callback ){
		q = 'modifiedDate >= \''+self.cache.lastUpdated+'\'';
		gapi.client.drive.files.list({
            "q":q,
        }).execute(function(response) {
            self.cache.pushFiles( response.items );
            self.cache.cacheFiles( datetime );
        });
	}

}