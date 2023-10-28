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


def plot_month_to_month_comparison_of_daily_kwh_series(start: datetime, end: datetime) -> go.Figure:

    dict_of_series = kwh_series_aggregator.get_month_by_month_kwh_series(start, end)

    fig = go.Figure()

    for month_start, series in dict_of_series.items():

        dates = [d.day for d, v in series]
        values = [v for d, v in series]

        fig.add_trace(go.Scatter(x=dates, y=values, mode='lines+markers', name=month_start.strftime('%Y-%m')))

    return fig