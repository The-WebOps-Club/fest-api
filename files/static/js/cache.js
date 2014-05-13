/*
*	FEST API background cache system.
*/
var CACHE_VERSION = "1.1";
var STORAGE_PREFIX = "pre1";

var VirtualStorage = function( contextPrefix ){
	//var obj0 = {};
	this.contexts = localStorage[contextPrefix+'contexts'];
	this.num_contexts = localStorage[contextPrefix+'num_contexts'];
	this.CacheVersion = localStorage[contextPrefix+'CacheVersion'];
	this.update = function(){
		localStorage[contextPrefix+'contexts'] = this.contexts;
		localStorage[contextPrefix+'num_contexts'] = this.num_contexts;
		localStorage[contextPrefix+'CacheVersion'] = this.CacheVersion;
	}
	this.clear = function(){
		localStorage.removeItem(contextPrefix+'contexts');
		localStorage.removeItem(contextPrefix+'num_contexts');
		localStorage.removeItem(contextPrefix+'CacheVersion');
	}
}

var ContextController = function(){

	var cobj = this;	// set local object as cobj.

	this.files = [];
	this.lastUpdated = null;
	this.fileIds = [];
	this.contextType = 'context#unknown'
	this.staticdata = {};
	this.contextNumber = -1;
	this.virtualStorage = new VirtualStorage( STORAGE_PREFIX );

	this.initCache = function( contextNumber, contextType ){
		this.contextNumber = contextNumber;
		var storage = {};
		storage.contexts = []
		storage.num_contexts = 0;
		if(this.virtualStorage.contexts != undefined )
			storage.contexts = JSON.parse(this.virtualStorage.contexts);
		if(this.virtualStorage.num_contexts != undefined )
			storage.num_contexts = parseInt(this.virtualStorage.num_contexts);

		//console.log(storage);
		if(storage.contexts[ contextNumber ] != undefined){
			// TODO at some point.... optimize this code to have a single write and single read.
			this.files = JSON.parse( storage.contexts[this.contextNumber].files );
			this.fileIds = JSON.parse( storage.contexts[this.contextNumber].fileIds );
			this.lastUpdated = new Date( storage.contexts[this.contextNumber].lastUpdated );
			this.contextType = storage.contexts[this.contextNumber].contextType;
			this.staticdata = JSON.parse( storage.contexts[this.contextNumber].staticdata );
		}
		else{
			this.files = [];
			this.lastUpdated = null;
			this.fileIds = [];
			this.contextType = contextType || 'context#unknown'
			this.contextNumber = storage.num_contexts;
			this.staticdata = {changed:true,hits:0};
			storage.num_contexts ++;
			this.virtualStorage.num_contexts = storage.num_contexts.toString();
			this.virtualStorage.update();
		}
	}


	// cache files using the date parameter
	this.cacheFiles = function( datetime ){
		storage = []
		if(this.virtualStorage.contexts !=undefined)
			storage.contexts = JSON.parse(this.virtualStorage.contexts);
		else
			storage.contexts = [];

		if( storage.contexts[this.contextNumber] == undefined ) storage.contexts[this.contextNumber] = {};
		this.lastUpdated = datetime;
		//console.log('caching: '+this.contextNumber);
		storage.contexts[this.contextNumber].files = JSON.stringify(this.files);
		storage.contexts[this.contextNumber].fileIds = JSON.stringify(this.fileIds);
		storage.contexts[this.contextNumber].lastUpdated = datetime.toISOString();
		storage.contexts[this.contextNumber].contextType = this.contextType;
		storage.contexts[this.contextNumber].staticdata = JSON.stringify(this.staticdata)
		this.virtualStorage.contexts = JSON.stringify(storage.contexts);
		this.virtualStorage.update();

	}

	this.pushStatic = function( staticdata ){
		Object.keys(staticdata).forEach(function( item ){
			cobj.staticdata[ item ] = staticdata[ item ];
		});
	}
	this.clearStatic = function( staticdata ){
		cobj.staticdata = {};
	}

	this.syncFiles = function(){
		this.files = JSON.parse( storage.contexts[this.contextNumber].files );
		this.fileIds = JSON.parse( storage.contexts[this.contextNumber].fileIds );
		this.lastUpdated = new Date( storage.contexts[this.contextNumber].lastUpdated );
		this.contextType = storage.contexts[this.contextNumber].contextType;
		this.staticdata = JSON.parse( storage.contexts[this.contextNumber].staticdata );
	}

	this.pushFiles = function( fileList ){
		fileList.forEach(function(e){
			if( cobj.fileIds.indexOf(e.id) != -1 ){
				cobj.files[ cobj.fileIds.indexOf(e.id) ] = e;
			}
			else{
				cobj.files.push(e);
				cobj.fileIds.push(e.id);
			}
		});
	}

}

