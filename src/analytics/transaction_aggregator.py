from datetime import datetime
from collections import defaultdict

from dateutil.relativedelta import relativedelta

from analytics.local_dataclasses import(
    FinancialTransaction,
    FinancialCategory,
    FinancialSubcategory,
    FinancialTransactionType
)
from analytics.utils import aggregate_by_day

balance_key_list = [
    FinancialCategory.INCOME, FinancialCategory.LEARNING, FinancialCategory.BANKING, 
    FinancialCategory.SOCIAL, FinancialCategory.GROCERIES, FinancialCategory.LUXURIES,
    FinancialCategory.UTILITIES, FinancialCategory.CHARITY, FinancialCategory.RENT, 
    FinancialCategory.SUBSCRIPTIONS, FinancialCategory.UNRECONCILED
]

def group_by_category(transactions: list[FinancialTransaction]) -> defaultdict[FinancialCategory, float]:

    category_dictionary = defaultdict(float)
    for t in transactions:

        amount = t.amount_cad if t.transaction_type == FinancialTransactionType.INFLOW else -1 * t.amount_cad
        category_dictionary[t.category] += amount
    
    return category_dictionary

def group_by_subcategory(transactions: list[FinancialSubcategory]) -> defaultdict[FinancialSubcategory, float]:

    category_dictionary = defaultdict(int)
    for t in transactions:

        amount = t.amount_cad if t.transaction_type == FinancialTransactionType.INFLOW else -1 * t.amount_cad
        category_dictionary[t.subcategory] += amount
    
    return category_dictionary

def calculate_balance(category_dictionary: defaultdict[FinancialCategory, float]) -> float:
    
    return sum([v for k, v in category_dictionary.items() if k in balance_key_list])


def get_category_expenditures_labels_and_values(cd: defaultdict[FinancialCategory, float]) -> list[tuple[str, float]]:

    labels_and_values: list[tuple[str, float]] = []

    for k, v in cd.items():

        if (k != FinancialCategory.INCOME and k != FinancialCategory.BANKING):

            labels_and_values.append((k.name, abs(v)))

    return labels_and_values


def get_subcategory_expenditures_labels_and_values(csd: defaultdict[FinancialSubcategory, float]) -> list[tuple[str, float]]:
    labels_and_values: list[tuple[str, float]] = []
    
    for k, v in csd.items():

        if (k != FinancialSubcategory.INCOME_SALARY 
            and k != FinancialSubcategory.INCOME_TAX_RETURNS
            and k != FinancialSubcategory.INCOME_PARENTS
            and k != FinancialSubcategory.SAVINGS
            and k != FinancialSubcategory.BANKING_INTERNAL_TRANSFERS
           ):

            labels_and_values.append((k.name, abs(v)))

    return labels_and_values

def get_waterfall_labels_and_values(cd: defaultdict[FinancialCategory, float]) -> list[tuple[str, str, float]]:

    balance = calculate_balance(cd)

    measure = ["relative", "relative", "relative", 
                "relative", "relative", "relative", 
                "relative", "relative", 
                "relative", "relative", "total"]
    x = [FinancialCategory.INCOME.name, FinancialCategory.RENT.name, FinancialCategory.GROCERIES.name,
            FinancialCategory.SOCIAL.name, FinancialCategory.CHARITY.name, FinancialCategory.SUBSCRIPTIONS.name,
            FinancialCategory.LUXURIES.name, FinancialCategory.LEARNING.name, 
            FinancialCategory.BANKING.name, FinancialCategory.UNRECONCILED.name, "Balance"]
    y = [cd[FinancialCategory.INCOME], cd[FinancialCategory.RENT], cd[FinancialCategory.GROCERIES], 
            cd[FinancialCategory.SOCIAL], cd[FinancialCategory.CHARITY], cd[FinancialCategory.SUBSCRIPTIONS],
            cd[FinancialCategory.LUXURIES], cd[FinancialCategory.LEARNING],
            cd[FinancialCategory.BANKING], cd[FinancialCategory.UNRECONCILED], balance]
    
    return [(m, x1, y1) for m, x1, y1 in zip(measure, x, y)]


def get_balance_over_time(
    classified_transactions: list[FinancialTransaction],
    data_start: datetime, 
    data_end: datetime, 
    delta: relativedelta) -> list[tuple[datetime, float]]:

    balance_over_time: list[tuple[datetime, float]] = []
    start = data_start
    while start < data_end:
        end = start + delta

        classified_transactions_by_date = [t for t in classified_transactions if start <= t.date < end]
        cd = group_by_category(classified_transactions_by_date)
        balance = calculate_balance(cd)

        balance_over_time.append((start, balance))

        start = start + delta

    return balance_over_time

def get_category_over_time(
    classified_transactions: list[FinancialTransaction],
    data_start: datetime, 
    data_end: datetime, 
    delta: relativedelta) -> dict[FinancialCategory, list[tuple[datetime, float]]]:

    dict_of_lists: dict[FinancialCategory, list[tuple[datetime, float]]] = {}

    start = data_start
    while start < data_end:
        end = start + delta

        classified_transactions_by_date = [t for t in classified_transactions if start <= t.date < end]
        cd = group_by_category(classified_transactions_by_date)

        for k, v in cd.items():
            if k not in dict_of_lists.keys():
                dict_of_lists[k] = []
            dict_of_lists[k].append((start, v))

        start = start + delta

    return dict_of_lists

def get_subcategory_over_time(
    classified_transactions: list[FinancialTransaction],
    data_start: datetime, 
    data_end: datetime, 
    delta: relativedelta) -> dict[FinancialSubcategory, list[tuple[datetime, float]]]:

    dict_of_lists: dict[FinancialSubcategory, list[tuple[datetime, float]]] = {}

    start = data_start
    while start < data_end:
        end = start + delta

        classified_transactions_by_date = [t for t in classified_transactions if start <= t.date < end]
        cd = group_by_subcategory(classified_transactions_by_date)

        for k, v in cd.items():
            if k not in dict_of_lists.keys():
                dict_of_lists[k] = []
            dict_of_lists[k].append((start, v))

        start = start + delta

    return dict_of_lists


def get_daily_asset_growth_over_time(
    classified_transactions: list[FinancialTransaction],
    data_start: datetime,
    data_end: datetime,
) -> list[tuple[datetime, float]]:
    
    # turn daily transactions
    daily_transactions: list[tuple[datetime, float]] = []
    for t in classified_transactions:
        value = t.amount_cad if t.transaction_type == FinancialTransactionType.INFLOW else -1 * t.amount_cad
        daily_transactions.append((t.date, value))

    daily_transactions = aggregate_by_day(daily_transactions)

    cumulative_sum = 0.0
    asset_growth_over_time: list[tuple[datetime, float]] = []
    for d, v in daily_transactions:
        cumulative_sum += v
        asset_growth_over_time.append((d, cumulative_sum))

    return asset_growth_over_time
