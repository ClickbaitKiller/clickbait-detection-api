from controllers.classifier.load_classifier import load_classifier
from controllers.summarizer.load_summarizer import load_summarizer
from controllers.listicleizer.load_listicleizer import load_listicleizer
from controllers.twitter.load_twitter_reader import load_twitter_reader

predict_clickbait, predict_listicle = load_classifier()
summarize = load_summarizer()
listicleizer = load_listicleizer()
get_twitter_text = load_twitter_reader()

memo = {}


def detect_post(parameters) -> dict:

    texts = map(lambda x: x['text'], parameters)
    res = zip(parameters, predict_clickbait(texts))

    def reconstruct(elem):
        parameter, score = elem
        return {
            'id': parameter['id'],
            'score': score
        }

    return list(map(reconstruct, res))


def summary_post(parameters) -> dict:

    text, url = parameters['text'], parameters['url']

    if (url, text) in memo:
      return memo[(url, text)]

    if '//twitter.com' in url:
        memo[(url, text)] = {
            'type': 'summary',
            'summary': get_twitter_text(url)
        }
    elif predict_listicle(text) > 0.5: # contains a number -> listicle
        memo[(url, text)] = {
            'type': 'listicle',
            'summary': listicleizer(url)
        }
    else:
        memo[(url, text)] = {
            'type': 'summary',
            'summary': summarize(url)
        }


    return memo[(url, text)]
