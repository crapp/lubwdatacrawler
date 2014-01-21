#     Data Crawler for LUBW Measurement Stations
#     Copyright (C) 2014  Christian Rapp
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.

__author__ = 'Christian Rapp'

import re
import logging
import bs4
import time
import urllib.request
import urllib.parse


class MeasurementParser:

    def __init__(self, args, db):
        self.args = args
        self.urllist = []
        self.crawl = True
        self.log = logging.getLogger("my_logger")
        self.db = db

        self._parseurls()

    def _parseurls(self):
        urls = str.split(self.args.url, ',')
        if len(urls) > 0:
            validurl = re.compile(r"^https?://.+\.html?$")
            for url in urls:
                if not re.match(validurl, url):
                    raise Exception(url + " is not a valid URL. e.g. https://myUrl.html")
                self.log.info("Found URL: " + url)
                self.urllist.append(url)
        else:
            raise Exception("URLs must be a comma separated list")

    def crawlwebsites(self):
        while self.crawl:
            self.log.info("Starting next crawl cycle...")
            starttime = time.clock()
            for url in self.urllist:
                try:
                    response = urllib.request.urlopen(url)
                    self.log.debug(url + " code: " + str(response.getcode()))
                    html = response.read()
                    #TODO: Check response code with get_code()
                    soup = bs4.BeautifulSoup(html, "html.parser")
                    print(soup)
                    #TODO: Station Name could have special characters like german umlauts. Can
                    #      sqlite safely operate with them?
                    station_name = soup.find("div", id="Name")
                    self.log.info("Station Name: " + station_name.get_text())
                    valuestable = soup.find("table", id="WerteTabelle")
                    # find all components the station is measuring. This components define the table
                    # columns in the database. additionally the parent object is the table row. we
                    # traverse all siblings in this row later to get to the current reading.
                    components = valuestable.find_all("td", class_="cell3d-ueb02")
                    self.log.debug("Found " + str(len(components)) + " components in table")
                    #get_text()
                    for c in components:
                        #get all td elements
                        rowdata = c.parent.find_all("td", class_="cell3d-dat")
                        self.log.debug("Found " + str(len(rowdata)) + " data cells in table row")
                    #print(components)
                    #all data is collected now tell the database to do its job
                    self.db.insert(station_name.get_text(), "", "")
                except urllib.error.URLError as ex:
                    self.log.error("Can not parse URL: " + url + "\n" + str(ex))
            endttime = time.clock()
            self.log.info("Crawl cycle finished in " + str(endttime-starttime) + " seconds")
            #if parsetime is set we sleep here and crawl the data once again
            if self.args.parsetime:
                self.log.debug("Sleeping for " + str(self.args.parsetime) + " seconds")
                time.sleep(self.args.parsetime)
            else:
                #exit the program...
                self.crawl = False
