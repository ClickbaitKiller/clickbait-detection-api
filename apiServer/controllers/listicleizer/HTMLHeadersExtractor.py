from html.parser import HTMLParser

import re


class HTMLHeadersExtractor(HTMLParser):

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
        """
        Fetch headers as a flat list.
        :return:
        """
        return self.header_list

    def get_nested(self):
        """
        Fetch headers as a nested list.
        :return:
        """

        structure = {
            'type': 'root',
            'content': '',
            'list': self.header_list,
        }

        def process_structure(struct):
            """
            Magic recursive function that transform one root header with a list of consecutive
            headers into a nested list of headers that contain their attached sub-headers.

            It's one of these after midnight hackathon coding, so don't try to understand.
            :param struct:
            :return:
            """

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
