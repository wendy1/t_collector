#!/usr/bin/env python
__author__ = 'wswanbeck'

import argparse
import datetime
import logging
import time

from db_sqlite import DB_sqlite
from db_mysql import DB_mysql

from mbta_rt import MbtaRt

def todate(datestring):
    return datetime.datetime.fromtimestamp(int(datestring))

api_key = 'jfhKC8TLdkWIsOs-DVEUGg'
logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger("LinesDataCollection")
log.setLevel(logging.INFO)

def check_and_update(db, routes, delay=2):
    log.info("--- Getting vehicle data ---")

    vdatas = MbtaRt.get_all_vehicles(routes, delay=delay)

    for vdata  in vdatas.values():
        # save this data
        log.info('Saving data for trip: %s, vehicle: %s, trip id "%s"', vdata.trip_number, vdata.vehicle_number, vdata.trip_id)
        db.save_route_data(vdata)
        # check for previous route using same train
        last_route = db.get_last_route_using_same_vehicle(vdata.vehicle_number, vdata.trip_number)
        if last_route is not None:
            log.info('  Adding last train using same vehicle: This trip is %s, last trip ws %s, vehicle was %s',
                         vdata.trip_number, last_route.trip_number, vdata.vehicle_number)
            db.set_last_trip_using_same_vehicle(vdata.trip_number, last_route.trip_number, last_route.line)


if __name__ == '__main__':

    log.info("=== Starting ===")

    # parse any arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('dbtype', choices=['sqlite', 'mysql'])
    args = parser.parse_args()

    if args.dbtype == 'sqlite':
        db = DB_sqlite('db/mbta_collection.sqlite')
    elif args.dbtype == 'mysql':
        DB = 'tcollector'
        DB_HOST = 'tcollector.swanbeck.net'
        DB_USER = 'tcollector'
        DB_PASSWORD = 'tc0llect0r'
        db = DB_mysql(DB, DB_HOST, DB_USER, DB_PASSWORD)
    else:
        raise Exception('Specify dbtype=sqlite or dbtype=mysql')


    restart_interval = datetime.timedelta(minutes=15)
    wait_between_calls_seconds = 20

    routes = MbtaRt.get_commuter_rail_routes()
    if len(routes) == 0:
        log.error("No route data available")
        exit()

    delay = 1 # first time through go faster
    while True:
        start=datetime.datetime.now()
        check_and_update(db, routes, delay=delay)
        delay = wait_between_calls_seconds # after first call, can slow down
        time_spent = datetime.datetime.now() - start
        if time_spent < restart_interval:
            time_to_wait = restart_interval - time_spent
            log.info("=== sleeping ===")
            time.sleep(time_to_wait.seconds)
