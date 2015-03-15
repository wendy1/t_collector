#!/usr/bin/env python
# encoding: utf-8

import datetime
import sys;
from route_data import RouteData

sys.path.append('.');sys.path.append('..')
from db_sqlite import DB_sqlite
from mbta_rt import MbtaRt


try:
    import unittest2
    unittest = unittest2
except ImportError:
    import unittest


class TestMultipleThings(unittest.TestCase):

    def setUp(self):
        self.db_path = '/tmp/train_collector_unittest.sqlite'
        self.db = DB_sqlite(self.db_path)
        self.db.initialize_schema()

    def test_get_andsave_route_data(self):
        print "--- Getting vehicle data ---"
        routes = MbtaRt.get_commuter_rail_routes()

        vdatas = MbtaRt.get_all_vehicles(routes)
        for vdata  in vdatas.values():
            # save this data
            self.db.save_route_data(vdata)
            # check for previous route using same train
            last_route = self.db.get_last_route_using_same_vehicle(vdata.vehicle_number, vdata.trip_number)
            if last_route is not None:
                self.db.set_last_trip_using_same_vehicle(vdata.trip_number, last_route.trip_number, last_route.line)


if __name__ == '__main__':
    unittest.main()