/*
*	FEST API background cache system.
*	Currently operates off a hard cache and a soft cache.
*	the hard cache auto loads files on the background and stores them on the local machine thus reducing the load times.
*	the soft cache stores search results on global vars in order mimic a decent amount of common sense. Does NOT store data on the client machine.
*/

var FileMetaCache = function(){
	// SINGLETON pattern.
	fmc = this;

	// set variables to null.
	this.files = [];
	this.lastUpdated = null;
	this.fileIds = [];

	this.initCache = function(){
		if(localStorage.files != undefined){
			this.files = JSON.parse(localStorage.files);
			this.fileIds = JSON.parse(localStorage.fileIds);
			this.lastUpdated = JSON.parse(localStorage.lastUpdated);
		}
		else{
			this.files = [];
			this.lastUpdated = null;
			this.fileIds = [];
		}
	}


	// cache files using the date parameter
	this.cacheFiles = function( datetime ){
		localStorage.files = JSON.stringify(this.files);
		localStorage.fileIds = JSON.stringify(this.fileIds);
		localStorage.lastUpdated = JSON.stringify(datetime);
	}

	this.syncFiles = function(){
		this.files = JSON.parse(localStorage.files);
		this.fileIds = JSON.parse(localStorage.fileIds);
		this.lastUpdated = JSON.parse(localStorage.lastUpdated);
	}

	this.pushFiles = function( fileList ){

		fileList.forEach(function(e){
			if( fmc.fileIds.indexOf(e.id) != -1 ){
				fmc.files[ fmc.fileIds.indexOf( e.id) ] = e;
			}
			else{
				fmc.files.push(e);
				fmc.fileIds.push(e.id);
			}
		});
	}

}

var DriveFileRetreival = function(){

	this.cache = new FileMetaCache();

	this.init = function(){
		this.cache.initCache();
	}

	dfr = this;	// set local context for all functions decalred within this block to prevent confusion. Using self raises some weird issues.

	/*
	*	folderId: ID of the folder to retreive.
	*	callbacks:  
	*/
	this.loadByDir = function( folderId, callbacks, datetime ){
		query = {
            "folderId": folderId,
            "q":'modifiedDate >= \''+new Date(this.cache.lastUpdated).toISOString()+'\''
        };
		if(this.cache.lastUpdated != null)
			query.q = 'modifiedDate >= \''+new Date(this.cache.lastUpdated).toISOString()+'\'';

		gapi.client.drive.children.list(query).execute(function(response) {
			var cachedFiles = [];
			dfr.cache.files.forEach(function( item ){
            	if( item.parents[0].id == folderId ) 
            		cachedFiles.push( item );
            });

			totalResponse = response;

			if( response.items == undefined ){
				totalResponse.items = cachedFiles;
            	callbacks['finish']( totalResponse );
            	return;
			}
            properResponse = [];
            itemCount = response.items.length;
            itemsLoaded = 0;

            

            response.items.forEach(function( item ){
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

            });
        });
	}

	this.cacheExists = function(){
		return (this.cache.lastUpdated == null);
	}

	//Background loading functions.
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

	}
}