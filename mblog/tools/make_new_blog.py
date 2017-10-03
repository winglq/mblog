import argparse
import codecs

from datetime import datetime
from jinja2 import Environment, PackageLoader

env = Environment(
        loader=PackageLoader('mblog', 'templates'))


def generate_template(data):
    template = env.get_template("__new_blog.md")
    return template.render({"data": data})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate blog template.')
    parser.add_argument('-o',
                        required=True,
                        help="template output file path")
    parser.add_argument('-i',
                        help='File path to the md file conent')
    args = parser.parse_args()
    data = {}
    if args.i:
        with codecs.open(args.i, 'r', 'utf-8') as f:
            data['content'] = f.read()
    data['date'] = datetime.now().strftime("%Y-%m-%d")
    cnt = generate_template(data)
    with codecs.open(args.o, 'w', 'utf-8') as f:
        f.write(cnt)
