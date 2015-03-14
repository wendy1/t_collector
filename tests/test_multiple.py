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
        self.db_path = '/tmp/train_collector.sqlite'
        self.db = DB_sqlite(self.db_path)
        self.db.initialize_schema()

    def test_get_andsave_route_data(self):
        print "--- Getting vehicle data ---"
        vdatas = MbtaRt.get_all_vehicles()
        for vdata  in vdatas.values():
            self.db.save_route_data(vdata)


if __name__ == '__main__':
    unittest.main()