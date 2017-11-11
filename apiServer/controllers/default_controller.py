from controllers.classifier.load_classifier import load_classifier

predict = load_classifier()


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
    return 'do some magic!'
