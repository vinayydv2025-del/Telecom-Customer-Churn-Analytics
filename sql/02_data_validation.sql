
-- ============================================================
-- PROJECT: TELECOM CUSTOMER CHURN ANALYTICS
-- FILE: 02_data_validation.sql
-- PURPOSE: Validate dataset quality and imported records
-- ============================================================

USE telecom_churn_analytics;


-- 1. Total number of customers
SELECT COUNT(*) AS total_customers
FROM customers;


-- 2. Check table structure
DESCRIBE customers;


-- 3. Check unique customer IDs
SELECT
    COUNT(DISTINCT customer_id) AS unique_customer_ids,
    COUNT(*) AS total_records
FROM customers;


-- 4. Check duplicate customer IDs
SELECT
    customer_id,
    COUNT(*) AS duplicate_count
FROM customers
GROUP BY customer_id
HAVING COUNT(*) > 1;


-- 5. Check duplicate complete records
SELECT COUNT(*) AS total_duplicate_records
FROM (
    SELECT
        customer_id,
        COUNT(*) AS record_count
    FROM customers
    GROUP BY customer_id
    HAVING COUNT(*) > 1
) AS duplicates;


-- 6. Check NULL values in important columns
SELECT
    SUM(customer_id IS NULL) AS missing_customer_id,
    SUM(tenure IS NULL) AS missing_tenure,
    SUM(monthlycharges IS NULL) AS missing_monthly_charges,
    SUM(totalcharges IS NULL) AS missing_total_charges,
    SUM(churn IS NULL) AS missing_churn
FROM customers;


-- 7. Check blank customer IDs
SELECT COUNT(*) AS blank_customer_ids
FROM customers
WHERE customer_id IS NULL
   OR TRIM(customer_id) = '';


-- 8. Check invalid negative values
SELECT
    SUM(tenure < 0) AS negative_tenure,
    SUM(monthlycharges < 0) AS negative_monthly_charges,
    SUM(totalcharges < 0) AS negative_total_charges
FROM customers;


-- 9. Check churn distribution
SELECT
    churn,
    COUNT(*) AS customer_count,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM customers), 2
    ) AS percentage
FROM customers
GROUP BY churn;


-- 10. Check missing and zero total charges
SELECT
    SUM(totalcharges IS NULL) AS null_total_charges,
    SUM(totalcharges = 0) AS zero_total_charges
FROM customers;


-- 11. Inspect zero-tenure customers
SELECT
    COUNT(*) AS zero_tenure_customers,
    SUM(totalcharges = 0) AS zero_charge_customers
FROM customers
WHERE tenure = 0;


-- 12. Check numerical ranges
SELECT
    MIN(tenure) AS minimum_tenure,
    MAX(tenure) AS maximum_tenure,
    ROUND(AVG(tenure), 2) AS average_tenure,

    MIN(monthlycharges) AS minimum_monthly_charges,
    MAX(monthlycharges) AS maximum_monthly_charges,
    ROUND(AVG(monthlycharges), 2) AS average_monthly_charges,

    MIN(totalcharges) AS minimum_total_charges,
    MAX(totalcharges) AS maximum_total_charges,
    ROUND(AVG(totalcharges), 2) AS average_total_charges
FROM customers;


-- 13. Verify categorical values
SELECT DISTINCT churn FROM customers;
SELECT DISTINCT contract FROM customers;
SELECT DISTINCT internetservice FROM customers;
SELECT DISTINCT paymentmethod FROM customers;
SELECT DISTINCT senior_citizen FROM customers;


-- 14. Final dataset verification
SELECT
    COUNT(*) AS total_records,
    COUNT(DISTINCT customer_id) AS unique_customers,
    SUM(churn = 'Yes') AS churned_customers,
    SUM(churn = 'No') AS retained_customers
FROM customers;

-- ============================================================
-- END OF DATA VALIDATION
-- ============================================================
