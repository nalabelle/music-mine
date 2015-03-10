#!/usr/bin/env python

import urllib2
import json
import feedparser
import time

class EchoNest:
    url = "http://developer.echonest.com/artist/%s/reviews.rss?api_key=%s"
    apiKey = ""

    def __init__(self, key):
        self.apiKey = key

    def getList(self, artist):
        try:
            #url = self.url % (urllib2.quote(artist.replace(' ', '+'), safe="+"), self.apiKey)
            url = self.url % (artist.replace(' ', '+').encode('utf-8'), self.apiKey)
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
