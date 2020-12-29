from datetime import datetime, timedelta


class DatetimeInter:

    def get_datetime(self):
        ms = timedelta(microseconds=datetime.now().microsecond)
        dt = datetime.now() - ms
        return dt

    def get_date(self):
        return datetime.date(datetime.now()).strftime('%d %b %Y')

    def get_dt_hmin(self):
        s = timedelta(seconds=datetime.now().second)
        dt = DatetimeInter().get_datetime() - s
        return dt.strftime('%d %b %Y %H:%M')