function validateVirtualCache( storagePrefix ){
	// if cache is non-existent or if the cache format is outdated.. reset the local cache to prevent cache inconsistencies.
	var virtualStorage = new VirtualStorage( storagePrefix );
	console.log(virtualStorage);
	if(virtualStorage.CacheVersion == undefined || virtualStorage.CacheVersion != CACHE_VERSION){
		console.log('invalid cache version');
		virtualStorage.clear();
		virtualStorage.CacheVersion = CACHE_VERSION;
		virtualStorage.num_contexts = 0;

		virtualStorage.update();
	}
}

var FileMetaCache = function(){
	// SINGLETON pattern.
	fmc = this;

	// main var.
	this.controllers = [];

	//util vars holding a mapping for quick access.
	this.byfile = { };
	this.bydir = { };
	this.byall = { };

	this.init = function(){
		//console.log(localStorage.num_contexts);
		var i = 0;
		var max = new VirtualStorage( STORAGE_PREFIX ).num_contexts;
		for( i = 0; i<parseInt(max); i++ ){
			controller = new ContextController( );
			controller.initCache( i );
			//console.log('initialized cache: '+i );
			this.controllers.push( controller );
			if( controller.contextType == 'context#bydir' ) 
				this.bydir[controller.staticdata.dirid] = controller;
			else if( controller.contextType == 'context#byfile' ) {
				this.byfile[controller.fileIds[0]] = controller;
				//console.log('found a file');
			}
			else if( controller.contextType == 'context#byall' ) 
				this.byall['global'] = controller;

			//console.log('created controller for cache: ');
			//console.log(controller);
			//break;
		}
		//console.log('caches obtained: ');
		//console.log(this.controllers);
	}
}

