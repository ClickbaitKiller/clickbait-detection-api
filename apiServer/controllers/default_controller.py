from controllers.classifier.load_classifier import load_classifier

predict = load_classifier()

def detect_get(parameters) -> str:

    for p in parameters:
        p['clickbaitiness'] = predict([p['text']])[0]
        del p['text']
    return parameters

def summary_get(parameters) -> str:
    return 'do some magic!'
