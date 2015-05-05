#!/usr/bin/env python

import sys
import os
import json

if __name__ == "__main__":
  path = sys.argv[1]
  reviewpath = sys.argv[2]
  print "path: " + path
  reviews = {}
  for subdir, dirs, files in os.walk(reviewpath):
    for file in files:
      fileName, fileExtension = os.path.splitext(file)
      if(fileName[0] == '.' or fileExtension != '.json'):
        continue
      fpath = os.path.join(subdir, file)
      with open(fpath, 'r') as reviewjson:
        data = json.load(reviewjson)
        reviews[fileName] = {}
        for key,value in data.items():
          reviews[fileName][key] = value['date']

  for subdir, dirs, files in os.walk(path):
    for file in files:
      fileName, fileExtension = os.path.splitext(file)
      fpath = os.path.join(subdir, file)
      if(fileName[0] == '.' or fileExtension != '.txt'):
        continue
      with open(fpath, "r") as chartlist:
        for line in chartlist:
          data = line.strip().split(',')
          filename = data[0].replace('\\','/').split('/')[::-1][0:2]
          num = filename[0].rstrip('.txt')
          artist = filename[-1]
          if num == '' or artist == '':
            continue
          #print reviews[artist]
          print '%s\t%s\t%s\t%s\t%s' % (artist,num,reviews[artist][num], data[1], data[2])
          #s = '%s\t%s\t%s\t%s\t%s' % (chartName[-1], fileName, i, data[0], data[1])
          #s = s.rstrip()
          #print s
          #storage.append(s)
  #with open('chartdetails.txt', 'w') as details:
  #  for line in storage:
  #    details.write('%s\n' % line)
