import datetime

__author__ = 'wendy'

def todate(datestring):
    return datetime.datetime.fromtimestamp(int(datestring))

class RouteData:
    def __init__(self, trip_number, vehicle_number, trip_id, line, trip_start_time, trip_end_time, weekday):
        self.trip_number = trip_number
        self.vehicle_number = vehicle_number
        self.trip_id = trip_id
        self.weekday = weekday
        self.line = line

        self.trip_start_time = trip_start_time
        if not isinstance(trip_start_time, datetime.datetime):
            self.trip_start_time = todate(self.trip_start_time)

        self.trip_end_time = trip_end_time
        if not isinstance(trip_end_time, datetime.datetime):
            self.trip_end_time = todate(self.trip_end_time)

        self.date = datetime.date.today()