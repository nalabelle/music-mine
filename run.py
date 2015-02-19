#!/usr/bin/env python
import sys, os, getopt
import pprint
import ConfigParser
import json
import time
from datetime import date
from echonest import EchoNest

class MusicMine:
    settings = None
    debug = False
    charts = []

    def main(self, argv):
        config = ConfigParser.ConfigParser()
        config.read('config')

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

        self.printcharts(config.get('Charts', 'export'),
                         config.get('Charts', 'format'))

    def printcharts(self, location, form=None):
        for chartName in self.charts:
            # Dynamically load classes
            mod = __import__('charts')
            className = '%sChart' % chartName
            chart = getattr(mod, className)
            chart = chart()

            if location == 'Display' or self.debug:
                pp = pprint.PrettyPrinter(indent=2)
                pp.pprint(chart.filter())

            if location == 'File':
                path = form.replace('{chartname}', chartName)
                path = path.replace('{date}', date.today().strftime("%Y-%m-%d"))
                path = 'chart/%s' % path
                if not os.path.exists(os.path.dirname(path)):
                    os.makedirs(os.path.dirname(path))
                cfile = open(path, 'w')
                for item in chart.filter():
                    string = "%s / %s / %s\n" % (item['artist'],
                        item['album'], item['date'])
                    cfile.write(string.encode('utf8'))
                cfile.close()


if __name__ == "__main__":
    mine = MusicMine()
    mine.main(sys.argv[1:])
