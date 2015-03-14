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
        self.db_path = '/tmp/train_collector_unittest.sqlite'
        self.db = DB_sqlite(self.db_path)
        self.db.initialize_schema()

    def test_save_route_data(self):
        rd = RouteData('trip_number_123',
                       'vehicle_number_456',
                       'trip_id_something_or_other',
                       'Mars',
                       'Monday')
        self.db.save_route_data(rd)

        rd = RouteData('trip_number_ttt',
                       'vehicle_number_ttt',
                       'trip_id_something_or_other',
                       'Fitchburg',
                       'Tuesday')
        self.db.save_route_data(rd)

    def test_get_last_trip_with_same_vehicle(self):
        # no previous trip to start with
        self.assertTrue(self.db.get_last_trip_using_same_vehicle('1600', '333') is None)

        # previous trip 335 had this train
        rd = RouteData('331',
                       '1600',
                       'trip_id_something_or_other',
                       'Lowell',
                       'Monday')
        self.db.save_route_data(rd)

        # now we find it
        last_trip = self.db.get_last_trip_using_same_vehicle('1600', '333')
        self.assertEqual(last_trip, '331')

        # but not if it's the same trip number as the current trip
        self.assertTrue(self.db.get_last_trip_using_same_vehicle('1600', '331') is None)

    def test_update_last_trip_number(self):
        rd = RouteData('333',
                       '1600',
                       'trip_id_something_or_other',
                       'Lowell',
                       'Monday')
        self.db.save_route_data(rd)

        self.db.set_last_trip_using_same_vehicle('333', '331')


if __name__ == '__main__':
    unittest.main()