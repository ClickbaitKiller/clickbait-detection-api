from html.parser import HTMLParser
import re

url = 'https://www.buzzfeed.com/beckybarnicoat/autumnal-dresses-perfect-for-a-cold-november-day?' \
      'utm_term=.vflRJgz57p#.acxDezxw4o'

f = open('test.html', 'r')
html_content = f.read()
f.close()


class MyHTMLParser(HTMLParser):

    HEADER_PATTERN = '^h\d$'
    HEADER_ORDER = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8']

    def __init__(self):
        super().__init__()
        self.header_list = []
        self.incomplete_tag = None

    def handle_starttag(self, tag, attrs):

        if re.match(self.HEADER_PATTERN, tag):
            self.incomplete_tag = {
                'type': tag,
                'content': '',
            }

    def handle_endtag(self, tag):

        if re.match(self.HEADER_PATTERN, tag):
            self.header_list.append(self.incomplete_tag)
            self.incomplete_tag = None

    def handle_data(self, data):

        if self.incomplete_tag is not None:
            self.incomplete_tag['content'] += data

    def error(self, message):
        print('Parse error', message)

    def get_list(self):
        return self.header_list

    def get_nested(self):

        structure = {
            'type': 'root',
            'content': '',
            'list': self.header_list,
        }

        def process_structure(struct):

            struct_list = struct['list']
            level = self.HEADER_ORDER.index(struct['type'])

        return process_structure(structure)



def fetch_html(url):
    pass


def get_headers(html):
    html_header_extractor = MyHTMLParser()
    html_header_extractor.feed(html)

    return html_header_extractor.get_list()

if __name__ == '__main__':
    print(html_content)
    print(get_headers(html_content))
