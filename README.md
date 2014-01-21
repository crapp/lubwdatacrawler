lubwdatacrawler
===============

Is a software written in Python to collect data from Measurement Stations that are operated by the LUBW (Landesanstalt für Umwelt, Messungen und Naturschutz Baden-Württemberg). The data will be stored in a sqlite database

They currently offer an one hour resolution for their data (Particulate Matter, Ozone...)


Requirements
------------

* Python >= 3.2
* [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/) >= 4

Installation
------------

Just run the application with your favorite Python interpreter

> $ python3 lubwcrawler.py --url http://gather_data_from_here/index.html

General usage
-------------

After downloading the application you simply have to run lubwcrawler.py from the command line. The application offers several command line options of which one is required. After you have executed the script it will start crawling the data. You can specify a time delta in seconds that will be used to wait until the next crawling cycle is started. The data gathered will be stored in a sqlite3 database. See command line options on how to configure the application

### Command line options ###

* --version      : Prints the version of lubwcrawler
* -d --database  : Database file to use. If omitted the databse will be created in the working directory (lubw_crawler.sqlite)
* -t --parsetime : Timeout in seconds until next crawling cycle. If not provided the application will fetch the data only one time and exit after that.
* -u --url       : Comma separated list of urls the application should crawl. This option is **required**
* -V --verbose   : Print logging information (debug and info level) to stdout

> $ python3 lubwcrawler.py -d dump_all_here.sqlite -u https://crawlme.org/station.html,http://andmetoo.to/station.html -V

Database structure
------------------

Table Name is the Station Name provided by the LUBW

* ID              : INTEGER, primary key
* component       : TEXT, name of the component (Particulate Matter, Ozone, Nitrogen Dioxide...)
* current         : INTEGER, the last measured value
* daymax          : INTEGER, maximum value of this day (so far)
* yesterday_max   : INTEGER, maximum of the day before
* yesterday_mean  : INTEGER, mean of yesterdays values
* measurement_time: DATETIME, date and time of the current measurement
* timestamp       : DATETIME, insert timestamp

ToDo
----

* Add a command line option for the minimum loglevel 
* Allow logging to a file
* Improved sqlite exception handling
* Improved urllib error handling
* Add other database connectors
* Allow dumping directly into files like csv

License
-------

> This program is free software: you can redistribute it and/or modify
> it under the terms of the GNU General Public License as published by
> the Free Software Foundation, either version 3 of the License, or
> (at your option) any later version.
> 
> This program is distributed in the hope that it will be useful,
> but WITHOUT ANY WARRANTY; without even the implied warranty of
> MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
> GNU General Public License for more details.
> 
> You should have received a copy of the GNU General Public License
> along with this program.  If not, see <http://www.gnu.org/licenses/>.

Copyright
---------

(C) 2013, 2014 Christian Rapp (crapp) crappbytes<at>gmail<dot>com
