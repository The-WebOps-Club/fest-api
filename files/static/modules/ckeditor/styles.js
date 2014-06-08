/**
 * Copyright (c) 2003-2014, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see LICENSE.md or http://ckeditor.com/license
 */

CKEDITOR.stylesSet.add( 'default', [
	/* Block Styles */

	{ name: 'Title',		element: 'h2' },
	{ name: 'Subtitle',			element: 'h3', styles: { 'color': '#aaa',} },
	{
		name: 'Container',
		element: 'div',
		styles: {
			padding: '5px 10px',
			background: 'transparent',
			border: '1px solid #ccc'
		}
	},


	{ name: 'Marker',			element: 'span', attributes: { 'class': 'marker' } },

	{ name: 'Big',				element: 'big' },
	{ name: 'Small',			element: 'small' },
	{ name: 'Typewriter',		element: 'tt' },

	{ name: 'Deleted Text',		element: 'del' },

	/* Object Styles */

	{
		name: 'Styled image (left)',
		element: 'img',
		attributes: { 'class': 'left' }
	},

	{
		name: 'Styled image (right)',
		element: 'img',
		attributes: { 'class': 'right' }
	},

	{
		name: 'Compact table',
		element: 'table',
		attributes: {
			cellpadding: '5',
			cellspacing: '0',
			border: '1',
			bordercolor: '#ccc'
		},
		styles: {
			'border-collapse': 'collapse'
		}
	},

	{ name: 'Borderless Table',		element: 'table',	styles: { 'border-style': 'hidden', 'background-color': '#E6E6FA' } },
	{ name: 'Square Bulleted List',	element: 'ul',		styles: { 'list-style-type': 'square' } }
] );

