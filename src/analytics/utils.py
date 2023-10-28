from datetime import datetime
from collections import defaultdict

def aggregate_by_day(series: list[tuple[datetime, float]]) -> list[tuple[datetime, float]]:

    sum_dict = defaultdict(float)
    for date, value in series:
        sum_dict[datetime(date.year, date.month, date.day)] += value

    summed_series: list[tuple[datetime, float]] = []
    for k, v in sum_dict.items():
        summed_series.append((k, v))
    
    return sorted(summed_series, key=lambda x: x[0])


def aggregate_by_month(series: list[tuple[datetime, float]]) -> list[tuple[datetime, float]]:

    sum_dict = defaultdict(float)
    for date, value in series:
        sum_dict[datetime(date.year, date.month, 1)] += value

    summed_series: list[tuple[datetime, float]] = []
    for k, v in sum_dict.items():
        summed_series.append((k, v))
    
    return sorted(summed_series, key=lambda x: x[0])