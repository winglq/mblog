import os
import codecs
import markdown

from mblog.datasources.driver import SourceDriver


class FileSource(SourceDriver):
    def __init__(self, dir_list):
        if not isinstance(dir_list, type([])):
            dir_list = [dir_list]
        self.dir_list = dir_list

    def get_entries(self):
        blog_entries = []
        for d in self.dir_list:
            files = os.listdir(d)
            for f in files:
                if not f.endswith('md'):
                    continue
                entry = self.get_empty_entry()
                entry['location'] = "file://%s" % ("%s/%s" % (d, f))
                entry['id'] = f.strip().split('.')[0]
                entry['title'] = entry['id']
                blog_entries.append(entry)
        return blog_entries

    @staticmethod
    def location_to_file_path(location):
        return location.split('//')[-1]

    def entry_to_html(self, entry_id):
        entries = self.get_entries()
        for entry in entries:
            if entry['id'] == entry_id:
                md = self.location_to_file_path(entry['location'])

        with codecs.open(md, 'r', 'utf-8') as f:
            blog_content = markdown.markdown(
                f.read(),
                extensions=['markdown.extensions.tables',
                            'markdown.extensions.toc',
                            'markdown.extensions.nl2br',
                            'codehilite'])
        return blog_content
