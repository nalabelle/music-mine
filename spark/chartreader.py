from pyspark import SparkContext
from bs4 import BeautifulSoup
from senti_classifier import senti_classifier
import nltk.data

def getTextFromHTML(html):
  soup = BeautifulSoup(html)
  # remove script tags
  for s in soup.findAll('script'):
    s.extract()
  return soup.get_text()

def getSentiment(text):
  sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
  sentences = sent_detector.tokenize(text.strip())
  pos_score, neg_score = senti_classifier.polarity_scores(sentences)
  return '%s,%s' % (pos_score, neg_score)

sc = SparkContext(appName="ChartReader")

files = sc.wholeTextFiles('reviews/*/*.txt') \
        .map(lambda (x,y): (x, getTextFromHTML(y))) \
	.map(lambda (x,y): (x, getSentiment(y)))

files.saveAsTextFile("senti.txt")
