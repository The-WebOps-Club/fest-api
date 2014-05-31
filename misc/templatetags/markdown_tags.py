
import misaka
from misaka import HtmlRenderer, SmartyPants
from django import template
from django.conf import settings
from misc.utils import *  #Import miscellaneous functions
import re

#Tell django that this is a template filter module
register = template.Library()

VIDEO_SOURCES = {
  "youtube": {
    "re": r'https?://(www\.|)youtube\.com/watch\?\S*v=(?P<youtube>[A-Za-z0-9_=-]+)\S*',
  },
  # "vimeo": {
  #   "re": r'https?://(www\.|)vimeo\.com/(?P<vimeo>\d+)\S*',
  # },
}

class CustomRenderer(HtmlRenderer, SmartyPants):
    
    """
        # Block level
            x block_code(str code, str language)
            / block_quote(str quote)
            / block_html(str raw_html)
            x header(str text, int level)
            / hrule()
            / list(str contents, bool is_ordered)
            / list_item(str text, bool is_ordered)
            / paragraph(str text)
            x table(str header, str body)
            x table_row(str content)
            x table_cell(str content, int flags)

        # Span Level    
            / autolink(str link, bool is_email)
            / codespan(str code)
            / double_emphasis(str text)
            / emphasis(str text)
            / image(str link, str title, str alt_text)
            / linebreak()
            / link(str link, str title, str content)
            / raw_html(str raw_html)
            / triple_emphasis(str text)
            / strikethrough(str text)
            / superscript(str text)

        # Low level
            entity(str text)
            normal_text(str text)

        # Header, Footer
            doc_header()
            doc_footer()

        # Processors
            preprocess(str full_document)
            postprocess(str full_document)
    """

    def setup(self):
        super(CustomRenderer, self).setup()


    def header(self, text, level) :
        return "<p>" + text + "</p>"

    def link(self, link, title, content):
        return_text = ""
        if not title:
            title = ""
        _id = None
        if title.startswith("doc#") or title.startswith("user#") or title.startswith("subdept#") or title.startswith("dept#") or title.startswith("page#"): # Implies it is a doc from drive
            _type, _id = title.split("#", 1)
            if _type == "doc":
                _link = reverse("view") + "?id=" + _id
            else:
                _link = reverse("my_wall", kwargs={"owner_type":_type, "owner_id":_id})

        if _id:
            _name = content
            _icon = link
            _icon_text = ""
            if _type == "doc":
                _icon_text = "<img src='" + _icon + "' />"
            else:
                _icon_text = "<i class='icon-" + _type + "'></i>"
            return_text = _icon_text + " <a href='" + _link + "' target='_blank' title='" + title +"' data-id='" + _id + "' >" + _name +"</a>"
        else:
            return_text = "<a href='" + link + "' target='_blank' title='" + title +"' >" + content +"</a>"
        
        return return_text

    def autolink(self, link, is_email):
        my_html = ''
        if is_email :
            # print link
            preview = ""
            short_link = (link[:40] + '..') if len(link) > 40 else link
            my_html = "<a target='_blank' href='mailto:" + link + "'>" + short_link + "</a>" + preview
        else :    
            # print link
            preview = ""
            video_id = ""
            for key, val in VIDEO_SOURCES.items():
                match = re.match(val["re"], link)
                if match and match.group(key):
                    video_id = match.group(key)
                #     preview = """<a href='%s' target='_blank'><div class='row-fluid video_render video_comment' data-service='%s' data-video-id='%s'> <div class='span4 left'>
                #         </div> <div class='span8 right'>
                #         </div></div></a>""" % (link, key, video_id)
            short_link = (link[:40] + '...') if len(link) > 40 else link
            if video_id:
                my_html = "<a target='_blank' class='comment_link_render comment_link' data-service='%s' data-link-id='%s' href='%s'>%s</a>" % (key, video_id, link, short_link)
            else:
                my_html = "<a target='_blank' href='%s'>%s</a>" % (link, short_link)
            # print my_html
        return my_html
    
    def block_code(self, text, lang):
        return text
    
# And use the renderer
renderer = CustomRenderer(flags=
        # misaka.HTML_SKIP_HTML |
        # HTML_SKIP_STYLE |
        # HTML_SKIP_IMAGES |
        # HTML_SKIP_LINKS |
        # HTML_EXPAND_TABS |
        misaka.HTML_SAFELINK |
        # misaka.HTML_TOC | 
        misaka.HTML_HARD_WRAP |
        # misaka.HTML_USE_XHTML |
        # misaka.HTML_ESCAPE |  //do not escape.
        misaka.HTML_SMARTYPANTS
    )
md = misaka.Markdown(renderer,
    extensions=
        misaka.EXT_NO_INTRA_EMPHASIS | # aa_bb_cc does not become italic
        # misaka.EXT_TABLES | 
        misaka.EXT_FENCED_CODE | 
        misaka.EXT_AUTOLINK # Autolink http:// and stuff
        # misaka.EXT_STRIKETHROUGH | # Allow strikethough in text
        # misaka.EXT_LAX_SPACING |
        # misaka.EXT_SPACE_HEADERS | 
        # misaka.EXT_SUPERSCRIPT  # The ^2 becoming squared funda
    )
 
def markdown(text, style="default"):
    return md.render(text)

register.filter('markdown', markdown)