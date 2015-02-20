#!/usr/bin/env python
import sys, os, getopt
import pprint
import ConfigParser
import json
import time
from datetime import date
from echonest import EchoNest

class MusicMine:
    config = None
    debug = False
    charts = []

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

        self.charts = json.loads(config.get('Charts', 'charts'))
        if self.debug:
            print self.charts

        chartitems = self.printcharts(config.get('Charts', 'export'),
                        config.get('Charts', 'format'))

        self.printreviews(chartitems,
                        config.get('Reviews', 'export'),
                        config.get('Reviews', 'format'))

    def printcharts(self, location, form=None):
        chlist = []
        for chartName in self.charts:
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

    def printreviews(self, chartitems, location, form=None):
        nest = EchoNest(self.config.get('EchoNest', 'apikey'))

        for item in chartitems:
            if item['artist'] in json.loads(self.config.get('EchoNest', 'VAstrings')):
                continue;
            revlist = nest.filter(item['artist'])

            if location == 'Display' or self.debug:
                pp = pprint.PrettyPrinter(indent=2)
                pp.pprint(revlist)

            if location == 'File':
                path = form.replace('{artist}', self.pathformat(item['artist']))
                path = path.replace('{album}', item['album'])
                path = path.replace('{date}', date.today().strftime("%Y-%m-%d"))
                path = 'reviews/%s' % path
                if not os.path.exists(os.path.dirname(path)):
                    os.makedirs(os.path.dirname(path))
                cfile = open(path, 'w')
                for item in revlist:
                    string = "%s\n" % (item)
                    cfile.write(string.encode('utf8'))
                cfile.close()

            time.sleep(self.config.getint('EchoNest', 'sleep'))

    def pathformat(self, s):
        import string
        valid_chars = '-_.() %s%s' % (string.ascii_letters, string.digits)
        string = ''.join(c for c in s if c in valid_chars)
        return string

if __name__ == "__main__":
    mine = MusicMine()
    mine.main(sys.argv[1:])
