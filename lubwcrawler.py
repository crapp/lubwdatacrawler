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
import signal
import logging
import argparse as argp

from sqlite_connector import SQliteConnector
from measurement_parser import MeasurementParser


def _signal_handler(sig, frame):
    """
    A signal handler for SIGINT. Will exit the application gracefully.
    """
    signalno_name = {0: 0, 1: 'SIGHUB', 2: 'SIGINT', 3: 'SIGQUIT', 6: 'SIGABRT', 9: 'SIGKILL',
                     14: 'SIGALARM', 15: 'SIGTERM'}
    print("Script was interrupted by " + signalno_name[sig] + ", frame " + str(frame))
    sys.exit(0)


def main():
    """
    Main method used to start the application
    Instantiates the argparser and reads the command line options. The populated namespace will be
    passed around in the whole application. Additionaly we are  messing around with the root logger
    to redirect all messages to stdout and have a different Formatter.
    """
    #define a signal handler
    signal.signal(signal.SIGINT, _signal_handler)
    #build up our command line parser based on argparse
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

    #parse the arguments, this throws an exception if something goes wrong
    args = parser.parse_args()

    formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s')

    if args.verbose:
    #get the root logger
        root = logging.getLogger()
        #get a streamhandler for stdout
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)
        #create a new formatter for the streamhandler
        #formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s')
        ch.setFormatter(formatter)
        #set the
        root.addHandler(ch)
        log = logging.getLogger("my_logger")
        log.setLevel(logging.DEBUG)
    else:
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        log = logging.getLogger("my_logger")
        log.addHandler(ch)

    log.info("LUBW Data Crawler 0.1 starting...")

    db = SQliteConnector(args)
    lubwparser = MeasurementParser(args, db)
    lubwparser.crawlwebsites()

    log.info("Jobs finished, closing application")
    return 0

if __name__ == "__main__":
    main()