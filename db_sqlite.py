import datetime
import os
import sqlite3
from route_data import RouteData

__author__ = 'wendy'


class DB_sqlite:

    def __init__(self, db_path):
        self.db_path = db_path
        if not os.path.exists(self.db_path):
            self.initialize_schema()


    def _connect_db(self):
        self.conn = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)

    def _disconnect_db(self):
        self.conn.close()

    def initialize_schema(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

        self._connect_db()
        self.c = self.conn.cursor()

        # create tables
        self.c.execute('''CREATE TABLE if not exists route_data
            (trip_key text primary key,
            trip_number text,
            tripdate timestamp default current_timestamp,
            vehicle_number text NULLABLE default NULL,
            last_trip_using_this_vehicle_number text,
            last_trip_name text,
            weekday text,
            line text,
            trip_id text,
            trip_start_time timestamp,
            trip_end_time timestamp)
            ''')
        self._disconnect_db()

    def _make_trip_key(self, trip_number, trip_date):
        return str(trip_number) + ' ' + str(trip_date)

    def save_route_data(self, route_data):
        self._connect_db()
        self.c = self.conn.cursor()

        try:
            self.c.execute('''
            INSERT INTO route_data (trip_key, trip_number, tripdate, vehicle_number, weekday, line, trip_id, trip_start_time, trip_end_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''',
                           (self._make_trip_key(route_data.trip_number, route_data.date),
                            route_data.trip_number,
                           route_data.date,
                           route_data.vehicle_number,
                           route_data.weekday,
                           route_data.line,
                           route_data.trip_id,
                           route_data.trip_start_time,
                           route_data.trip_end_time))
        except sqlite3.IntegrityError:
            self.c.execute('''
            UPDATE route_data SET vehicle_number=?, weekday=?, line=?, trip_id=?
            WHERE trip_number=? AND tripdate=?
            ''',
                           (route_data.vehicle_number,
                           route_data.weekday,
                           route_data.line,
                           route_data.trip_id,
                           route_data.trip_number,
                           route_data.date))

        self.conn.commit()
        self._disconnect_db()

    def get_last_route_using_same_vehicle(self, vehicle_number, this_trip_start_time):
        '''Returns the trip number (as a string) or None if not found'''
        self._connect_db()
        self.c = self.conn.cursor()

        self.c.execute('''
            SELECT trip_number, line, trip_id, trip_start_time, trip_end_time, weekday FROM route_data
            WHERE vehicle_number=? AND trip_end_time < ?
            ORDER BY trip_end_time DESC
            LIMIT 1''',
           (vehicle_number, this_trip_start_time))

        l = list(self.c.fetchall())
        self._disconnect_db()

        if len(l) == 0:
            return None

        (trip_number, line, trip_id, start_time, end_time, weekday) = l[0]

        return RouteData(trip_number, vehicle_number, trip_id, line, start_time, end_time, weekday)

    def set_last_trip_using_same_vehicle(self, this_trip_number, last_trip_number, last_trip_name):
        self._connect_db()
        self.c = self.conn.cursor()
        a = self.c.execute('''
            UPDATE route_data SET last_trip_using_this_vehicle_number=?, last_trip_name=?
            WHERE trip_number=? AND date(tripdate)=date(?)
            ''',
            (last_trip_number, last_trip_name, this_trip_number, datetime.datetime.today()))

        b = self.conn.commit()
        self._disconnect_db()

