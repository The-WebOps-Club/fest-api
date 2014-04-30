import misaka
from misaka import HtmlRenderer, SmartyPants
from pygments import highlight, lexers, formatters
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from django import template

#Tell django that this is a template filter module
register = template.Library()

VIDEO_SOURCES = {
  "youtube": {
    "re": r'https?://(www\.|)youtube\.com/watch\?\S*v=(?P<youtube>[A-Za-z0-9_&=-]+)\S*',
    "embed": u"//www.youtube.com/embed/%s"
  },
  "vimeo": {
    "re": r'https?://(www\.|)vimeo\.com/(?P<vimeo>\d+)\S*',
    "embed": u"//player.vimeo.com/video/%s"
  }
}

class CustomRenderer(HtmlRenderer, SmartyPants):
    def setup(self):
        super(CustomRenderer, self).setup()

    def image(self, link, title, alt):
        print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
        print link, title, alt
        for key, val in VIDEO_SOURCES.items():
          match = re.match(val["re"], link)
          if match and match.group(key):
            video_id = match.group(key)
            return self.make_iframe(video_id.strip(), key, alt, title)
        return u"<img src='{0}' alt='{1}' title='{2}'/>".format(link, alt, title)
 
    def make_iframe(self, id, video_type, alt, title):
        url = VIDEO_SOURCES[video_type]["embed"] % id
        return u"<iframe class='{2}' src='{0}' alt='{1}' title='{3}' allowfullscreen></iframe>" \
            .format(url, alt, video_type, title)

    def block_code(self, text, lang):
        s = ''
        if not lang:
            lang = 'text'
        try:
            lexer = get_lexer_by_name(lang, stripall=True)
        except:
            s += '<div class="highlight"><span class="err">Error: language "%s" is not supported</span></div>' % lang
            lexer = get_lexer_by_name('text', stripall=True)
        formatter = HtmlFormatter()
        s += highlight(text, lexer, formatter)
        return s

    def table(self, header, body):
        return '<table class="table">\n'+header+'\n'+body+'\n</table>'

# And use the renderer
renderer = CustomRenderer(flags=misaka.HTML_ESCAPE | misaka.HTML_HARD_WRAP | misaka.HTML_SAFELINK)
md = misaka.Markdown(renderer,
    extensions=
        misaka.EXT_FENCED_CODE | 
        misaka.EXT_NO_INTRA_EMPHASIS | # aa_bb_cc does not become italic
        misaka.EXT_TABLES | 
        misaka.EXT_AUTOLINK | # Autolink http:// and stuff
        misaka.EXT_SPACE_HEADERS | 
        misaka.EXT_STRIKETHROUGH | 
        misaka.EXT_SUPERSCRIPT  # The ^2 becoming squared funda
    )

def markdown(text, style="default"):
    return md.render(text)

register.filter('markdown', markdown)