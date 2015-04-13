#!/usr/bin/env python

from senti_classifier import senti_classifier
import nltk.data

def getSentiment(text):
  sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
  sentences = sent_detector.tokenize(text.strip())
  print sentences
  pos_score, neg_score = senti_classifier.polarity_scores(sentences)
  print pos_score, neg_score
  return pos_score, neg_score