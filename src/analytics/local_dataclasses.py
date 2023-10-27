
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class Account(Enum):
    CTFS_CREDIT = 'ctfs-credit'
    SCOTIABANK_CHEQUING = 'scotiabank-chequing'
    SCOTIABANK_CREDIT = 'scotiabank-credit'
    VANCITY_CHEQUING = 'vancity-chequing'
    VANCITY_CREDIT = 'vancity-credit'

class AccountFlow(Enum):
    DEBIT = 0
    CREDIT = 1

class FinancialTransactionType(Enum):
    
    # anything that makes david have more money
    INFLOW = 0

    # anything that makes david have less money
    OUTFLOW = 1

    # transactions between accounts
    INTERNAL = 2

class FinancialCategory(Enum):
    UNRECONCILED = 0
    INCOME = 1
    RENT = 2
    GROCERIES = 3
    UTILITIES = 4
    SOCIAL = 5
    SUBSCRIPTIONS = 6
    LEARNING = 7
    LUXURIES = 8
    CHARITY = 9
    SAVINGS = 10
    BANKING = 11
    FAMILY = 12

class FinancialSubcategory(Enum):
    UNRECONCILED = 0

    INCOME_SALARY = 1
    INCOME_TAX_RETURNS = 2
    INCOME_PARENTS = 3

    RENT = 4
    GROCERIES = 5

    UTILITY_TRANSPORT = 6
    UTILITY_INTERNET = 7
    UTILITY_CELLULAR = 8
    UTILITY_WATER = 9
    UTILITY_ELECTRICITY = 10
    UTILITY_MAINTENANCE = 11

    SOCIAL_FOOD = 12
    SOCIAL_OTHER = 13

    SUBSCRIPTION_ENTERTAINMENT = 14
    SUBSCRIPTION_NEWS = 15
    SUBSCRIPTION_UTILITY = 16

    LEARNING_BOOKS = 17
    LEARNING_LESSONS = 18
    LEARNING_EQUIPMENT = 19
    LEARNING_CERTIFICATIONS = 20

    LUXURIES = 21
    
    CHARITY_HUMANITARIAN = 22
    CHARITY_ENVIRONMENT = 23
    CHARITY_LOCAL = 24
    CHARITY_OTHER = 25

    SAVINGS = 26

    BANKING_INTERNAL_TRANSFERS = 27
    BANKING_WITHDRAWALS = 28
    BANKING_SERVICE_CHARGES = 29

    FAMILY = 30


@dataclass
class FinancialTransaction:
    date: datetime
    made_to: str
    amount_cad: float

    bank_account: Account
    bank_account_flow: AccountFlow

    # convert into accounting flows?
    # this will do for now.
    transaction_type: FinancialTransactionType

    category: FinancialCategory = FinancialCategory.UNRECONCILED
    subcategory: FinancialSubcategory = FinancialSubcategory.UNRECONCILED

