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

__author__ = 'christian'

import datetime
import logging


class LoggerFilter(logging.Filter):
    # DEBUG = 0
    # INFO = 1
    # WARNING = 2
    # ERROR = 3
    #
    # def __init__(self, args):
    #     self.args = args
    #
    # def writeLog(self, lvl, msg):
    #     if self.args.verbose:
    #         dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #
    #         if lvl == Logger.DEBUG:
    #             print("[" + dt + "]" + " DEBUG: " + msg)
    def __init__(self, passlevel, reject):
        self.passlevel = passlevel
        self.reject = reject

    def filter(self, record):
        if self.reject:
            return record.levelno != self.passlevel
        else:
            return record.levelno == self.passlevel
