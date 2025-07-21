CREATE VIEW rpt_monthly_spend_per_account AS
SELECT 
    da.account_id,
    dd.year,
    dd.month,
    dd.month_name,
    SUM(ft.amount) AS total_spent
FROM Gold.fact_transactions ft
JOIN Gold.dim_date dd ON ft.date_sk = dd.date_sk
JOIN Gold.dim_account da ON ft.account_sk = da.account_sk
WHERE ft.pending_flag = 0
GROUP BY da.account_id, dd.year, dd.month, dd.month_name;

--SELECT * FROM rpt_monthly_spend_per_account