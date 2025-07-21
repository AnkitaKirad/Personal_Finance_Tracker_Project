CREATE VIEW rpt_monthly_trend AS
SELECT 
    dd.year,
    dd.month,
    dd.month_name,
    SUM(ft.amount) AS monthly_spend
FROM Gold.fact_transactions ft
JOIN Gold.dim_date dd ON ft.date_sk = dd.date_sk
WHERE ft.pending_flag = 0
GROUP BY dd.year, dd.month, dd.month_name;

--SELECT * FROM rpt_monthly_trend