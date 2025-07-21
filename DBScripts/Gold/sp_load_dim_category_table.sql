/*
===============================================================================
Stored Procedure
===============================================================================
Script Purpose:
    This will create the stored procedure to load data in Gold.dim_category table
	from Silver.stg_transaction and implement SCD type 2 on it
===============================================================================
*/
--Select * from Gold.dim_category
CREATE OR ALTER PROCEDURE Gold.sp_load_dim_category
AS
BEGIN
    SET NOCOUNT ON;

    -- Insert new categories that don't exist yet in dim_category
    INSERT INTO Gold.dim_category (primary_category, detailed_category)
    SELECT DISTINCT
        stg.personal_finance_category_primary,
        stg.personal_finance_category_detailed
    FROM Silver.stg_transactions stg
    LEFT JOIN Gold.dim_category dim
        ON ISNULL(stg.personal_finance_category_primary, '') = ISNULL(dim.primary_category, '')
        AND ISNULL(stg.personal_finance_category_detailed, '') = ISNULL(dim.detailed_category, '')
    WHERE dim.category_sk IS NULL;
END;
