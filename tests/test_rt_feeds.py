#!/usr/bin/env python
# encoding: utf-8

import sys; sys.path.append('.');sys.path.append('..')

from mbta_rt import MbtaRt

try:
    import unittest2
    unittest = unittest2
except ImportError:
    import unittest


class TestResearchReporter(unittest.TestCase):

    def setUp(self):
        pass

    def test_routes(self):
        routes = MbtaRt.get_commuter_rail_routes()

        print '--- Getting list of routes ---'
        for rid in routes.keys():
            print "'%s' = '%s" % (rid, routes[rid])

    def test_get_all_vehicles(self):
        print '--- Getting vehicle data ---'
        vv = MbtaRt.get_all_vehicles()
        for vvid in vv.keys():
            td = vv[vvid]
            print "Trip: '%s', vehicle %s, weekday %s, trip id '%s'" % (vvid, td['vehicle_id'], td['weekday'], td['trip_id'])

    def test_get_trip_number_from_tripid(self):
        tripids = [
            'CR-Kingston-CR-Saturday-Kingston-Dec14-1035',
            'CR-Franklin-CR-Saturday-Franklin-Dec13-1708',
            'CR-Franklin-CR-Saturday-Franklin-Dec13-1709',
            'CR-Kingston-CR-Saturday-Kingston-Dec14-1054',
            'CR-Fitchburg-CR-Saturday-Fitchburg-Aug14-1451',
            'CR-Needham-CR-Saturday-Needham-Dec14-1607',
            'CR-Middleborough-CR-Saturday-Middleborough-Dec13-1008'
        ]

        for tripid in tripids:
            td = MbtaRt.parse_tripid(tripid)
            print "Trip number %s - trip id '%s', weekday %s, route name %s" \
                  % (td['trip_number'],tripid, td['weekday'], td['route_name'])

if __name__ == '__main__':
    unittest.main()