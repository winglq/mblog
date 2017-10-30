import markdown

from mblog.lib.formaters.driver import Formater


class MarkdownFormater(Formater):

    def loads(self, s):
        md = markdown.Markdown(extensions=['markdown.extensions.tables',
                                           'markdown.extensions.toc',
                                           'markdown.extensions.nl2br',
                                           'codehilite',
                                           'markdown.extensions.meta'])

        html = md.convert(self.s)
        self.html = html
        return md

    def convert_to(self, to='html'):
        if to is 'html':
            return self.html
