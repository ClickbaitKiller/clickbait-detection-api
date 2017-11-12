import twitter
import re


def load_twitter_reader():
  regex = re.compile(r'/status/\d*')


  api = twitter.Api(consumer_key='x3nOLTWibiXWJalCEE8NGuGNn',
                        consumer_secret='ULyX33kaM0NoT8gZu1JVcbGcHIvrCocxxUOJm7e7bK9OjHLuJe',
                        access_token_key='2387757236-592DQJ5jW1zDCiirqqlQv777pWL91QPBWXAlf0K',
                        access_token_secret='0QC8kXBc5oFQx2PrCqmsxtZ67VCNSo4F4SAxNfACWBOFb')

  def get_twitter_text(url):
    id = regex.search(url)[0].split('/status/')[1]
    return api.GetStatus(status_id=929511061954297857).text

  return get_twitter_text

