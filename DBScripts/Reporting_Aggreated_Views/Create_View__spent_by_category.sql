CREATE VIEW rpt_spend_by_category AS
SELECT 
    dc.primary_category,
    dc.detailed_category,
    SUM(ft.amount) AS total_spent,
    COUNT(*) AS transaction_count
FROM Gold.fact_transactions ft
JOIN Gold.dim_category dc ON ft.category_sk = dc.category_sk
WHERE ft.pending_flag = 0
GROUP BY dc.primary_category, dc.detailed_category;

--Select * FROM rpt_spend_by_category