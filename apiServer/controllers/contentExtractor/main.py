import json
from html.parser import HTMLParser
import re

url = 'https://www.buzzfeed.com/beckybarnicoat/autumnal-dresses-perfect-for-a-cold-november-day?' \
      'utm_term=.vflRJgz57p#.acxDezxw4o'

f = open('test.html', 'r')
html_content = f.read()
f.close()


class MyHTMLParser(HTMLParser):

    HEADER_PATTERN = '^h\d$'
    HEADER_ORDER = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9']

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

            print('called on ' + struct['type'] + ' ' + struct['content'])

            struct_list = struct['list']

            if len(struct_list) > 0:

                final_list = []

                element = struct_list.pop(0)
                element_level = self.HEADER_ORDER.index(element['type'])

                temp_list = []

                for el in struct_list:

                    el_level = self.HEADER_ORDER.index(el['type'])

                    if el_level <= element_level:
                        element['list'] = temp_list
                        final_list.append(process_structure(element))

                        element = el
                        element_level = self.HEADER_ORDER.index(element['type'])
                        temp_list = []
                    else:
                        temp_list.append(el)

                element['list'] = temp_list
                final_list.append(process_structure(element))

                struct['list'] = final_list

            else:
                struct['list'] = []

            return struct

        return process_structure(structure)



def fetch_html(url):
    pass


def get_listicle_headers(html):

    html_header_extractor = MyHTMLParser()
    html_header_extractor.feed(html)

    nested_headers = html_header_extractor.get_nested()

    def rec_longest(headers, longest_list, longest_list_size):

        if len(headers['list']) > longest_list_size:
            longest_list_size = len(headers['list'])
            longest_list = headers

        for x in headers['list']:
            longest_list, longest_list_size = rec_longest(x, longest_list, longest_list_size)

        return longest_list, longest_list_size

    longest_list, longest_list_size = rec_longest(
        nested_headers, nested_headers, len(nested_headers['list']))

    main_title = longest_list['content']
    items = list(map(lambda x: x['content'], longest_list['list']))

    print(main_title, longest_list_size, items)

    return nested_headers

if __name__ == '__main__':
    print(html_content)
    print(json.dumps(get_listicle_headers(html_content), indent=2))
