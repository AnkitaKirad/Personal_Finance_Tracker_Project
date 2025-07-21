/*
===============================================================================
Stored Procedure
===============================================================================
Script Purpose:
    This will create the stored procedure to load data in Gold.dim_account table
	from Silver.stg_account and implement SCD type 2 on it
===============================================================================
*/
--Select * from Gold.dim_account
CREATE OR ALTER PROCEDURE Gold.sp_upsert_dim_account
AS
BEGIN
    SET NOCOUNT ON;

    -- Temp table for incoming data from Silver layer
    CREATE TABLE #incoming (
        account_id              VARCHAR(100),
        mask                    VARCHAR(10),
        name                    VARCHAR(255),
        official_name           VARCHAR(255),
        type                    VARCHAR(50),
        subtype                 VARCHAR(50),
        holder_category         VARCHAR(100),
        currency_code           VARCHAR(10)
    );

    -- Load latest data from Silver layer
    INSERT INTO #incoming (account_id, mask, name, official_name, type, subtype, holder_category, currency_code)
    SELECT 
        account_id,
        mask,
        name,
        official_name,
        type,
        subtype,
        holder_category,
        balances_iso_currency_code
    FROM Silver.stg_accounts;

    -- Step 1: Expire old records if there's a change
    UPDATE dim
    SET 
        end_date = GETDATE(),
        current_flag = 0,
        is_active = 0
    FROM Gold.dim_account dim
    INNER JOIN #incoming inc ON dim.account_id = inc.account_id
    WHERE dim.current_flag = 1
      AND (
          ISNULL(dim.mask, '') <> ISNULL(inc.mask, '') OR
          ISNULL(dim.name, '') <> ISNULL(inc.name, '') OR
          ISNULL(dim.official_name, '') <> ISNULL(inc.official_name, '') OR
          ISNULL(dim.type, '') <> ISNULL(inc.type, '') OR
          ISNULL(dim.subtype, '') <> ISNULL(inc.subtype, '') OR
          ISNULL(dim.holder_category, '') <> ISNULL(inc.holder_category, '') OR
          ISNULL(dim.currency_code, '') <> ISNULL(inc.currency_code, '')
      );

    -- Step 2: Insert new records (new or changed)
    INSERT INTO Gold.dim_account (
        account_id, mask, name, official_name, type, subtype,
        holder_category, currency_code, is_active,
        start_date, end_date, current_flag
    )
    SELECT 
        inc.account_id,
        inc.mask,
        inc.name,
        inc.official_name,
        inc.type,
        inc.subtype,
        inc.holder_category,
        inc.currency_code,
        1,                -- is_active
        GETDATE(),        -- start_date
        NULL,             -- end_date
        1                 -- current_flag
    FROM #incoming inc
    LEFT JOIN Gold.dim_account dim
        ON inc.account_id = dim.account_id AND dim.current_flag = 1
    WHERE dim.account_id IS NULL OR
          (
            ISNULL(dim.mask, '') <> ISNULL(inc.mask, '') OR
            ISNULL(dim.name, '') <> ISNULL(inc.name, '') OR
            ISNULL(dim.official_name, '') <> ISNULL(inc.official_name, '') OR
            ISNULL(dim.type, '') <> ISNULL(inc.type, '') OR
            ISNULL(dim.subtype, '') <> ISNULL(inc.subtype, '') OR
            ISNULL(dim.holder_category, '') <> ISNULL(inc.holder_category, '') OR
            ISNULL(dim.currency_code, '') <> ISNULL(inc.currency_code, '')
          );

    DROP TABLE #incoming;
END;
GO
