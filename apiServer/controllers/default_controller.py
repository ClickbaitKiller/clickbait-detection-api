from controllers.classifier.load_classifier import load_classifier
from controllers.summarizer.load_summarizer import load_summarizer
from controllers.listicleizer.load_listicleizer import load_listicleizer
import re

regexp = re.compile(r'\d')

predict = load_classifier()
summarize = load_summarizer()
listicleizer = load_listicleizer()


def detect_post(parameters) -> dict:

    texts = map(lambda x: x['text'], parameters)
    res = zip(parameters, predict(texts))

    def reconstruct(elem):
        parameter, score = elem
        return {
            'id': parameter['id'],
            'clickbaitiness': score
        }

    return list(map(reconstruct, res))


def summary_post(parameters) -> dict:
    text, url = parameters['text'], parameters['url']
    if regexp.search(text): # contains a number -> listicle
        return {
            'type': 'listicle',
            'summary': listicleizer(url)
        }
    else:
        return {
            'type': 'summary',
            'summary': summarize(url)
        }
