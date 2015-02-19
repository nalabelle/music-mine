#!/usr/bin/env python

import urllib2
import json

class AppleChart:
    url = "https://itunes.apple.com/us/rss/topalbums/limit=100/explicit=true/json"

    def getList(self):
        try:
            response = urllib2.urlopen(self.url)
        except urllib2.HTTPError, err:
            # raise error here, after making error class
            print err
        data = json.load(response)
        return data

    def filter(self):
        data = self.getList()
        albumList = []
        for album in data["feed"]["entry"]:
            album = {"artist" : album["im:artist"]["label"],
                     "album"  : album["title"]["label"],
                     "date"   : album["im:releaseDate"]["label"]}
            albumList.append(album)
        return albumList

    def run(self):
        data = self.filter()
        for album in data:
             print "%s - %s (%s)" % (album["artist"],
                                     album["album"],
                                     album["date"])
        return

#chart = AppleChart()
#chart.run()
