/*
*	FEST API background cache system.
*	Currently operates off a hard cache and a soft cache.
*	the hard cache auto loads files on the background and stores them on the local machine thus reducing the load times.
*	the soft cache stores search results on global vars in order mimic a decent amount of common sense. Does NOT store data on the client machine.
*/
var ContextController = function(){

	var cobj = this;	// set local object as cobj.

	this.files = [];
	this.lastUpdated = null;
	this.fileIds = [];
	this.contextType = 'context#unknown'
	this.staticdata = {};
	this.contextNumber = -1;


	this.initCache = function( contextNumber, contextType ){
		this.contextNumber = contextNumber;
		if(localStorage.contexts[ contextNumber ] != undefined){
			// TODO at some point.... optimize this code to have a single write and single read.
			this.files = JSON.parse( localStorage.contexts[contextNumber].files );
			this.fileIds = JSON.parse( localStorage.contexts[contextNumber].fileIds );
			this.lastUpdated = JSON.parse( localStorage.contexts[contextNumber].lastUpdated );
			this.contextType = JSON.parse( localStorage.contexts[contextNumber].contextType );
			this.staticdata = JSON.parse( localStorage.contexts[contextNumber].staticdata );
		}
		else{
			this.files = [];
			this.lastUpdated = null;
			this.fileIds = [];
			this.contextType = contextType || 'context#unknown'
			this.contextNumber = localStorage.contexts.length;
		}
	}


	// cache files using the date parameter
	this.cacheFiles = function( datetime ){
		localStorage.contexts[contextNumber].files = JSON.stringify(this.files);
		localStorage.contexts[contextNumber].fileIds = JSON.stringify(this.fileIds);
		localStorage.contexts[contextNumber].lastUpdated = JSON.stringify(datetime);
		localStorage.contexts[contextNumber].contextType = JSON.stringify(this.contextType);
		localStorage.contexts[contextNumber].staticdata = JSON.stringify(this.staticdata)
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
		this.files = JSON.parse( localStorage.contexts[contextNumber].files );
		this.fileIds = JSON.parse( localStorage.contexts[contextNumber].fileIds );
		this.lastUpdated = JSON.parse( localStorage.contexts[contextNumber].lastUpdated );
		this.contextType = JSON.parse( localStorage.contexts[contextNumber].contextType );
		this.staticdata = JSON.parse( localStorage.contexts[contextNumber].staticdata );
	}

	this.pushFiles = function( fileList ){
		fileList.forEach(function(e){
			if( cobj.fileIds.indexOf(e.id) != -1 ){
				cobj.files[ fmc.fileIds.indexOf( e.id) ] = e;
			}
			else{
				cobj.files.push(e);
				cobj.fileIds.push(e.id);
			}
		});
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
		for( var i = 0; i<localStorage.num_contexts; i++ );
			cc = new ContextController( );
			cc.initCache( i );
			this.controllers.push( cc )
			if( controller.contextType == 'context#bydir' ) 
				this.bydir[controller.staticdata.dirid] = controller;
			else if( controller.contextType == 'context#byfile' ) 
				this.byfile[controller.staticdata.fileid] = controller;
			else if( controller.contextType == 'context#byall' ) 
				this.byall['global'] = controller;

		}
	}
}

var DriveFileRetreival = function(){

	this.cache = new FileMetaCache();

	this.init = function(){
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
		query = {
            "folderId": folderId,
            //"q":'modifiedDate >= \''+new Date(this.cache.lastUpdated).toISOString()+'\''
        };
        var dir_cache = this.cache.bydir[folderId];
		if( dir_cache != undefined ){
			query.q = 'modifiedDate >= \''+new Date(dir_cache.lastUpdated).toISOString()+'\'';
			callbacks['cached']( dir_cache.files )
		}else{
			var cc = new ContextController();
			cc.initCache( -1, 'cache#bydir');
			dfr.cache.bydir[folderId] = cc;
			dfr.cache.controllers.push(cc);
			dir_cache = cc;
		}
		gapi.client.drive.children.list(query).execute(function(response) {
			var cachedFiles = [];
			dir_cache.files.forEach(function( item ){
            	if( item.parents[0].id == folderId ) 
            		cachedFiles.push( item );
            });

			//totalResponse = response;


			if( response.items == undefined ){
				response.items = cachedFiles;
            	callbacks['finish']( response );
            	return;
			}
			// Possible incosistency if dir_cache is not accessed by address.
			dfr.cache.bydir[folderId].pushFiles( response.items );
			response.items.forEach(function(item){
				if( dfr.cache.byfile[item.id] != undefined )
					dfr.cache.byfile[item.id].staticdata.changed = true;
				else{
					var cc = new ContextController();
					cc.initCache( -1, 'cache#byfile');
					dfr.cache.byfile[item.id] = cc;
					dfr.cache.controllers.push(cc);
					dfr.cache.byfile[item.id].fileIds.push(item.id);
					dfr.cache.byfile[item.id].staticdata.changed = true;
				}
			});

			dfr.cache.bydir[folderId].cacheFiles( new Date() ); 
            response.items = dfr.cache.bydir[folderId].files;
            callbacks['finish']( response );
            /*response.items.forEach(function( item ){
            	if( item.kind == 'drive#childReference' ){
            		console.log('need to get more data. for ');
            		console.log(item);
					gapi.client.drive.files.get({fileId:item.id}).execute(function( response ){
						properResponse.push( response );
						console.log('GOT:')
						console.log( response );
						itemsLoaded++;
						callbacks['metaload']( response, itemCount, itemsLoaded );

						if( itemCount == itemsLoaded ){
							// Do push and cache after all items are loaded.
							dfr.cache.pushFiles( properResponse );
            				dfr.cache.cacheFiles( datetime );
            				dfr.cache.syncFiles( );
            				totalResponse.items = properResponse.concat( cachedFiles );
            				callbacks['finish']( totalResponse );
						}

					});
				}
				else
				{
					properResponse.push(item);
				}

            });*/
        });
	}

	this.loadByFile = function( fileId, callbacks, datetime, refresh_changes ){
		query = {
            "fileId": fileId,
            //"q":'modifiedDate >= \''+new Date(this.cache.lastUpdated).toISOString()+'\''
        };
        var file_cache = this.cache.byfile[fileId];

		if( file_cache != undefined )
			callbacks['cached']( file_cache.files[0] )
		else{
			var cc = new ContextController();
			cc.initCache( -1, 'cache#byfile');
			dfr.cache.byfile[fileid] = cc;
			dfr.cache.controllers.push(cc);
			dfr.cache.byfile[fileid].fileIds.push(fileid);
			dfr.cache.byfile[fileid].staticdata.changed = true;
			file_cache = dfr.cache.byfile[fileid];
		}

		if( refresh_changes || file_cache.staticdata.changed )
			gapi.client.drive.files.get(query).execute(function(response) 
				if( response.items == undefined ){
            		callbacks['finish']( response );
            		return;
				}
			// Possible incosistency if dir_cache is not accessed by address.
				dfr.cache.bydir[folderId].pushFiles( response.items );
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