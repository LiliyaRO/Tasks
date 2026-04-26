-- Условие 1: ровно по сумме и в интервале T+10 дней
WITH matches_exact AS (
    SELECT
        t.inn AS tranche_inn,
        t.credit_num,
        t.account AS tranche_account,
        t.operation_datetime AS tranche_datetime,
        t.operation_sum AS tranche_sum,
        t.doc_id AS tranche_doc_id,
        tr.operation_datetime AS transaction_datetime,
        tr.operation_sum AS transaction_sum,
        tr.ctrg_inn,
        tr.ctrg_account,
        tr.doc_id AS transaction_doc_id,
        1 AS match_type   -- Тип сопоставления: 1 (копейка в копейку)
    FROM tranches t
    JOIN transactions tr
      ON t.inn = tr.inn
      AND t.account = tr.account
      AND tr.operation_datetime BETWEEN t.operation_datetime AND t.operation_datetime + INTERVAL '10 days'
      AND tr.operation_sum = t.operation_sum
    WHERE t.operation_datetime >= '2024-01-01' AND t.operation_datetime < '2025-01-01'
),

-- Проверяем, были ли "копейка в копейку" совпадения для каждого транша
used_tranches AS (
    SELECT DISTINCT tranche_doc_id FROM matches_exact
),

-- Условие 2: сумма операций больше суммы транша, если транш не найден по условию 1
matches_over AS (
    SELECT
        t.inn AS tranche_inn,
        t.credit_num,
        t.account AS tranche_account,
        t.operation_datetime AS tranche_datetime,
        t.operation_sum AS tranche_sum,
        t.doc_id AS tranche_doc_id,
        tr.operation_datetime AS transaction_datetime,
        tr.operation_sum AS transaction_sum,
        tr.ctrg_inn,
        tr.ctrg_account,
        tr.doc_id AS transaction_doc_id,
        2 AS match_type   -- Тип сопоставления: 2 (превышение суммы)
    FROM tranches t
    JOIN transactions tr
      ON t.inn = tr.inn
      AND t.account = tr.account
      AND tr.operation_datetime BETWEEN t.operation_datetime AND t.operation_datetime + INTERVAL '10 days'
      AND tr.operation_sum > t.operation_sum
    WHERE t.operation_datetime >= '2024-01-01' AND t.operation_datetime < '2025-01-01'
      AND t.doc_id NOT IN (SELECT tranche_doc_id FROM used_tranches)
)

-- Объединяем оба условия
SELECT * FROM matches_exact
UNION ALL
SELECT * FROM matches_over
ORDER BY tranche_inn, tranche_doc_id, transaction_datetime;