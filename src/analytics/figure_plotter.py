
from datetime import datetime

from dateutil.relativedelta import relativedelta
import plotly.graph_objects as go

from analytics.local_dataclasses import FinancialCategory, FinancialSubcategory, FinancialTransaction
from analytics import transaction_aggregator


def plot_expenditures_category_pie_chart(cd: dict[FinancialCategory, float]) -> go.Figure:

    lables_and_values = transaction_aggregator.get_category_expenditures_labels_and_values(cd)
    labels = [l for l, v in lables_and_values]
    values = [v for l, v in lables_and_values]

    return go.Figure(data=[go.Pie(labels=labels, values=values)])


def plot_expenditures_subcategory_pie_chart(csd: dict[FinancialSubcategory, float]) -> go.Figure:

    lables_and_values = transaction_aggregator.get_subcategory_expenditures_labels_and_values(csd)
    labels = [l for l, v in lables_and_values]
    values = [v for l, v in lables_and_values]

    return go.Figure(data=[go.Pie(labels=labels, values=values)])


def plot_category_waterfall(cd: dict[FinancialCategory, float]) -> go.Figure:

    waterfall_labels_and_values = transaction_aggregator.get_waterfall_labels_and_values(cd)
    measure = [m for m, l, v in waterfall_labels_and_values]
    labels = [l for m, l, v in waterfall_labels_and_values]
    values = [v for m, l, v in waterfall_labels_and_values]

    return go.Figure(go.Waterfall(
        name = "20", 
        orientation = "v",
        measure = measure,
        x = labels,
        y = values
    ))

def plot_balance_over_time(
    classified_transactions: list[FinancialTransaction],
    data_start: datetime,
    data_end: datetime,
    delta: relativedelta) -> go.Figure:

    balance_over_time = transaction_aggregator.get_balance_over_time(classified_transactions, data_start, data_end, delta)
    time = [t for t, b in balance_over_time]
    balance = [b for t, b in balance_over_time]

    return go.Figure(go.Scatter(x=time, y=balance))

def plot_all_categories_over_time(
    classified_transactions: list[FinancialTransaction],
    data_start: datetime,
    data_end: datetime,
    delta: relativedelta,  
) -> go.Figure:
    
    category_over_time_dict = transaction_aggregator.get_category_over_time(classified_transactions, data_start, data_end, delta)

    fig = go.Figure()

    for k, category_over_time in category_over_time_dict.items():
        time = [t for t, b in category_over_time]
        kpi = [b for t, b in category_over_time]

        fig.add_trace(go.Scatter(x=time, y=kpi, mode='lines+markers', name=k.name))

    return fig


def plot_all_subcategories_over_time(
    classified_transactions: list[FinancialTransaction],
    data_start: datetime,
    data_end: datetime,
    delta: relativedelta,  
) -> go.Figure:
    
    category_over_time_dict = transaction_aggregator.get_subcategory_over_time(classified_transactions, data_start, data_end, delta)

    fig = go.Figure()

    for k, category_over_time in category_over_time_dict.items():
        time = [t for t, b in category_over_time]
        kpi = [b for t, b in category_over_time]

        fig.add_trace(go.Scatter(x=time, y=kpi, mode='lines+markers', name=k.name))

    return fig


def plot_category_over_time_bar(
    classified_transactions: list[FinancialTransaction],
    data_start: datetime,
    data_end: datetime,
    delta: relativedelta,  
) -> go.Figure:
    
    category_over_time_dict = transaction_aggregator.get_category_over_time(classified_transactions, data_start, data_end, delta)

    fig = go.Figure()

    for k, category_over_time in category_over_time_dict.items():
        time = [t for t, b in category_over_time]
        kpi = [b for t, b in category_over_time]

        fig.add_trace(go.Bar(name=k.name, x=time, y=kpi))

    # Change the bar mode
    fig.update_layout(barmode='relative')
    
    return fig

def plot_subcategory_over_time_bar(
    classified_transactions: list[FinancialTransaction],
    data_start: datetime,
    data_end: datetime,
    delta: relativedelta,  
) -> go.Figure:
    
    category_over_time_dict = transaction_aggregator.get_subcategory_over_time(classified_transactions, data_start, data_end, delta)

    fig = go.Figure()

    for k, category_over_time in category_over_time_dict.items():
        time = [t for t, b in category_over_time]
        kpi = [b for t, b in category_over_time]

        fig.add_trace(go.Bar(name=k.name, x=time, y=kpi))

    # Change the bar mode
    fig.update_layout(barmode='relative')
    
    return fig