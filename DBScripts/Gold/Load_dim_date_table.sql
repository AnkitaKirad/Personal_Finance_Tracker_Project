/*
===============================================================================
Table Loading script
===============================================================================
Script Purpose:
    This script will load the dim_date table as it is a static dimension table
===============================================================================
*/

--SELECT * FROM Gold.dim_date
DECLARE @StartDate DATE = '2015-01-01';
DECLARE @EndDate DATE = '2035-12-31';

WITH Dates AS (
    SELECT @StartDate AS DateValue
    UNION ALL
    SELECT DATEADD(DAY, 1, DateValue)
    FROM Dates
    WHERE DateValue < @EndDate
)
INSERT INTO Gold.dim_date (date_sk, date, day, month, month_name, year, quarter, day_of_week)
SELECT
    CONVERT(INT, FORMAT(DateValue, 'yyyyMMdd')) AS date_sk,
    DateValue AS date,
    DAY(DateValue) AS day,
    MONTH(DateValue) AS month,
    DATENAME(MONTH, DateValue) AS month_name,
    YEAR(DateValue) AS year,
    DATEPART(QUARTER, DateValue) AS quarter,
    DATENAME(WEEKDAY, DateValue) AS day_of_week
FROM Dates
OPTION (MAXRECURSION 32767);

print('dim_date table loaded successfully')