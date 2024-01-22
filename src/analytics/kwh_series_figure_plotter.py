from datetime import datetime

import plotly.graph_objects as go

from analytics.local_dataclasses import Period
from analytics import kwh_series_aggregator

# bar chart of monthly kwh series

def plot_bar_chart_of_monthly_kwh_series(start: datetime, end: datetime) -> go.Figure:

    series = kwh_series_aggregator.get_kwh_time_series(start, end, Period.MONTHLY)

    dates = [d for d, v in series]
    values = [v for d, v in series]

    fig = go.Figure()

    fig.add_trace(go.Bar(x=dates, y=values, name="Monthly Kwh"))

    return fig


def plot_line_chart_of_daily_kwh_series(start: datetime, end: datetime) -> go.Figure:

    series = kwh_series_aggregator.get_kwh_time_series(start, end, Period.DAILY)

    dates = [d for d, v in series]
    values = [v for d, v in series]

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=dates, y=values, name="Daily kWh"))

    return fig


def plot_line_chart_of_hourly_kwh_series(start: datetime, end: datetime) -> go.Figure:

    series = kwh_series_aggregator.get_kwh_time_series(start, end, Period.HOURLY)

    dates = [d for d, v in series]
    values = [v for d, v in series]

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=dates, y=values, name="Hourly kWh"))

    return fig


def plot_month_to_month_comparison_of_daily_kwh_series(start: datetime, end: datetime) -> go.Figure:

    dict_of_series = kwh_series_aggregator.get_month_by_month_kwh_series(start, end)

    fig = go.Figure()

    for month_start, series in dict_of_series.items():

        dates = [d.day for d, v in series]
        values = [v for d, v in series]

        fig.add_trace(go.Scatter(x=dates, y=values, mode='lines+markers', name=month_start.strftime('%Y-%m')))

    return fig


def plot_week_to_week_comparison_of_daily_kwh_series(start: datetime, end: datetime) -> go.Figure:

    series = kwh_series_aggregator.get_kwh_time_series(start, end, Period.DAILY)

    # class every time series element as being one of monday - sunday.
    dict_of_series: dict[str, list[tuple[str, float]]] = {}
    for d, v in series:
        year_and_week_number = d.strftime("%Y-%U")
        name_of_day = d.strftime("%A")

        if year_and_week_number not in dict_of_series.keys():
            dict_of_series[year_and_week_number] = []

        dict_of_series[year_and_week_number].append((name_of_day, v))
    
    fig = go.Figure()
    for year_and_week_number, series in dict_of_series.items():

        dates = [d for d, v in series]
        values = [v for d, v in series]

        fig.add_trace(go.Scatter(x=dates, y=values, mode='lines+markers', name=year_and_week_number))

    return fig