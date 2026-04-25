import pandas as pd

# Входные данные
data_transactions = {
    'transaction_id': [1, 2, 3, 4, 5, 6, 7, 8],
    'client_id': [101, 102, 101, 103, 102, 101, 103, 102],
    'transaction_date': ['2024-01-15', '2024-02-20', '2024-03-10', '2024-04-05', '2024-05-12', '2023-12-25', '2024-06-01', '2024-07-18'],
    'amount': ['1000.50', '200.75', '150.00', '500.25', '300.50', '1200.00', '700.00', '400.00'],
    'currency': ['USD', 'EUR', 'USD', 'USD', 'EUR', 'USD', 'USD', 'EUR'],
    'transaction_type': ['deposit', 'withdrawal', 'deposit', 'withdrawal', 'deposit', 'deposit', 'withdrawal', 'withdrawal']
}

data_clients = {
    'client_id': [101, 102, 103],
    'client_name': ['Иван Иванов', 'Петр Петров', 'Сидор Сидоров'],
    'registration_date': ['2023-12-01', '2024-01-10', '2024-02-15'],
    'client_status': ['active', 'active', 'inactive']
}

transactions = pd.DataFrame(data_transactions)
clients = pd.DataFrame(data_clients)

# Преобразование типов
transactions['amount'] = pd.to_numeric(transactions['amount'])
transactions['transaction_date'] = pd.to_datetime(transactions['transaction_date'])

# Фильтрация
active_clients = clients[clients['client_status'] == 'active']
transactions_2024 = transactions[
    (transactions['transaction_date'] >= '2024-01-01') &
    (transactions['transaction_date'] <= '2024-12-31')
]

# Объединение
merged = pd.merge(transactions_2024, active_clients, on='client_id')

# Группировка
result = merged.groupby(['client_id', 'client_name', 'transaction_type']).agg(
    total_amount=('amount', 'sum'),
    average_amount=('amount', 'mean'),
    transaction_count=('amount', 'count'),
    last_transaction_date=('transaction_date', 'max')
).reset_index()

# Сортировка
result_sorted = result.sort_values('total_amount', ascending=False)

# Выводим результат
result_sorted
