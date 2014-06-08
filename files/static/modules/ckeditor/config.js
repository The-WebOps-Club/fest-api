/**
 * @license Copyright (c) 2003-2013, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see LICENSE.html or http://ckeditor.com/license
 */

CKEDITOR.editorConfig = function( config ) {
	// http://docs.ckeditor.com/#!/api/CKEDITOR.config

	// The toolbar groups arrangement, optimized for two toolbar rows.
	config.toolbarGroups = [
		//{ name: 'clipboard',   groups: [ /*'clipboard', */'undo' ] },
		//{ name: 'editing',     groups: [ 'find', 'selection', 'spellchecker' ] },
		{ name: 'links'},
		{ name: 'insert' },
		//{ name: 'forms' },
		//{ name: 'tools' },
		//{ name: 'document',	   groups: [ 'mode', 'document', 'doctools' ] },
		//{ name: 'others' },
		//'/',
		{ name: 'basicstyles', groups: [ 'basicstyles', 'cleanup' ] },
		{ name: 'paragraph',   groups: [ 'list', 'indent', ] },
		{ name: 'styles' },
//		{ name: 'colors' },
	];

	// Remove some buttons provided by the standard plugins, which are
	// not needed in the Standard(s) toolbar.
	config.removeButtons = 'horizontalrule,table,Format,Strike,Subscript,Superscript,Anchor';
	config.resize_enabled = true;
	// Set the most common block elements.
	config.format_tags = 'p;h1;h2;h3;pre';

	// Simplify the dialog windows.
	config.removeDialogTabs = 'image:advanced;link:advanced';
	config.skin = 'moono';
	config.extraPlugins = 'resize,attach,';
	config.removePlugins = 'horizontalrule,table,liststyle,tabletools,contextmenu,specialchar,Strike,Subscript,Superscript,Anchor';
};
