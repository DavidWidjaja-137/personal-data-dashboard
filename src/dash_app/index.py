from datetime import datetime, date
import os
from dataclasses import dataclass

from dateutil.relativedelta import relativedelta

from dash import Dash, html, dcc, State, Input, Output, callback
from dash.dash_table import DataTable
from analytics import (
    transaction_reader,
    transaction_classifier,
    transaction_aggregator,
    figure_plotter,
    kwh_series_figure_plotter
)
from analytics.local_dataclasses import FinancialTransaction, FinancialTransactionType

app = Dash(__name__)


title_banner = html.Header(
    children=html.H1("Personal Data Dashboard", style={'font-weight': 'normal'}),
    style={
        'margin': '2vh',
        'text-align': 'center',
    }
)

date_picker = dcc.DatePickerRange(
    id='date-picker',
    start_date=datetime(2022, 6, 1),
    end_date=datetime(2023, 12, 1),
    min_date_allowed=date(2022, 5, 1),
    max_date_allowed=date(2024, 1, 1),
    display_format='YYYY-MM-DD',
    style={
    }
)

view_picker_display_options = [
    "Asset Growth over Time Line Chart",
    "Monthly Categories Bar Chart",
    "Monthly Subcategories Bar Chart",
    "Expenditure Categories Pie Chart",
    "Expenditure Subcategories Pie Chart",
    "Categories Waterfall",
    "Transactions Table",
    "Monthly kWh Bar Chart",
    "Daily kWh Line Chart",
    "Hourly kWh Line Chart",
    "Month to Month kWh Comparison Line Chart",
    "Week to Week kWh Comparison Line Chart"
]

view_picker_dropdown = dcc.Dropdown(
    placeholder="Select Views",
    options=view_picker_display_options,
    multi=True,
    id='view-picker-dropdown',
    style={
        'width': '30vw',
    }
)

load_view_button = html.Button(
    children="Load Views",
    id='load-view-button',
    style={
        'width': '10vw',
    }
)

view_section = html.Div(
    children="View Section here",
    id='view-section',
    style={
        'height': '70vh',
        'overflow-y': 'scroll'
    }
)

height_slider = dcc.Slider(
    value=500,
    min=400,
    max=900,
    step=100,
    id='height-slider'
)

selectors = html.Div(
    children=[
        date_picker,
        view_picker_dropdown,
        load_view_button
    ],
    style={
        'display': 'grid',
        'grid-template-columns': '1fr 1fr 1fr',
        'margin': '5vh'
    }
)

layout = html.Div(
    children=[
        title_banner,
        selectors,
        height_slider,
        view_section
    ],
    style={
        'font-family': 'sans-serif',
        'margin-left': '10vw',
        'margin-right': '10vw'
    }
)

def render_transactions_table(classified_transactions: list[FinancialTransaction]) -> DataTable:

    # convert list of dataclasses to list of records.
    list_of_records: list[dict[str, str]] = []
    for t in classified_transactions:

        record = {
            "Date": t.date.strftime("%Y-%m-%d"),
            "Category": t.category.name,
            "Subcategory": t.subcategory.name,
            "Amount": t.amount_cad if t.transaction_type == FinancialTransactionType.INFLOW else -1 * t.amount_cad,
            "Account": t.bank_account.name,
            "Description": t.made_to[:50]
        }

        list_of_records.append(record)

    list_of_columns: list[dict[str, str]] = []
    list_of_columns.append({"name": "Date", "id": "Date"})
    list_of_columns.append({"name": "Category", "id": "Category"})
    list_of_columns.append({"name": "Subcategory", "id": "Subcategory"})
    list_of_columns.append({"name": "Amount", "id": "Amount"})
    list_of_columns.append({"name": "Account", "id": "Account"})
    list_of_columns.append({"name": "Description", "id": "Description"})

    return DataTable(
        data=list_of_records,
        columns=list_of_columns,
        filter_action='native',
        sort_action='native',
        page_action='native'
    )

