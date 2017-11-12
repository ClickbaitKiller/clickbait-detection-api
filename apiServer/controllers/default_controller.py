from controllers.classifier.load_classifier import load_classifier
from controllers.summarizer.load_summarizer import load_summarizer
import re

regexp = re.compile(r'\d')

predict = load_classifier()
summarize = load_summarizer()

def detect_post(parameters) -> str:

    texts = map(lambda x: x['text'], parameters)
    res = zip(parameters, predict(texts))

    def reconstruct(elem):
        parameter, score = elem
        return {
            'id': parameter['id'],
            'clickbaitiness': score
        }

    return list(map(reconstruct, res))

def summary_post(parameters) -> str:
    text, url = parameters['text'], parameters['url']
    if regexp.search(text): # contains a number -> listicle
        pass # todo
    else:
        return summarize(url)
