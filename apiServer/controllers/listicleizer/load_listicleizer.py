import json
from html.parser import HTMLParser
import re
from time import sleep

from selenium import webdriver

url = 'https://www.buzzfeed.com/beckybarnicoat/autumnal-dresses-perfect-for-a-cold-november-day?' \
      'utm_term=.vflRJgz57p#.acxDezxw4o'

#f = open('test.html', 'r')
#html_content = f.read()
#f.close()


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
            self.incomplete_tag['content'].strip()
            self.header_list.append(self.incomplete_tag)
            self.incomplete_tag = None

    def handle_data(self, data):

        if self.incomplete_tag is not None:
            self.incomplete_tag['content'] += ' ' + data.strip()

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

def load_listicleizer():

    driver = webdriver.PhantomJS() # or add to your PATH
    driver.set_window_size(1920, 1200) # optional

    def fetch_html(url):
        driver.get(url)
        sleep(1)
        return driver.page_source

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

        def build_html(title, items):
            ret = '<b>'+title+'</b>'
            ret += '<ul>'
            for i in items:
                ret += '\n<li>'+i+'</li>'
            ret += '</ul>'

            return ret

        return build_html(main_title, items)

    def listicleize(url):
        return get_listicle_headers(fetch_html(url))

    return listicleize

if __name__ == '__main__':

    listicleize = load_listicleizer()

    print(listicleize(url))
