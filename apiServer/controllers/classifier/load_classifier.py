import pickle

def load_classifier():
  classifier_clickbait, classifier_listicle,tfv = pickle.load(open('./controllers/classifier/classifier.p', 'rb'))

  def predict_clickbait(X):
    return [p[1] for p in classifier_clickbait.predict_proba(tfv.transform(X))]


  def predict_listicle(X):
    return classifier_listicle.predict_proba(tfv.transform([X]))[0][1]

  return predict_clickbait, predict_listicle


if __name__ == '__main__':
  predict, _ = load_classifier()

  X = ['you will never believe what happens next', 'Obama declares war']

  print(predict(X))
