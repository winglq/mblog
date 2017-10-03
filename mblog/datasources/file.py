import os
import codecs
import markdown

from mblog.datasources.driver import SourceDriver
from mblog.exceptions import InstanceNotInit


class FileSource(SourceDriver):
    instance = None
    def __init__(self, dir_list, exclude_files):
        if not isinstance(dir_list, type([])):
            dir_list = [dir_list]
        self.dir_list = dir_list
        self.exclude_files = exclude_files

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = SourceDriver.__new__(cls, *args,
                                                **kwargs)
        return cls.instance

    @classmethod
    def get_instance(cls):
        if cls.instance is None:
            InstanceNotInit(class_name = cls.__name__)
        return cls.instance

    def get_entries(self, exclude_entries=True):
        blog_entries = []
        for d in self.dir_list:
            files = os.listdir(d)
            for f in files:
                if not f.endswith('md'):
                    continue
                entry = self.get_empty_entry()
                if f in self.exclude_files:
                    entry['excluded'] = True
                entry['location'] = "file://%s" % ("%s/%s" % (d, f))
                entry['id'] = f.strip().split('.')[0]
                entry['format'] = 'markdown'
                self.get_metadata("%s/%s" % (d, f), entry)
                if not entry['title']:
                    entry['title'] = entry['id']
                blog_entries.append(entry)
        blog_entries = sorted(blog_entries, key=lambda x: x['date'],
                              reverse=True)
        if exclude_entries:
            return [x for x in blog_entries if not x['excluded']]
        else:
            return blog_entries

    def get_metadata(self, filepath, entry):
        with codecs.open(filepath, 'r', 'utf-8') as f:
            md = markdown.Markdown(extensions=['markdown.extensions.meta'])
            md.convert(f.read())
            entry.update(md.Meta)
            for k, v in entry.iteritems():
                if isinstance(v, type([])):
                    entry[k] = ''.join(v)

    @staticmethod
    def location_to_file_path(location):
        return location.split('//')[-1]

    def entry_to_html(self, entry_id):
        entries = self.get_entries(exclude_entries=False)
        for entry in entries:
            if entry['id'] == entry_id:
                md = self.location_to_file_path(entry['location'])

        if entry['format'] == 'markdown':
            with codecs.open(md, 'r', 'utf-8') as f:
                blog_content = markdown.markdown(
                    f.read(),
                    extensions=['markdown.extensions.tables',
                                'markdown.extensions.toc',
                                'markdown.extensions.nl2br',
                                'codehilite',
                                'markdown.extensions.meta'])
        return blog_content
