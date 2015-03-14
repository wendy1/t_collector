import os
import sqlite3

__author__ = 'wendy'


class DB_sqlite:

    def __init__(self, db_path):
        self.db_path = db_path

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
            date timestamp default current_timestamp,
            vehicle_number text,
            weekday text)
            ''')
        self._disconnect_db()

    def save_route_data(self, route_data):
        self._connect_db()
        self.c = self.conn.cursor()

        try:
            self.c.execute('''
            INSERT INTO route_data (trip_number, date, vehicle_number, weekday)
            VALUES (?, ?, ?, ?)
            ''',
                           (route_data.trip_number,
                           route_data.date,
                           route_data.vehicle_number,
                           route_data.weekday))
        except sqlite3.IntegrityError:
            self.c.execute('''
            UPDATE route_data SET vehicle_number=?, weekday=?
            WHERE trip_number=? AND date=?
            ''',
                           (route_data.vehicle_number,
                           route_data.weekday,
                           route_data.trip_number,
                           route_data.date))

        self.conn.commit()
        self._disconnect_db()