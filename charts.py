#!/usr/bin/env python

import urllib2

class AppleChart:
    import json
    url = "https://itunes.apple.com/us/rss/topalbums/limit=100/explicit=true/json"

    def getList(self):
        try:
            response = urllib2.urlopen(self.url)
        except urllib2.HTTPError, err:
            # raise error here, after making error class
            print err
        data = self.json.load(response)
        return data

    def filter(self):
        data = self.getList()
        albumList = []
        for album in data["feed"]["entry"]:
            album = {"artist" : album["im:artist"]["label"],
                     "album"  : album["im:name"]["label"],
                     "date"   : album["im:releaseDate"]["label"]}
            albumList.append(album)
        return albumList

class BillboardChart:
    from bs4 import BeautifulSoup
    url = "http://www.billboard.com/charts/billboard-200"

    def getList(self):
        try:
            response = urllib2.urlopen(self.url)
            soup = self.BeautifulSoup(response)
        except urllib2.HTTPError, err:
            # raise error here, after making error class
            print err
        data = []
        for row in soup.select(".chart-row > .row-primary > .row-title"):
            album = {"artist": row.h3.a.get_text().strip(),
                     "album":   row.h2.get_text().strip(),
                     "date":    None}
            data.append(album)
        return data

    def filter(self):
        return self.getList()

