#!/usr/bin/env python
# encoding: utf-8

try:
    import unittest2
    unittest = unittest2
except ImportError:
    import unittest

import urllib2
import json

class MbtaRt:
    global routes_url, vehicles_by_route_url
    api_key = 'jfhKC8TLdkWIsOs-DVEUGg'
    rt_url_base = 'http://realtime.mbta.com/developer/api/v2'
    routes_url = rt_url_base +'/routes?api_key=%s&format=json' % api_key
    vehicles_by_route_url = rt_url_base +'/vehiclesbyroute?api_key=%s&format=json&route=' % api_key # append route-id

    @classmethod
    def prt(cls, msg):
        print msg

    @classmethod
    def get_commuter_rail_routes(cls):
        '''Returns dictionary of key: route-id, value: route-name
        Or returns {} if error
        '''
        rt_data = {}

        try:
            rt_info = urllib2.urlopen(routes_url)
            rt_data = json.load(rt_info)
        except Exception as e:
            cls.prt('No route data available: ' + e.message)

        try:
            routes_list = [r for r in rt_data['mode'] if str(r['mode_name']) == 'Commuter Rail'][0]['route']
            ret = {}
            for r in routes_list:
                ret[r['route_id']] = r['route_name']

            return ret

        except Exception as e:
            cls.prt('Problem parsing route data')
            return {}

    @classmethod
    def get_all_vehicles(cls):
        '''Return all current vehicles for known routes
        or return {} if error
        '''
        routes = cls.get_commuter_rail_routes()
        if len(routes) == 0:
            return {}

        trip_vehicle = {}

        try:
            for rid in routes.keys():
                vehicle_info = urllib2.urlopen(vehicles_by_route_url + rid)
                vehicle_data = json.load(vehicle_info)
                try:
                    for dir in vehicle_data['direction']:
                        try:
                            trips = dir['trip']
                            for trip in trips:
                                try:
                                    trip_id = trip['trip_id']
                                    vehicle = trip['vehicle']['vehicle_id']
                                    # add to our data
                                    trip_vehicle[trip_id] = vehicle
                                except:
                                    pass
                        except:
                            pass
                except:
                    pass
        except Exception as e:
            cls.prt('No vehicle data available' + e.message)
            return trip_vehicle

        return trip_vehicle


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
            print "'%s': '%s'" % (vvid, vv[vvid])

if __name__ == '__main__':
    unittest.main()