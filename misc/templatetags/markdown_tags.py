import misaka
from misaka import HtmlRenderer, SmartyPants
from pygments import highlight, lexers, formatters
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from django import template
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
            / block_code(str code, str language)
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

    def autolink(self, link, is_email):
        my_html = ''
        if is_email :
            # print link
            preview = ""
            short_link = (link[:40] + '..') if len(link) > 40 else link
            my_html = "<a href='mailto:" + link + "'>" + short_link + "</a>" + preview
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

    # def image(self, link, title, alt):
    #     print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
    #     print link, title, alt
    #     for key, val in VIDEO_SOURCES.items():
    #       match = re.match(val["re"], link)
    #       if match and match.group(key):
    #         video_id = match.group(key)
    #         return self.make_iframe(video_id.strip(), key, alt, title)
    #     return u"<img src='{0}' alt='{1}' title='{2}'/>".format(link, alt, title)
 
    # def make_iframe(self, id, video_type, alt, title):
    #     url = VIDEO_SOURCES[video_type]["embed"] % id
    #     return u"<iframe class='{2}' src='{0}' alt='{1}' title='{3}' allowfullscreen></iframe>" \
    #         .format(url, alt, video_type, title)

    # def block_code(self, text, lang):
    #     s = ''
    #     if not lang:
    #         lang = 'text'
    #     try:
    #         lexer = get_lexer_by_name(lang, stripall=True)
    #     except:
    #         s += '<div class="highlight"><span class="err">Error: language "%s" is not supported</span></div>' % lang
    #         lexer = get_lexer_by_name('text', stripall=True)
    #     formatter = HtmlFormatter()
    #     s += highlight(text, lexer, formatter)
    #     return s

    # def table(self, header, body):
        # return '<table class="table">\n'+header+'\n'+body+'\n</table>'

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
        misaka.HTML_ESCAPE | 
        misaka.HTML_SMARTYPANTS
    )
md = misaka.Markdown(renderer,
    extensions=
        misaka.EXT_NO_INTRA_EMPHASIS | # aa_bb_cc does not become italic
        # misaka.EXT_TABLES | 
        # misaka.EXT_FENCED_CODE | 
        misaka.EXT_AUTOLINK | # Autolink http:// and stuff
        # misaka.EXT_STRIKETHROUGH | # Allow strikethough in text
        # misaka.EXT_LAX_SPACING |
        # misaka.EXT_SPACE_HEADERS | 
        misaka.EXT_SUPERSCRIPT  # The ^2 becoming squared funda
    )
 
def markdown(text, style="default"):
    return md.render(text)

register.filter('markdown', markdown)