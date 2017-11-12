from time import sleep
from selenium import webdriver

def load_summarizer():

  driver = webdriver.PhantomJS() # or add to your PATH
  driver.set_window_size(1920, 1200) # optional

  def build_request(url):
      base = 'http://smmry.com/'
      end = '/#&SM_LENGTH=1'
      return base + url + end

  def summarize(url):
    request = build_request(url)
    print(request)
    driver.get(request)
    sleep(1)
    container = driver.find_element_by_id('sm_container_output')

    return container.text

  return summarize

if __name__ == '__main__':
  summarize = init_summarizer()

  url = 'http://www.breitbart.com/video/2017/11/10/alabama-abc-affiliate-cant-find-one-voter-believes-wapo-report-roy-moore-man-street-segment'
  print(summarize(url))
