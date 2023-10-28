from datetime import datetime
import os
import csv

from dateutil.relativedelta import relativedelta

from analytics.local_dataclasses import BCHYDRO_HOURLY_KWH, Period

def read_kwh_hourly_series_from_local(start_date: datetime) -> list[tuple[datetime, float]]:

    prefix = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
    suffix = f"{BCHYDRO_HOURLY_KWH}/{start_date.date().isoformat()}.csv"
    key = os.path.join(prefix, suffix)

    time_series: list[tuple[datetime, float]] = []
    if os.path.exists(key) is False:
        return time_series
    
    with open(key, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for i, row in enumerate(spamreader):
    
            if i == 0 or i == 1:
                continue

            time_series.append((datetime.strptime(row[1], "%Y/%m/%d %X"), float(row[2])))

    return time_series

def read_kwh_hourly_series(start_date: datetime) -> list[tuple[datetime, float]]:

    return read_kwh_hourly_series_from_local(start_date)


def read_kwh_series_for_date_range(start: datetime, end: datetime) -> list[tuple[datetime, float]]:

    adjusted_start = datetime(start.year, start.month, 1)
    adjusted_end = datetime(end.year, end.month, 1)

    kwh_series = []
    loop_start = adjusted_start
    while loop_start < adjusted_end:
        kwh_series += read_kwh_hourly_series_from_local(loop_start)
        loop_start = loop_start + relativedelta(months=1)

    if len(kwh_series) == 0:
        return kwh_series
    
    return [(date, kwh) for date, kwh in kwh_series if (date >= start and date < end)]
