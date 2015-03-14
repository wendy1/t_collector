
__author__ = 'wswanbeck'

import datetime
import logging
import time

from db_sqlite import DB_sqlite
from mbta_rt import MbtaRt

def todate(datestring):
    return datetime.datetime.fromtimestamp(int(datestring))

api_key = 'jfhKC8TLdkWIsOs-DVEUGg'
log = logging.getLogger("LinesDataCollection")
log.setLevel(logging.INFO)

def check_and_update(db_path):
    log.info("--- Getting vehicle data ---")

    vdatas = MbtaRt.get_all_vehicles()
    db = DB_sqlite(db_path)

    for vdata  in vdatas.values():
        # save this data
        log.info('Saving data for trip: %s, vehicle: %s, trip id "%s"', vdata.trip_number, vdata.vehicle_number, vdata.trip_id)
        db.save_route_data(vdata)
        # check for previous route using same train
        last_trip_number = db.get_last_trip_using_same_vehicle(vdata.vehicle_number, vdata.trip_number)
        if last_trip_number is not None:
            log.info('  Adding last train using same vehicle: This trip is %s, last trip ws %s, vehicle was %s',
                         vdata.trip_number, last_trip_number, vdata.vehicle_number)
            db.set_last_trip_using_same_vehicle(vdata.trip_number, last_trip_number)


if __name__ == '__main__':
    log.info("=== Starting ===")
    while True:
        check_and_update('/tmp/mbta_collection.sqlite')
        log.info("=== sleeping 15 minutes ===")
        time.sleep(15 * 60)