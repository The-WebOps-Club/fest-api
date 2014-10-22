CKEDITOR.plugins.add('showtime',   //name of our plugin
{    
    requires: ['dialog'], //requires a dialog window
    init:function(a) {
  var b="showtime";
  var c=a.addCommand(b,new CKEDITOR.dialogCommand(b));
  c.modes={wysiwyg:1,source:1}; //Enable our plugin in both modes
  c.canUndo=true;
 
  //add new button to the editor
  a.ui.addButton("showtime",
  {
   label:'Show current time',
   command:b,
   icon:this.path+"showtime.png"   //path of the icon
  });
  CKEDITOR.dialog.add(b,this.path+"dialogs/ab.js") //path of our dialog file
 }
});