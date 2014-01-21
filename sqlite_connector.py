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

import sqlite3
import logging
import os

class SQliteConnector:

    def __init__(self, args):
        self.args = args
        self.log = logging.getLogger("my_logger")
        self.log.debug("Init SQLiteConnector Object")

        self.conn = sqlite3.Connection

    def insert(self, table_name, columns, values):
        self.log.debug("Insert data in Table " + table_name)
        self._open_connection()
        # ref: http://stackoverflow.com/questions/1601151/how-do-i-check-in-sqlite-whether-a-table-exists
        # SELECT name FROM sqlite_master WHERE type='table' AND name='table_name';
        #FIXME: Replace Umlauts in Table Name
        parameters = [table_name]
        curs = self.conn.cursor()
        curs.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", parameters)
        #print(curs.fetchone())
        if curs.fetchone() is None:
            self.log.debug("Table " + table_name + " does not exist")
            createtable = "CREATE TABLE " + table_name + "(ID INTEGER PRIMARY KEY AUTOINCREMENT, "
            for col in columns:
                createtable += col + " INTEGER, "
            createtable += "measurement_time DATETIME, "
            createtable += "timestamp DATETIME DEFAULT CURRENT_TIMESTAMP);"
            curs.execute(createtable)

        insertstmt = "INSERT INTO " + table_name + "("
        for col in columns:
            insertstmt += col + ", "
        self.log.debug("Committing changes")
        self.conn.commit()
        self.log.debug("Closing database")
        self.conn.close()

    def _open_connection(self):
        self.log.debug("Opening database " + self.args.database)
        if not os.path.isfile(self.args.database):
            self.log.debug("Database file does not exist")
            if not os.path.isdir(os.path.dirname(self.args.database)) and \
               os.path.dirname(self.args.database) != '':
                try:
                    os.makedirs(os.path.dirname(self.args.database))
                except OSError as ex:
                    self.log.error("Could not create Directory for Database " + str(ex))
                    raise
        self.conn = sqlite3.connect(self.args.database)
        self.log.debug("Database open")



