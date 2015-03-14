#!/usr/bin/env python
# encoding: utf-8

try:
    import unittest2
    unittest = unittest2
except ImportError:
    import unittest

import json
import logging
import urllib2


class MbtaRt:
    global routes_url, vehicles_by_route_url
    api_key = 'jfhKC8TLdkWIsOs-DVEUGg'
    rt_url_base = 'http://realtime.mbta.com/developer/api/v2'
    routes_url = rt_url_base +'/routes?api_key=%s&format=json' % api_key
    vehicles_by_route_url = rt_url_base +'/vehiclesbyroute?api_key=%s&format=json&route=' % api_key # append route-id

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

        except:
            logging.exception('Problem parsing route data')
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

        for rid in routes.keys():
            try:
                vehicle_info = urllib2.urlopen(vehicles_by_route_url + rid)
                vehicle_data = json.load(vehicle_info)
                try:
                    for dir in vehicle_data['direction']:
                        try:
                            trips = dir['trip']
                            for trip in trips:
                                try:
                                    trip_id = trip['trip_id']
                                    trip_data = cls.parse_tripid(trip_id)
                                    trip_number = trip_data['trip_number']
                                    vehicle_id = trip['vehicle']['vehicle_id']
                                    # add to our data
                                    if trip_number not in trip_vehicle:
                                        trip_vehicle[trip_number] = {}
                                    trip_vehicle[trip_number]['vehicle_id'] = vehicle_id
                                    trip_vehicle[trip_number]['trip_id'] = trip_id
                                    trip_vehicle[trip_number]['weekday'] = trip_data['weekday']
                                    trip_vehicle[trip_number]['route_name'] = trip_data['route_name']
                                except:
                                    pass
                        except:
                            pass
                except:
                    pass
            except:
                #logging.exception('No vehicle data available for route %s', rid)
                logging.error('No realtime data for %s', rid)
                pass

        return trip_vehicle

    @classmethod
    def parse_tripid(cls, tripid):
        tripidparts = tripid.split('-')
        ret = {}
        ret['trip_number'] = tripidparts[6]
        ret['weekday'] = tripidparts[3]
        ret['route_name'] = tripidparts[1]
        return ret


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