from datetime import datetime, timedelta


class DatetimeInter:

    def get_datetime(self):
        """Get current date and time.

        Function returns current date and time.

        Returns
        -------
        Datetime
            Current date and time without microseconds.
        """
        d = datetime.now() - timedelta(microseconds=datetime.now().microsecond)
        return d

    def get_date(self):
        """Get current date.

        Function returns current date in 'DD Month YYYY' format.

        Returns
        -------
        Datetime
            Current date.
        """
        return datetime.date(datetime.now()).strftime('%d %b %Y')

    def get_dt_hmin(self):
        """Get current date and time.

        Function returns current date and time in 'DD Month YYYY HH:MM' format.

        Returns
        -------
        Datetime
            Current date and time without seconds.
        """
        s = timedelta(seconds=datetime.now().second)
        dt = DatetimeInter().get_datetime() - s
        return dt.strftime('%d %b %Y %H:%M')

    def create_timestamp(self):
        """Creating timestamp.

        Function gets current date and time and creates timestamp in form
        'YYYYMMDD_HHMMSS'.

        Returns
        -------
        Datetime
            Timestamp basis on current time.
        """
        return datetime.now().strftime('%Y%m%d_%H%M%S')