var DriveFileRetreival = function(){

	this.cache = new FileMetaCache();

	this.init = function(){
		validateVirtualCache( STORAGE_PREFIX );
		this.cache.init();
	}

	dfr = this;	// set local context for all functions decalred within this block to prevent confusion. Using self raises some weird issues.

	/*
	*	folderId: ID of the folder to retreive.
	*	callbacks:  
	*		cached: called immediately if cache data exists.
	*		finish: called after changes are retreived from the server.
	*/
	this.loadByDir = function( folderId, callbacks, datetime ){
		var query = {
            "folderId": folderId,
            //"q":'modifiedDate >= \''+new Date(this.cache.lastUpdated).toISOString()+'\''
        };

        var dir_cache = this.cache.bydir[folderId];
        //console.log(this.cache);
		if( dir_cache != undefined ){
			query.q = 'modifiedDate >= \''+new Date(dir_cache.lastUpdated).toISOString()+'\'';
			this.cache.bydir[folderId].staticdata.hits++;
			callbacks['cached']( {items:dir_cache.files} )
		}else{
			var cc = new ContextController();
			cc.initCache( -1, 'context#bydir');
			cc.staticdata.dirid = folderId;
			dfr.cache.bydir[folderId] = cc;
			dfr.cache.controllers.push(cc);
			dir_cache = cc;
		}

		//console.log('QUERYING FOLDER: ');
		//console.log(query);
		gapi.client.drive.children.list(query).execute(function(response) {
			var cachedFiles = dir_cache.files;


			if( response.items == undefined ){
				response.items = cachedFiles;
            	callbacks['finish']( response );
            	return;
			}
			// Possible inconsistency if dir_cache is not accessed by address.
			dfr.cache.bydir[folderId].pushFiles( response.items );
			response.items.forEach(function(item){
				//console.log('DFR for:'+item.id);
				//console.log(dfr.cache.byfile[item.id]);

				if( dfr.cache.byfile[item.id] != undefined )
					dfr.cache.byfile[item.id].staticdata.changed = true;
				else{
					var cc = new ContextController();
					//console.log('Controller not found creating new.');
					cc.initCache( -1, 'context#byfile');
					dfr.cache.byfile[item.id] = cc;
					dfr.cache.controllers.push(cc);
					//dfr.cache.byfile[item.id].fileIds.push(item.id);
					dfr.cache.byfile[item.id].staticdata.changed = true;	// notify the file that it has changed.
				}
			});

			dfr.cache.bydir[folderId].cacheFiles( new Date() );
            response.items = dfr.cache.bydir[folderId].files;
            callbacks['finish']( response );
            
        });
	}

	this.loadByFile = function( fileId, callbacks, datetime, refresh_changes ){
		query = {
            "fileId": fileId,
            //"q":'modifiedDate >= \''+new Date(this.cache.lastUpdated).toISOString()+'\''
        };
        var file_cache = this.cache.byfile[fileId];
        //console.log('FILE:')
        //console.log(file_cache);

		if( file_cache != undefined && file_cache.lastUpdated != null){
			this.cache.byfile[fileId].staticdata.hits++;
			callbacks['cached']( file_cache.files[0] )
		}
		else{
			var cc = new ContextController();
			cc.initCache( -1, 'context#byfile');
			dfr.cache.byfile[fileId] = cc;
			dfr.cache.controllers.push(cc);
			//dfr.cache.byfile[fileid].fileIds.push(fileid);
			dfr.cache.byfile[fileId].staticdata.changed = true;
			file_cache = dfr.cache.byfile[fileId];
		}

		if( refresh_changes || file_cache.staticdata.changed )
			gapi.client.drive.files.get(query).execute(function(response){
				dfr.cache.byfile[fileId].staticdata.changed = false;
				dfr.cache.byfile[fileId].pushFiles( [response] );
				dfr.cache.byfile[fileId].cacheFiles( new Date() );
            	callbacks['finish']( response );
        	});
		else
			callbacks['finish']( file_cache.files[0] );

	}

	/*this.cacheExists = function(){
		return (this.cache.lastUpdated == null);
	}*/

	//Background loading functions.
	/*
	this.loadAllBG = function( callbacks, stepSize ){
		var numFilesLoaded = 0;
		gapi.client.drive.files.list({
            "maxResults":stepSize,
        }).execute(function loadNext( response ) {
            this.cache.pushFiles( response.items );
            
            if( response.items )
            	numFilesLoaded += response.items.length;
            	callbacks['progress']( numFilesLoaded );

            if( response.pageToken ){
            	gapi.client.drive.files.list({
            	"pageToken":response.pageToken,
            	}).execute( loadNext );

            }else{
            	this.cache.cacheFiles( callbacks['datetime']() );
            	callbacks['finish']();
            }

        });

	}
	this.loadChangesBG = function( callback, datetime ){

		q = 'modifiedDate >= \''+this.cache.lastUpdated.toISOString()+'\'';

		gapi.client.drive.files.list({
            "q":q,
        }).execute(function(response) {
            this.cache.pushFiles( response.items );	// store on 'floating' list.
            this.cache.cacheFiles( datetime );	// cache to local machine with a timestamp.
        });

	}*/
}