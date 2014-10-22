CKEDITOR.plugins.add('post_btn',
{
    init: function(editor)
    {
        var pluginName = 'post_btn';
        //CKEDITOR.dialog.add(pluginName, this.path + 'dialogs/footnote.js');
        //editor.addCommand(pluginName, new CKEDITOR.dialogCommand(pluginName));
        editor.ui.addButton('  Post  ', {
            label: 'Post',
            command: pluginName,
            
        });
    }
});