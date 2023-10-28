from datetime import datetime
import os
import csv

from dateutil.relativedelta import relativedelta

from analytics.local_dataclasses import (
    FinancialTransaction,
    FinancialTransactionType,
    Account,
    AccountFlow,
)

def read_row_from_vancity_credit(row):
    date = datetime.fromisoformat(row[2].strip())
    made_to = str(row[4].strip())
    amount = float(row[6])
    
    bank_account_flow = AccountFlow.CREDIT if amount > 0 else AccountFlow.DEBIT
    transaction_type = FinancialTransactionType.OUTFLOW if amount > 0 else FinancialTransactionType.INFLOW

    return FinancialTransaction(
        date=date,
        made_to=made_to,
        amount_cad=abs(amount),
        bank_account=Account.VANCITY_CREDIT,
        bank_account_flow=bank_account_flow,
        transaction_type=transaction_type
    )

def read_row_from_vancity_chequing(row):
    date = datetime.strptime(row[1], "%d-%b-%Y")
    made_to = str(row[2].strip())

    if row[4] != '':
        amount = float(row[4])
        bank_account_flow = AccountFlow.CREDIT
        transaction_type = FinancialTransactionType.OUTFLOW
    else:
        amount = float(row[5])
        bank_account_flow = AccountFlow.DEBIT
        transaction_type = FinancialTransactionType.INFLOW

    return FinancialTransaction(
        date=date,
        made_to=made_to,
        amount_cad=abs(amount),
        bank_account=Account.VANCITY_CHEQUING,
        bank_account_flow=bank_account_flow,
        transaction_type=transaction_type
    )


def read_row_from_vancity_savings(row):

    date = datetime.strptime(row[1], "%d-%b-%Y")
    made_to = str(row[2].strip())

    if row[4] != '':
        amount = float(row[4])
        bank_account_flow = AccountFlow.CREDIT
        transaction_type = FinancialTransactionType.OUTFLOW
    elif row[5] != '':
        amount = float(row[5])
        bank_account_flow = AccountFlow.DEBIT
        transaction_type = FinancialTransactionType.INFLOW
    else:
        amount = 0.0
        bank_account_flow = AccountFlow.DEBIT
        transaction_type = FinancialTransactionType.INFLOW

    return FinancialTransaction(
        date=date,
        made_to=made_to,
        amount_cad=abs(amount),
        bank_account=Account.VANCITY_SAVINGS,
        bank_account_flow=bank_account_flow,
        transaction_type=transaction_type
    )

def read_row_from_scotiabank_credit(row):
    month, day, year = row[0].split('/')
    date = datetime(int(year), int(month), int(day))
    made_to = str(row[1].strip())
    amount = float(row[2])

    bank_account_flow = AccountFlow.CREDIT if amount < 0 else AccountFlow.DEBIT
    transaction_type = FinancialTransactionType.OUTFLOW if amount < 0 else FinancialTransactionType.INFLOW

    return FinancialTransaction(
        date=date,
        made_to=made_to,
        amount_cad=abs(amount),
        bank_account=Account.SCOTIABANK_CREDIT,
        bank_account_flow=bank_account_flow,
        transaction_type=transaction_type
    )

def read_row_from_scotiabank_chequing(row):
    month, day, year = row[0].split('/')
    date = datetime(int(year), int(month), int(day))
    made_to = str(row[3].strip()) + " " + str(row[4].strip())
    amount = float(row[1])

    bank_account_flow = AccountFlow.CREDIT if amount < 0 else AccountFlow.DEBIT
    transaction_type = FinancialTransactionType.OUTFLOW if amount < 0 else FinancialTransactionType.INFLOW

    return FinancialTransaction(
        date=date,
        made_to=made_to,
        amount_cad=abs(amount),
        bank_account=Account.SCOTIABANK_CHEQUING,
        bank_account_flow=bank_account_flow,
        transaction_type=transaction_type
    )


def read_row_from_scotiabank_savings(row):
    date = datetime.fromisoformat(row[0].strip())
    made_to = str(row[1].strip())
    amount = float(row[2].replace(',', ''))

    bank_account_flow = AccountFlow.DEBIT if amount > 0 else AccountFlow.CREDIT
    transaction_type = FinancialTransactionType.INFLOW if amount > 0 else FinancialTransactionType.OUTFLOW

    return FinancialTransaction(
        date=date,
        made_to=made_to,
        amount_cad=abs(amount),
        bank_account=Account.SCOTIABANK_SAVINGS,
        bank_account_flow=bank_account_flow,
        transaction_type=transaction_type
    )  


