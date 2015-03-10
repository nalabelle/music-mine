#!/usr/bin/env python
import sys, os, getopt
import pprint
import ConfigParser
import json
import time
import requests
from datetime import date
from echonest import EchoNest

class MusicMine:
  config = None
  debug = False

  def main(self, argv):
    config = ConfigParser.ConfigParser()
    config.read('config')
    self.config = config

    try:
      opts, args = getopt.getopt(argv, "cd")
    except getopt.GetoptError:
      usage()
      sys.exit(2)

    for opt, arg in opts:
      if opt == '-d':
        self.debug = True
      if opt == '-c':
        for section in config.sections():
          print '%s' % section
          pp = pprint.PrettyPrinter(indent=2)
          pp.pprint(dict(config.items(section)))

    chartitems = self.printcharts()
    self.printreviews(chartitems)

  def printcharts(self, form=None):
    chlist = []
    location = self.config.get('Charts', 'export')
    form = self.config.get('Charts', 'format')
    charts = json.loads(self.config.get('Charts', 'charts'))

    if self.debug:
      print charts

    for chartName in charts:
      # Dynamically load classes
      mod = __import__('charts')
      className = '%sChart' % chartName
      chart = getattr(mod, className)
      chart = chart()

      chartlist = chart.filter()
      if location == 'Display' or self.debug:
        pp = pprint.PrettyPrinter(indent=2)
        pp.pprint(chartlist)

      if location == 'File':
        path = form.replace('{chartname}', chartName)
        path = path.replace('{date}', date.today().strftime("%Y-%m-%d"))
        path = 'chart/%s' % path
        if not os.path.exists(os.path.dirname(path)):
          os.makedirs(os.path.dirname(path))
        cfile = open(path, 'w')
        for item in chartlist:
          string = "%s / %s / %s\n" % (item['artist'],
            item['album'], item['date'])
          cfile.write(string.encode('utf8'))
          chlist.append(item)
        cfile.close()
    return chlist

  def printreviews(self, chartitems):
    nest = EchoNest(self.config.get('EchoNest', 'apikey'))
    location = self.config.get('Reviews', 'export')

    for item in chartitems:
      # skip Various Artists and Soundtracks because no good data
      if item['artist'] in json.loads(self.config.get('EchoNest', 'VAstrings')):
        continue;

      revlist = nest.filter(item['artist'])

      if location == 'Display' or self.debug:
        pp = pprint.PrettyPrinter(indent=2)
        pp.pprint(revlist)

      if location == 'File':
        path = self.pathreplace(self.config.get('Reviews', 'format'), item)
        path = 'reviews/%s' % path
        tracker = self.pathreplace(self.config.get('Reviews', 'trackerfile'), item)
        tracker = 'reviews/%s' % tracker

        track = self.get_list(tracker)
        if len(track) > 0:
          itemid = max(int(s) for s in track)
        else:
          itemid = 0


        for item in revlist:
          itemid += 1
          #filter out anything we've seen before
          bail = False
          for key, value in track.iteritems():
            if value['url'] == item:
              bail = True
              break
          if bail:
            continue
          track[itemid] = {'url': item, 'date': "%s" % date.today().strftime("%Y-%m-%d")}

          print "%s: %s" % (itemid, item)
          # ssl certs may not match
          try:
            response = requests.get(item, verify=False)
          except requests.exceptions.SSLError, e:
            print e
            continue

          #save the html
          htmlpath = "%s%s.txt" % (path, itemid)
          if not os.path.exists(os.path.dirname(htmlpath)):
            os.makedirs(os.path.dirname(htmlpath))
          cfile = open(htmlpath, 'w')
          cfile.write(response.content)
          cfile.close()

        #save the tracker file
        self.save_list(tracker, track)

      time.sleep(self.config.getint('EchoNest', 'sleep'))

  def get_list(self, filename):
    filename = "%s.json" % filename
    data = {}
    if os.path.exists(filename):
      with open(filename) as json_data:
        data = json.load(json_data)
    return data

  def save_list(self, filename, data):
    filename = "%s.json" % filename
    with open(filename, 'w') as outfile:
      json.dump(data, outfile)

  def pathformat(self, s):
    import string
    valid_chars = '-_.() %s%s' % (string.ascii_letters, string.digits)
    string = ''.join(c for c in s if c in valid_chars)
    return string

  def pathreplace(self, s, album_info):
    s = s.replace('{artist}', self.pathformat(album_info['artist']))
    s = s.replace('{album}', self.pathformat(album_info['album']))
    s = s.replace('{date}', date.today().strftime("%Y-%m-%d"))
    s = s.replace('{item}', '')
    return s

if __name__ == "__main__":
  mine = MusicMine()
  mine.main(sys.argv[1:])
