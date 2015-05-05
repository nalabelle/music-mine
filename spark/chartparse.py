#!/usr/bin/env python

import sys
import os

if __name__ == "__main__":
  path = sys.argv[1]
  print "path: " + path
  
  for subdir, dirs, files in os.walk(path):
    for file in files:
      fileName, fileExtension = os.path.splitext(file)
      if fileExtension != ".txt":
        continue
      fpath = os.path.join(subdir, file)
      f = open(fpath, 'r')
      html = f.read()
      text = getTextFromHTML(html)
      pos, neg = sentiment.getSentiment(text)
      r.write('%s,%s,%s\n' % (fpath, pos, neg))
      #print pos, neg
      f.close()
