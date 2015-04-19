import datetime
import os
try:
    import MySQLdb
except:
    pass

from route_data import RouteData

__author__ = 'wendy'


class DB_mysql:

    def __init__(self, db, db_host, db_user, db_password):
        self.db = db
        self.db_host = db_host
        self.db_user = db_user
        self.db_password = db_password

        self.initialize_schema()


    def _connect_db(self):
        self.conn = MySQLdb.Connection(db=self.db, host=self.db_host, user=self.db_user,passwd=self.db_password)

    def _disconnect_db(self):
        self.conn.close()

    def initialize_schema(self):
        self._connect_db()
        self.c = self.conn.cursor()

        # create tables
        self.c.execute('''CREATE TABLE if not exists route_data
            (trip_key varchar(128) primary key,
            trip_number text,
            tripdate timestamp default current_timestamp,
            vehicle_number text NULL default NULL,
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
            VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
        except:
            self.c.execute('''
            UPDATE route_data SET vehicle_number=%s, weekday=%s, line=%s, trip_id=%s
            WHERE trip_number=%s AND tripdate=%s
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

        self.c.execute(
            '''
            SELECT trip_number, line, trip_id, trip_start_time, trip_end_time, weekday FROM route_data
                WHERE vehicle_number=%s AND trip_end_time < %s
                ORDER BY trip_end_time DESC
                LIMIT 1
            ''',
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
            UPDATE route_data SET last_trip_using_this_vehicle_number=%s, last_trip_name=%s
            WHERE trip_number=%s AND date(tripdate)=date(%s)
            ''',
            (last_trip_number, last_trip_name, this_trip_number, datetime.datetime.today()))

        b = self.conn.commit()
        self._disconnect_db()

