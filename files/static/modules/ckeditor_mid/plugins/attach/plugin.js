CKEDITOR.plugins.add('attach',
{
    init: function(editor)
    {
    var pluginName = 'attach';

    editor.addCommand( pluginName,
    {
        exec : function( editor )
        {
            $('.cke_focus').closest('.news_comment_body').find('.attach_doc_btn').click();
        },

        canUndo : true
    });

    editor.ui.addButton('attach',
    {
        label: 'Save',
        command: pluginName,
        className : 'cke_button_save'
    });
    }
});