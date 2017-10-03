class SourceDriver(object):
    def get_empty_entry(self):
        blog_entry = {
            'title': '',
            'author': '',
            'date': '',
            'description': '',
            'location': '',
            'format': 'markdown',
            'id': '',
            'tags': [],
            'category': '',
            'excluded': False,
        }
        return blog_entry
