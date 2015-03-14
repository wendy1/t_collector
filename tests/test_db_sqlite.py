#!/usr/bin/env python
# encoding: utf-8

import sys; sys.path.append('.');sys.path.append('..')

#from mbta_rt import MbtaRt

try:
    import unittest2
    unittest = unittest2
except ImportError:
    import unittest

import sqlite3
class DB_sqlite:

    def __init__(self, db_path):
        self.db_path = db_path

    def initialize_schema(self):
        self.conn = sqlite3.connect(self.db_path,
                                    detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        self.c = self.conn.cursor()

        # create tables
        self.c.execute('''CREATE TABLE if not exists route_data
            (trip_number text primary key,
            date timestamp default current_timestamp,
            vehicle_number text,
            weekday text)
            ''')
        self.conn.close()

    def save_route_data(self, route_data):
        pass

class TestResearchReporter(unittest.TestCase):

    def setUp(self):
        pass

    def test_create_db(self):
        db = DB_sqlite('/tmp/train_collector.sqlite')
        db.initialize_schema()


if __name__ == '__main__':
    unittest.main()