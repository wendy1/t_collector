#!/usr/bin/env python
# encoding: utf-8

import datetime
import sys;
from route_data import RouteData

sys.path.append('.');sys.path.append('..')
from db_sqlite import DB_sqlite

try:
    import unittest2
    unittest = unittest2
except ImportError:
    import unittest


class TestDb(unittest.TestCase):

    def setUp(self):
        self.db_path = '/tmp/train_collector.sqlite'
        self.db = DB_sqlite(self.db_path)
        self.db.initialize_schema()

    def test_save_route_data(self):
        rd = RouteData('trip_number_123',
                       'vehicle_number_456',
                       'trip_id_something_or_other',
                       'Monday')
        self.db.save_route_data(rd)

        rd = RouteData('trip_number_ttt',
                       'vehicle_number_ttt',
                       'trip_id_something_or_other',
                       'Tuesday')
        self.db.save_route_data(rd)


if __name__ == '__main__':
    unittest.main()