#!/usr/bin/env python
# encoding: utf-8
import sys;sys.path.append('..')
import datetime
from lines_data_collector import todate
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
                       '1426679400',
                       '1426681020',
                       'Monday')
        self.db.save_route_data(rd)

        rd = RouteData('trip_number_ttt',
                       'vehicle_number_ttt',
                       'trip_id_something_or_other',
                       'Fitchburg',
                       '1426679400',
                       '1426681020',
                       'Tuesday')
        self.db.save_route_data(rd)

    def test_get_last_trip_with_same_vehicle(self):
        # no previous trip to start with
        self.assertTrue(self.db.get_last_route_using_same_vehicle('1600', datetime.datetime.now()) is None)

        # current trip (only one so far)
        this_trip_start_time_string = '1426679400'
        rd = RouteData('331',
                       '1600',
                       'trip_id_something_or_other',
                       'Lowell',
                       this_trip_start_time_string,
                       '1426681020',
                       'Monday')
        self.db.save_route_data(rd)

        # still no previous vehicle
        last_route = self.db.get_last_route_using_same_vehicle('1600', todate(this_trip_start_time_string))
        self.assertIsNone(last_route)

        # add a previous vehicle
        previous_trip_end_time_string = str(int(this_trip_start_time_string)-1)
        previous_trip_start_time_string = str(int(previous_trip_end_time_string) -1)
        rd = RouteData('330',
                       '1600',
                       'trip_id_something_or_other',
                       'Lowell',
                       previous_trip_start_time_string,
                       previous_trip_end_time_string,
                       'Monday')
        self.db.save_route_data(rd)

        # now we find it
        last_route = self.db.get_last_route_using_same_vehicle('1600', todate(this_trip_start_time_string))
        self.assertEqual(last_route.trip_number, '330')
        self.assertEqual(last_route.line, 'Lowell')

        # but not if it's the same trip number as the current trip
        self.assertTrue(self.db.get_last_route_using_same_vehicle('1600', this_trip_start_time_string) is None)

    def test_update_last_trip_number(self):
        rd = RouteData('333',
                       '1600',
                       'trip_id_something_or_other',
                       'Lowell',
                       '1426679400',
                       '1426681020',
                       'Monday')
        self.db.save_route_data(rd)

        self.db.set_last_trip_using_same_vehicle('333', '331', 'Lowell')


if __name__ == '__main__':
    unittest.main()