def read_row_from_credential_asset_management(row):
    date = datetime.fromisoformat(row[0].strip())
    made_to = str(row[1].strip())
    amount = float(row[2].replace(',', ''))

    bank_account_flow = AccountFlow.DEBIT if amount > 0 else AccountFlow.CREDIT
    transaction_type = FinancialTransactionType.INFLOW if amount > 0 else FinancialTransactionType.OUTFLOW

    return FinancialTransaction(
        date=date,
        made_to=made_to,
        amount_cad=abs(amount),
        bank_account=Account.CREDENTIAL_ASSET_MANAGEMENT,
        bank_account_flow=bank_account_flow,
        transaction_type=transaction_type
    )  

def read_row_from_ctfs_credit(row):
    date = datetime.fromisoformat(row[0].strip())
    made_to = str(row[1].strip())
    amount = float(row[2].replace(',', ''))

    bank_account_flow = AccountFlow.CREDIT if amount > 0 else AccountFlow.DEBIT
    transaction_type = FinancialTransactionType.OUTFLOW if amount > 0 else FinancialTransactionType.INFLOW

    return FinancialTransaction(
        date=date,
        made_to=made_to,
        amount_cad=abs(amount),
        bank_account=Account.SCOTIABANK_CHEQUING,
        bank_account_flow=bank_account_flow,
        transaction_type=transaction_type
    )

def read_row_from_account(row, statement_source):
    if statement_source == Account.CTFS_CREDIT:
        return read_row_from_ctfs_credit(row)
    elif statement_source == Account.SCOTIABANK_CHEQUING:
        return read_row_from_scotiabank_chequing(row)
    elif statement_source == Account.SCOTIABANK_CREDIT:
        return read_row_from_scotiabank_credit(row)
    elif statement_source == Account.SCOTIABANK_SAVINGS:
        return read_row_from_scotiabank_savings(row)
    elif statement_source == Account.VANCITY_CHEQUING:
        return read_row_from_vancity_chequing(row)
    elif statement_source == Account.VANCITY_CREDIT:
        return read_row_from_vancity_credit(row)
    elif statement_source == Account.VANCITY_SAVINGS:
        return read_row_from_vancity_savings(row)
    elif statement_source == Account.CREDENTIAL_ASSET_MANAGEMENT:
        return read_row_from_credential_asset_management(row)
    else:
        raise ValueError(f"{statement_source} does not exist")

def read_transactions_from_local(statement_key, statement_source):
    transactions = []

    if os.path.exists(statement_key) is False:
        return []

    with open(statement_key, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            transaction = read_row_from_account(row, statement_source)
            transactions.append(transaction)
    
    return transactions

def get_statement_keys(statement_source):
    statement_filenames = os.listdir(statement_source.value)
    statement_keys = [os.path.join(statement_source.value, file) for file in statement_filenames]
    return statement_keys

def read_all_transactions_from_statement_source(statement_source):

    statement_keys = get_statement_keys(statement_source)
    
    transactions = []
    for statement_key in statement_keys:
        transactions += read_transactions_from_local(statement_key, statement_source)

    return transactions

def read_transactions_for_date_range(statement_source, start, end):

    adjusted_start = datetime(start.year, start.month, 1) - relativedelta(months=1)
    adjusted_end = datetime(end.year, end.month, 1) + relativedelta(months=1)

    transactions = []
    loop_start = adjusted_start
    while loop_start < adjusted_end:
        prefix = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
        suffix = f"{statement_source.value}/{loop_start.date().isoformat()}.csv"
        key = os.path.join(prefix, suffix)
        transactions += read_transactions_from_local(key, statement_source)
        loop_start = loop_start + relativedelta(months=1)
    
    return [t for t in transactions if (t.date >= start and t.date < end)]

def read_all_transactions_for_date_range(start, end):

    transactions = []
    for _, source in Account.__members__.items():
        transactions += read_transactions_for_date_range(source, start, end)

    return transactions