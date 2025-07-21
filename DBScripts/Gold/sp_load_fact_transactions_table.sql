/*
===============================================================================
Stored Procedure
===============================================================================
Script Purpose:
    This will create the stored procedure to load data in Gold.fact_transactions table
	from Silver.stg_transaction and joining it to dim_account,dim_category and dim_date tables
===============================================================================
*/
--SELECT * FROM Gold.fact_transactions
CREATE OR ALTER PROCEDURE Gold.sp_load_fact_transactions
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO Gold.fact_transactions (
        transaction_id,
        account_sk,
        date_sk,
        merchant_name,
        amount,
        currency_code,
        payment_channel,
        category_sk,
        pending_flag,
        created_at
    )
    SELECT
        st.transaction_id,
        da.account_sk,
        dd.date_sk,
        LOWER(LTRIM(RTRIM(st.merchant_name))),
        st.amount,
        ISNULL(st.iso_currency_code, 'USD'),
        ISNULL(st.payment_channel, 'online'),
        dc.category_sk,
        CASE WHEN st.pending = 1 THEN 1 ELSE 0 END,
        GETDATE()
    FROM Silver.stg_transactions st
    INNER JOIN Gold.dim_account da
        ON st.account_id = da.account_id
        AND da.current_flag = 1
    INNER JOIN Gold.dim_date dd
        ON CAST(st.date AS DATE) = dd.date
    LEFT JOIN Gold.dim_category dc
        ON ISNULL(st.personal_finance_category_primary, '') = ISNULL(dc.primary_category, '')
        AND ISNULL(st.personal_finance_category_detailed, '') = ISNULL(dc.detailed_category, '')
    WHERE NOT EXISTS (
        SELECT 1
        FROM Gold.fact_transactions ft
        WHERE ft.transaction_id = st.transaction_id
    );
END;
