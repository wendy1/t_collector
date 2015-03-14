import datetime

__author__ = 'wendy'


class RouteData:
    def __init__(self, trip_number, vehicle_number, trip_id, line, weekday):
        self.trip_number = trip_number
        self.vehicle_number = vehicle_number
        self.trip_id = trip_id
        self.weekday = weekday
        self.line = line
        self.date = datetime.date.today()