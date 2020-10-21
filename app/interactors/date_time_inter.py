from datetime import datetime, timedelta


class DatetimeInter:

    def get_datetime(self):
        ms = timedelta(microseconds=datetime.now().microsecond)
        dt = datetime.now() - ms
        return dt

    def get_date(self):
        return datetime.date(datetime.now())
