import pandas as pd
from mlxtend.preprocessing import TransactionEncoder


def load_data(path):
    return pd.read_csv(path)


def create_transactions(df):

    transactions = []

    for i in range(len(df)):
        transactions.append([
            str(item)
            for item in df.iloc[i, 1:].dropna().tolist()
        ])

    return transactions


def encode_transactions(transactions):

    te = TransactionEncoder()

    te_array = te.fit(transactions).transform(transactions)

    basket = pd.DataFrame(
        te_array,
        columns=te.columns_
    )

    return basket.astype(bool)