@callback(
    Output('view-section', 'children'),
    Input('load-view-button', 'n_clicks'),
    Input('height-slider', 'value'),
    State('date-picker', 'start_date'),
    State('date-picker', 'end_date'),
    State('view-picker-dropdown', 'value')
)
def update_figures(n_click, height, start_date_str, end_date_str, value):

    data_start = datetime.fromisoformat(start_date_str)
    data_end = datetime.fromisoformat(end_date_str)

    category_schema, subcategory_schema = (
        transaction_classifier.get_transaction_schema(os.path.join(os.getcwd(), '..', '..', 'metadata', 'subcategory_schema.json')))
    
    all_transactions = transaction_reader.read_all_transactions_for_date_range(data_start, data_end)
    classified_transactions = transaction_classifier.classify_transactions(
        category_schema, subcategory_schema, all_transactions)

    if value is None:
        return html.Div()
    
    graph_or_tables = []
    for option in value:

        if option == 'Monthly Categories Bar Chart':
            fig = figure_plotter.plot_category_over_time_bar(classified_transactions, data_start, data_end, relativedelta(months=1))
            fig.update_layout(height=height)
            graph_or_table = dcc.Graph(figure=fig, responsive='auto')
        elif option == 'Monthly Subcategories Bar Chart':
            fig = figure_plotter.plot_subcategory_over_time_bar(classified_transactions, data_start, data_end, relativedelta(months=1))
            fig.update_layout(height=height)
            graph_or_table = dcc.Graph(figure=fig, responsive=True)
        elif option == 'Expenditure Categories Pie Chart':
            cd = transaction_aggregator.group_by_category(classified_transactions)
            fig = figure_plotter.plot_expenditures_category_pie_chart(cd)
            fig.update_layout(height=height)
            graph_or_table = dcc.Graph(figure=fig, responsive=True)
        elif option == 'Expenditure Subcategories Pie Chart':
            csd = transaction_aggregator.group_by_subcategory(classified_transactions)
            fig = figure_plotter.plot_expenditures_subcategory_pie_chart(csd)
            fig.update_layout(height=height)
            graph_or_table = dcc.Graph(figure=fig, responsive=True)
        elif option == 'Categories Waterfall':
            cd = transaction_aggregator.group_by_category(classified_transactions)
            fig = figure_plotter.plot_category_waterfall(cd)
            fig.update_layout(height=height)
            graph_or_table = dcc.Graph(figure=fig, responsive=True)
        elif option == 'Transactions Table':
            graph_or_table = render_transactions_table(classified_transactions)
        elif option == 'Monthly kWh Bar Chart':
            fig = kwh_series_figure_plotter.plot_bar_chart_of_monthly_kwh_series(data_start, data_end)
            fig.update_layout(height=height)
            graph_or_table = dcc.Graph(figure=fig, responsive=True)
        elif option == 'Daily kWh Line Chart':
            fig = kwh_series_figure_plotter.plot_line_chart_of_daily_kwh_series(data_start, data_end)
            fig.update_layout(height=height)
            graph_or_table = dcc.Graph(figure=fig, responsive=True)
        elif option == 'Hourly kWh Line Chart':
            fig = kwh_series_figure_plotter.plot_line_chart_of_hourly_kwh_series(data_start, data_end)
            fig.update_layout(height=height)
            graph_or_table = dcc.Graph(figure=fig, responsive=True)
        elif option == 'Month to Month kWh Comparison Line Chart':
            fig = kwh_series_figure_plotter.plot_month_to_month_comparison_of_daily_kwh_series(data_start, data_end)
            fig.update_layout(height=height)
            graph_or_table = dcc.Graph(figure=fig, responsive=True)
        elif option == "Week to Week kWh Comparison Line Chart":
            fig = kwh_series_figure_plotter.plot_week_to_week_comparison_of_daily_kwh_series(data_start, data_end)
            fig.update_layout(height=height)
            graph_or_table = dcc.Graph(figure=fig, responsive=True)
        elif option == "Asset Growth over Time Line Chart":
            fig = figure_plotter.plot_asset_growth_over_time(classified_transactions, data_start, data_end)
            fig.update_layout(height=height)
            graph_or_table = dcc.Graph(figure=fig, responsive=True)


        graph_or_tables.append(
            html.Div(
                children=[
                    html.H3(option),
                    graph_or_table
                ],
            )
        )

    view_layout = html.Div(children=graph_or_tables)

    return view_layout

app.layout = layout

app.run(debug=True)
