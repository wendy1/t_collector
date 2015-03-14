import urllib2
import json
import logging
from route_data import RouteData

__author__ = 'wendy'


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
                                    trip_id_data = cls.parse_tripid(trip['trip_id'])
                                    trip_vehicle[trip_id_data['trip_number']] = RouteData(
                                        trip_id_data['trip_number'],
                                        trip['vehicle']['vehicle_id'],
                                        trip['trip_id'],
                                        trip_id_data['weekday']
                                    )
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