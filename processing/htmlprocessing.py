#!/usr/bin/env python
from bs4 import BeautifulSoup
import sys
import sentiment

def getTextFromHTML(html):
  soup = BeautifulSoup(html)

  # remove script tags
  for s in soup.findAll('script'):
    s.extract()
  print(soup.get_text())
  return soup.get_text()

if __name__ == "__main__":
  path = sys.argv[1]
  print "path: " + path
  f = open(path, 'r')
  html = f.read()
  text = getTextFromHTML(html)
  pos, neg = sentiment.getSentiment(text)
  print pos, neg
  f.close()