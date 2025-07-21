CREATE VIEW rpt_top_merchants AS
SELECT 
    merchant_name,
    SUM(amount) AS total_spent,
    COUNT(*) AS transaction_count
FROM Gold.fact_transactions
WHERE pending_flag = 0
GROUP BY merchant_name;

--SELECT * FROM rpt_top_merchants