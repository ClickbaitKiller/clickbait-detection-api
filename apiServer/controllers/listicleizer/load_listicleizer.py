from time import sleep

from selenium import webdriver

from controllers.listicleizer.HTMLHeadersExtractor import HTMLHeadersExtractor


def load_listicleizer():

    driver = webdriver.PhantomJS() # or add to your PATH
    driver.set_window_size(1920, 1200) # optional

    def fetch_html(url):
        driver.get(url)
        sleep(1)
        return driver.page_source

    def get_listicle_headers(html):

        html_header_extractor = HTMLHeadersExtractor()
        html_header_extractor.feed(html)

        nested_headers = html_header_extractor.get_nested()

        # just a complicated function that returns the longest list of consecutive headers (
        # aka. python scoping is a b**ch)
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

    url = 'https://www.buzzfeed.com/beckybarnicoat/autumnal-dresses-perfect-for-a-cold-november-day'

    f = open('test.html', 'r')
    html_content = f.read()
    f.close()

    listicleize = load_listicleizer()

    print(listicleize(url))
