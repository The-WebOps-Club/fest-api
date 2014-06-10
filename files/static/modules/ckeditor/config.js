/**
 * @license Copyright (c) 2003-2013, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see LICENSE.html or http://ckeditor.com/license
 */

CKEDITOR.editorConfig = function( config ) {
	// Define changes to default configuration here. For example:
	// config.language = 'fr';
	// config.uiColor = '#AADC6E';
	// The toolbar groups arrangement, optimized for a single toolbar row.

	config.language = 'en';

	config.toolbarGroups = [
		{ name: 'document' },
		{ name: 'clipboard' },
		{ name: 'editing' },
		{ name: 'forms' },
		{ name: 'basicstyles' },
		{ name: 'paragraph' },
		{ name: 'links' },
		{ name: 'insert' },
		{ name: 'styles' },
		{ name: 'colors' },
		{ name: 'tools' },
		{ name: 'others' },
		{ name: 'about' }
	];

	// The default plugins included in the basic setup define some buttons that
	// are not needed in a basic editor. They are removed here.
	//config.removeButtons = 'Cut,Copy,Paste,Undo,Redo,Unlink,Anchor,Strike,Subscript,Superscript';
	config.removeButtons = 'Unlink,Anchor,Strike,Subscript,Superscript';
	
	// Dialog windows are also simplified.
	config.removeDialogTabs = 'link:advanced,image:link,image:advanced';

	config.removePlugins = 'a11yhelp,about,clipboard,div,find,flash,format,forms,horizontalrule,iframe,magicline,newpage,pagebreak,pastefromword,pastetext,preview,scayt,showblocks,smiley,specialchar,stylescombo,table,tabletools,wsc';
	config.removePlugins += ',link,image';
 	//config.extraPlugins = 'post_btn';
	
	config.toolbar = 'Full'
	//config.toolbarLocation = 'top'
};
