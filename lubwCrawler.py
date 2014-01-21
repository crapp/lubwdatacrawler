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

import sys
import logging
import argparse as argp

from sqlite_connector import SQliteConnector
from measurement_parser import MeasurementParser


def main():
    parser = argp.ArgumentParser(description="LUBW Data Crawler")
    parser.add_argument('--version', action='version', version='%(prog)s 0.1')
    parser.add_argument("-d", "--database", default="lubw_crawler.sqlite",
                        help="SQlite Database file to use. Will be generated if it does not exist")
    parser.add_argument("-t", "--parsetime", type=int,
                        help="Time in seconds to query the websites")
    parser.add_argument("-u", "--url",
                        help="Url(s) of the Measurement Station(s) (comma separated list)",
                        required=True)
    parser.add_argument("-V", "--verbose", action='store_true', default=False,
                        help="Be verbose and print messages to stdout")

    args = parser.parse_args()

    root = logging.getLogger()

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)

    log = logging.getLogger("my_logger")
    log.setLevel(logging.DEBUG)
    log.info("LUBW Data Crawler 0.1 starting...")

    db = SQliteConnector(args)
    lubwparser = MeasurementParser(args, db)
    lubwparser.crawlwebsites()

    log.info("Jobs finished, closing application")
    return 0

if __name__ == "__main__":
    main()