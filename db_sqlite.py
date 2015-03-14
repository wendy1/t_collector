import datetime
import os
import sqlite3

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
            (trip_number text primary key,
            tripdate timestamp default current_timestamp,
            vehicle_number text NULLABLE default NULL,
            last_trip_using_this_vehicle_number text,
            weekday text,
            line text,
            trip_id text)
            ''')
        self._disconnect_db()

    def save_route_data(self, route_data):
        self._connect_db()
        self.c = self.conn.cursor()

        try:
            self.c.execute('''
            INSERT INTO route_data (trip_number, tripdate, vehicle_number, weekday, line, trip_id)
            VALUES (?, ?, ?, ?, ?, ?)
            ''',
                           (route_data.trip_number,
                           route_data.date,
                           route_data.vehicle_number,
                           route_data.weekday,
                           route_data.line,
                           route_data.trip_id))
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

    def get_last_trip_using_same_vehicle(self, vehicle_number, this_trip_number):
        '''Returns the trip number (as a string) or None if not found'''
        self._connect_db()
        self.c = self.conn.cursor()

        self.c.execute('''
            SELECT trip_number FROM route_data
            WHERE vehicle_number=? AND trip_number != ?
            ORDER BY tripdate DESC
            LIMIT 1''',
           (vehicle_number, this_trip_number))

        l = list(self.c.fetchall())
        self._disconnect_db()

        if len(l) == 0:
            return None

        return str(l[0][0])

    def set_last_trip_using_same_vehicle(self, this_trip_number, last_trip_number):
        self._connect_db()
        self.c = self.conn.cursor()
        a = self.c.execute('''
            UPDATE route_data SET last_trip_using_this_vehicle_number=?
            WHERE trip_number=? AND date(tripdate)=date(?)
            ''',
            (last_trip_number, this_trip_number, datetime.datetime.today()))

        b = self.conn.commit()
        self._disconnect_db()

