from datetime import datetime
from collections import defaultdict
import os
import csv

from dateutil.relativedelta import relativedelta

from analytics.local_dataclasses import BCHYDRO_HOURLY_KWH, Period
from analytics.kwh_series_reader import read_kwh_series_for_date_range, read_kwh_hourly_series
from analytics.utils import aggregate_by_day, aggregate_by_month



def aggregate_by_period(series: list[tuple[datetime, float]], period: Period):

    match period:
        case Period.HOURLY:
            return series
        case Period.DAILY:
            return aggregate_by_day(series)
        case Period.MONTHLY:
            return aggregate_by_month(series)
        case _:
            raise ValueError(f"{period} is not a valid period.")


def get_kwh_time_series(start: datetime, end: datetime, period: Period) -> list[tuple[datetime, float]]:

    raw_kwh_series = read_kwh_series_for_date_range(start, end)

    return aggregate_by_period(raw_kwh_series, period)


def get_month_by_month_kwh_series(start: datetime, end: datetime) -> dict[datetime, list[tuple[datetime, float]]]:

    adjusted_start = datetime(start.year, start.month, 1)
    adjusted_end = datetime(end.year, end.month, 1)

    kwh_series_dict: dict[datetime, list[tuple[datetime, float]]] = {}
    loop_start = adjusted_start
    while loop_start < adjusted_end:

        kwh_series_dict[loop_start] = aggregate_by_day(read_kwh_hourly_series(loop_start))
        loop_start = loop_start + relativedelta(months=1)

    return kwh_series_dict