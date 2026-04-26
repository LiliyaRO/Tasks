SELECT
    c.client_id,
    c.name,
    c.age,
    COALESCE(ac.total_accounts, 0) AS total_accounts,
    COALESCE(ac.total_balance, 0) AS total_balance,
    COALESCE(tr.total_deposits, 0) AS total_deposits,
    COALESCE(tr.total_withdrawals, 0) AS total_withdrawals
FROM
    clients c
LEFT JOIN (
    SELECT
        a.client_id,
        COUNT(*) AS total_accounts,
        SUM(a.balance) AS total_balance
    FROM accounts a
    GROUP BY a.client_id
) ac ON ac.client_id = c.client_id
LEFT JOIN (
    SELECT
        a.client_id,
        SUM(CASE WHEN t.transaction_type = 'deposit' THEN 1 ELSE 0 END) AS total_deposits,
        SUM(CASE WHEN t.transaction_type = 'withdrawal' THEN 1 ELSE 0 END) AS total_withdrawals
    FROM accounts a
    JOIN transactions t ON t.account_id = a.account_id
    GROUP BY a.client_id
) tr ON tr.client_id = c.client_id
WHERE
    c.registration_date >= '2020-01-01'
ORDER BY
    total_balance DESC;