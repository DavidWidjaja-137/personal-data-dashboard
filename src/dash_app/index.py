from datetime import datetime, date
import os
from dataclasses import dataclass

from dateutil.relativedelta import relativedelta

from dash import Dash, html, dcc, State, Input, Output, callback
from analytics import transaction_reader, transaction_classifier, transaction_aggregator, figure_plotter

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
    end_date=datetime(2023, 9, 1),
    min_date_allowed=date(2022, 5, 1),
    max_date_allowed=date(2024, 1, 1),
    display_format='YYYY-MM-DD',
    style={
    }
)

view_picker_display_options = [
    "Monthly Balance Line Plot",
    "Monthly Categories Line Plot",
    "Monthly Subcategories Line Plot",
    "Monthly Categories Bar Chart",
    "Monthly Subcategories Bar Chart",
    "Expenditure Categories Pie Chart",
    "Expenditure Subcategories Pie Chart",
    "Categories Waterfall"
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
        view_section
    ],
    style={
        'font-family': 'sans-serif',
        'margin-left': '10vw',
        'margin-right': '10vw'
    }
)

# on click the load view buttons, display charts

@callback(
    Output('view-section', 'children'),
    Input('load-view-button', 'n_clicks'),
    State('date-picker', 'start_date'),
    State('date-picker', 'end_date'),
    State('view-picker-dropdown', 'value')
)
def update_figures(n_click, start_date_str, end_date_str, value):

    data_start = datetime.fromisoformat(start_date_str)
    data_end = datetime.fromisoformat(end_date_str)

    category_schema, subcategory_schema = (
        transaction_classifier.get_transaction_schema(os.path.join(os.getcwd(), '..', '..', 'metadata', 'subcategory_schema.json')))
    
    all_transactions = transaction_reader.read_all_transactions_for_date_range(data_start, data_end)
    classified_transactions = transaction_classifier.classify_transactions(
        category_schema, subcategory_schema, all_transactions)

    if value is None:
        return html.Div()

    graphs = []
    for option in value:

        if option == 'Monthly Balance Line Plot':
            fig = figure_plotter.plot_balance_over_time(classified_transactions, data_start, data_end, delta=relativedelta(months=1))
        elif option == 'Monthly Categories Line Plot':
            fig = figure_plotter.plot_all_categories_over_time(classified_transactions, data_start, data_end, relativedelta(months=1))
        elif option == 'Monthly Subcategories Line Plot':
            fig = figure_plotter.plot_all_subcategories_over_time(classified_transactions, data_start, data_end, relativedelta(months=1))
        elif option == 'Monthly Categories Bar Chart':
            fig = figure_plotter.plot_category_over_time_bar(classified_transactions, data_start, data_end, relativedelta(months=1))
        elif option == 'Monthly Subcategories Bar Chart':
            fig = figure_plotter.plot_all_subcategories_over_time(classified_transactions, data_start, data_end, relativedelta(months=1))
        elif option == 'Expenditure Categories Pie Chart':
            cd = transaction_aggregator.group_by_category(classified_transactions)
            fig = figure_plotter.plot_expenditures_category_pie_chart(cd)
        elif option == 'Expenditure Subcategories Pie Chart':
            csd = transaction_aggregator.group_by_subcategory(classified_transactions)
            fig = figure_plotter.plot_expenditures_subcategory_pie_chart(csd)
        elif option == 'Categories Waterfall':
            cd = transaction_aggregator.group_by_category(classified_transactions)
            fig = figure_plotter.plot_category_waterfall(cd)

        graphs.append(
            html.Div(
                children=[
                    html.H3(option),
                    dcc.Graph(figure=fig, responsive=True)
                ],
                style={'height': '50vh'}
            )
        )

    view_layout = html.Div(children=graphs)

    return view_layout

app.layout = layout

app.run(debug=True)
