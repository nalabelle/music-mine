#!/usr/bin/env python

import urllib2
import json
import feedparser
import time

from chartscrape import AppleChart

class EchoNest:
    url = "http://developer.echonest.com/artist/%s/reviews.rss?api_key=%s"
    apiKey = ""

    def getList(self, artist):
        try:
            url = self.url % (urllib2.quote(artist.replace(' ', '+'), safe="+"), self.apiKey)
            print url
            data = feedparser.parse(url)
        except Exception, e:
            print e
        return data

    def filter(self, artist):
        data = self.getList(artist)
        newList = []
        if data["items"] is None:
            print data
        for item in data["items"]:
            newList.append(item["link"])
        return newList

    def run(self):
        # temp iterators for testing
        i = 0
        j = 0
        chart = AppleChart()
        for album in chart.filter():
            i += 1
            if i > 5:
                break
            print "%s - %s (%s)" % (album["artist"],
                                    album["album"],
                                    album["date"])
            if album["artist"] == 'Various Artists':
                continue
            data = self.filter(album["artist"])
            for review in data:
                j += 1
                if j > 5:
                    break
                print "%s" % review
            # Sleep for API Limit
            time.sleep(15)
            j = 0
        return
