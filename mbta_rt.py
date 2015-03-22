import urllib2
import json
import logging
import time
from route_data import RouteData

__author__ = 'wendy'


class MbtaRt:
    global routes_url, vehicles_by_route_url, schedule_by_trip_url
    api_key = 'jfhKC8TLdkWIsOs-DVEUGg'
    rt_url_base = 'http://realtime.mbta.com/developer/api/v2'
    routes_url = rt_url_base +'/routes?api_key=%s&format=json' % api_key
    vehicles_by_route_url = rt_url_base +'/vehiclesbyroute?api_key=%s&format=json&route=' % api_key # append route-id
    schedule_by_trip_url = rt_url_base +'/schedulebytrip?api_key=%s&format=json&trip=' % api_key # append trip_id

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
    def get_all_vehicles(cls, routes, delay=2):
        '''Return all current vehicles for known routes
        or return {} if error
        '''
        trip_vehicle = {}

        for rid in routes.keys():
            try:
                logging.info('Requesting data for route: %s', rid)
                vehicle_info = urllib2.urlopen(vehicles_by_route_url + rid)
                vehicle_data = json.load(vehicle_info)
                logging.info('  data for route %s received.  Sleeping for %d seconds', rid, delay)

                time.sleep(delay)
                logging.info('  delay complete.  Processing data for route %s', rid)
                try:
                    for dir in vehicle_data['direction']:
                        try:
                            trips = dir['trip']
                            for trip in trips:
                                try:
                                    trip_id_data = cls.parse_tripid(trip['trip_id'])
                                    trip_schedule = cls.get_schedule_for_trip(trip['trip_id'], delay=delay)
                                    trip_vehicle[trip_id_data['trip_number']] = RouteData(
                                        trip_id_data['trip_number'],
                                        trip['vehicle']['vehicle_id'],
                                        trip['trip_id'],
                                        trip_id_data['line'],
                                        trip_schedule['stop'][0]['sch_dep_dt'],
                                        trip_schedule['stop'][len(trip_schedule['stop'])-1]['sch_arr_dt'],
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
    def get_schedule_for_trip(cls, tripid, delay=2):
        '''Get schedule information about a trip
        Note:
            trip start time is trip_data['stop'][0]
            trip end time is trip_data['stop'][len(trip_data['stop'])-1]
        '''
        trip_data = {}

        try:
            trip_info = urllib2.urlopen(schedule_by_trip_url + tripid)
            trip_data = json.load(trip_info)
            time.sleep(delay)
            try:
                pass
            except:
                pass
        except:
            #logging.exception('No vehicle data available for route %s', rid)
            logging.error('No realtime data for %s', tripid)
            pass

        return trip_data

    @classmethod
    def parse_tripid(cls, tripid):
        tripidparts = tripid.split('-')
        ret = {}
        ret['trip_number'] = tripidparts[6]
        ret['weekday'] = tripidparts[3]
        ret['line'] = tripidparts[1]
        return ret