/*
*	FEST API background cache system.
*	Currently operates off a hard cache and a soft cache.
*	the hard cache auto loads files on the background and stores them on the local machine thus reducing the load times.
*	the soft cache stores search results on global vars in order mimic a decent amount of common sense. Does NOT store data on the client machine.
*/

var FileMetaCache = function(){
	self = this;
	// set variables to null
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
			if( self.fileIds.indexOf(e.id) == -1 ){
				self.files[ self.fileIds.indexOf( e.id) ] = e;
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
			q = 'modifiedDate >= \''+self.cache.lastUpdated.toISOString()+'\'';
		else
			q=null;

		gapi.client.drive.children.list({
            "folderId": folderId,
            "q":q,
        }).execute(function(response) {

            self.cache.pushFiles( response.items );
            self.cache.cacheFiles( datetime );

            var cachedFiles = [];
            self.cache.files.forEach(function(item){
            	if( item.parents[0].id == folderId ) 
            		cachedFiles.push( item );
            });

            callback( response.items.concat( cachedFiles ) );

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
	self.prototype.loadChangesBG = function( callback, datetime ){

		q = 'modifiedDate >= \''+self.cache.lastUpdated.toISOString()+'\'';

		gapi.client.drive.files.list({
            "q":q,
        }).execute(function(response) {
            self.cache.pushFiles( response.items );	// store on 'floating' list.
            self.cache.cacheFiles( datetime );	// cache to local machine with a timestamp.
        });

	}
}