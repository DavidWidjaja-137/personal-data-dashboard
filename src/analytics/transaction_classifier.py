from datetime import datetime
from pprint import pprint
import json

from analytics.local_dataclasses import FinancialTransaction, FinancialCategory, FinancialSubcategory

def convert_to_financial_categories(subcategory_name: str) -> tuple[FinancialCategory, FinancialSubcategory]:

    if subcategory_name == 'unreconciled':
        return FinancialCategory.UNRECONCILED, FinancialSubcategory.UNRECONCILED
    elif subcategory_name == 'income_salary':
        return FinancialCategory.INCOME, FinancialSubcategory.INCOME_SALARY
    elif subcategory_name == 'income_tax_returns':
        return FinancialCategory.INCOME, FinancialSubcategory.INCOME_TAX_RETURNS
    elif subcategory_name == 'income_parents':
        return FinancialCategory.INCOME, FinancialSubcategory.INCOME_PARENTS
    elif subcategory_name == 'rent':
        return FinancialCategory.RENT, FinancialSubcategory.RENT
    elif subcategory_name == 'groceries':
        return FinancialCategory.GROCERIES, FinancialSubcategory.GROCERIES
    elif subcategory_name == 'utility_transport':
        return FinancialCategory.UTILITIES, FinancialSubcategory.UTILITY_TRANSPORT
    elif subcategory_name == 'utility_internet':
        return FinancialCategory.UTILITIES, FinancialSubcategory.UTILITY_INTERNET
    elif subcategory_name == 'utility_cellular':
        return FinancialCategory.UTILITIES, FinancialSubcategory.UTILITY_CELLULAR
    elif subcategory_name == 'utility_water':
        return FinancialCategory.UTILITIES, FinancialSubcategory.UTILITY_WATER
    elif subcategory_name == 'utility_electricity':
        return FinancialCategory.UTILITIES, FinancialSubcategory.UTILITY_ELECTRICITY
    elif subcategory_name == 'utility_maintenance':
        return FinancialCategory.UTILITIES, FinancialSubcategory.UTILITY_MAINTENANCE
    elif subcategory_name == 'social_food':
        return FinancialCategory.SOCIAL, FinancialSubcategory.SOCIAL_FOOD
    elif subcategory_name == 'social_other':
        return FinancialCategory.SOCIAL, FinancialSubcategory.SOCIAL_OTHER
    elif subcategory_name == 'subscription_entertainment':
        return FinancialCategory.SUBSCRIPTIONS, FinancialSubcategory.SUBSCRIPTION_ENTERTAINMENT
    elif subcategory_name == 'subscription_news':
        return FinancialCategory.SUBSCRIPTIONS, FinancialSubcategory.SUBSCRIPTION_NEWS
    elif subcategory_name == 'subscription_utility':
        return FinancialCategory.SUBSCRIPTIONS, FinancialSubcategory.SUBSCRIPTION_UTILITY
    elif subcategory_name == 'learning_books':
        return FinancialCategory.LEARNING, FinancialSubcategory.LEARNING_BOOKS
    elif subcategory_name == 'learning_lessons':
        return FinancialCategory.LEARNING, FinancialSubcategory.LEARNING_LESSONS
    elif subcategory_name == 'learning_equipment':
        return FinancialCategory.LEARNING, FinancialSubcategory.LEARNING_EQUIPMENT
    elif subcategory_name == 'learning_certifications':
        return FinancialCategory.LEARNING, FinancialSubcategory.LEARNING_CERTIFICATIONS
    elif subcategory_name == 'luxuries':
        return FinancialCategory.LUXURIES, FinancialSubcategory.LUXURIES
    elif subcategory_name == 'charity_humanitarian':
        return FinancialCategory.CHARITY, FinancialSubcategory.CHARITY_HUMANITARIAN
    elif subcategory_name == 'charity_environment':
        return FinancialCategory.CHARITY, FinancialSubcategory.CHARITY_ENVIRONMENT
    elif subcategory_name == 'charity_local':
        return FinancialCategory.CHARITY, FinancialSubcategory.CHARITY_LOCAL
    elif subcategory_name == 'charity_other':
        return FinancialCategory.CHARITY, FinancialSubcategory.CHARITY_OTHER
    elif subcategory_name == 'savings':
        return FinancialCategory.SAVINGS, FinancialSubcategory.SAVINGS
    elif subcategory_name == 'banking_internal_transfers':
        return FinancialCategory.BANKING, FinancialSubcategory.BANKING_INTERNAL_TRANSFERS
    elif subcategory_name == 'banking_withdrawals':
        return FinancialCategory.BANKING, FinancialSubcategory.BANKING_WITHDRAWALS
    elif subcategory_name == 'banking_service_charges':
        return FinancialCategory.BANKING, FinancialSubcategory.BANKING_SERVICE_CHARGES
    elif subcategory_name == 'family':
        return FinancialCategory.FAMILY, FinancialSubcategory.FAMILY
    else:
        return FinancialCategory.UNRECONCILED, FinancialSubcategory.UNRECONCILED


def get_transaction_schema(schema_file: str) -> tuple[dict[str, FinancialCategory], dict[str, FinancialSubcategory]]:

    with open(schema_file, mode='r') as f:
        transaction_schema = json.load(f)

    category_schema_dict = {}
    subcategory_schema_dict = {}
    for k, v in transaction_schema.items():
        category, subcategory = convert_to_financial_categories(k)
        for transaction_name in v:
            category_schema_dict[transaction_name] = category
            subcategory_schema_dict[transaction_name] = subcategory

    return category_schema_dict, subcategory_schema_dict

def classify_transaction_into_category(
        category_schema: dict[str, FinancialCategory],
        transaction_made_to: str
    ) -> FinancialCategory:

    category = FinancialCategory.UNRECONCILED

    if transaction_made_to in category_schema.keys():
        category = category_schema[transaction_made_to]

    return category

def classify_transaction_into_subcategory(
        subcategory_schema: dict[str, FinancialSubcategory],
        transaction_made_to: str
    ) -> FinancialSubcategory:

    subcategory = FinancialSubcategory.UNRECONCILED

    if transaction_made_to in subcategory_schema.keys():
        subcategory = subcategory_schema[transaction_made_to]

    return subcategory

def classify_transaction(
        category_schema: dict[str, FinancialCategory],
        subcategory_schema: dict[str, FinancialSubcategory],
        transaction: FinancialTransaction
    ) -> FinancialTransaction:

    return FinancialTransaction(
        date=transaction.date,
        made_to=transaction.made_to,
        amount_cad=transaction.amount_cad,
        bank_account=transaction.bank_account,
        bank_account_flow=transaction.bank_account_flow,
        transaction_type=transaction.transaction_type,
        category=classify_transaction_into_category(category_schema, transaction.made_to),
        subcategory=classify_transaction_into_subcategory(subcategory_schema, transaction.made_to)
    )

def classify_transactions(
        category_schema: dict[str, FinancialCategory],
        subcategory_schema: dict[str, FinancialSubcategory],
        transactions: list[FinancialTransaction]
    ) -> list[FinancialTransaction]:

    return [classify_transaction(category_schema, subcategory_schema, t) for t in transactions]