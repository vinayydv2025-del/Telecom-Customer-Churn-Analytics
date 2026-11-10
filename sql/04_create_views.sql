
-- ============================================================
-- PROJECT: TELECOM CUSTOMER CHURN ANALYTICS
-- FILE: 04_create_views.sql
-- PURPOSE: Create reusable analytical SQL views
-- DATABASE: telecom_churn_analytics
-- ============================================================

USE telecom_churn_analytics;


-- 1. OVERALL CHURN SUMMARY

CREATE OR REPLACE VIEW churn_summary AS
SELECT
    COUNT(*) AS total_customers,
    SUM(churn = 'Yes') AS churned_customers,
    SUM(churn = 'No') AS retained_customers,
    ROUND(100.0 * SUM(churn = 'Yes') / COUNT(*), 2) AS churn_rate_pct,
    ROUND(100.0 * SUM(churn = 'No') / COUNT(*), 2) AS retention_rate_pct,
    ROUND(AVG(tenure), 2) AS average_tenure,
    ROUND(AVG(monthlycharges), 2) AS average_monthly_charges,
    ROUND(SUM(monthlycharges), 2) AS total_monthly_charge_base
FROM customers;


-- 2. CHURN BY CONTRACT

CREATE OR REPLACE VIEW churn_by_contract AS
SELECT
    contract,
    COUNT(*) AS customer_count,
    SUM(churn = 'Yes') AS churned_customers,
    ROUND(100.0 * SUM(churn = 'Yes') / COUNT(*), 2) AS churn_rate_pct
FROM customers
GROUP BY contract;


-- 3. CHURN BY INTERNET SERVICE

CREATE OR REPLACE VIEW churn_by_internet_service AS
SELECT
    internetservice,
    COUNT(*) AS customer_count,
    SUM(churn = 'Yes') AS churned_customers,
    ROUND(100.0 * SUM(churn = 'Yes') / COUNT(*), 2) AS churn_rate_pct
FROM customers
GROUP BY internetservice;


-- 4. CHURN BY PAYMENT METHOD

CREATE OR REPLACE VIEW churn_by_payment_method AS
SELECT
    paymentmethod,
    COUNT(*) AS customer_count,
    SUM(churn = 'Yes') AS churned_customers,
    ROUND(100.0 * SUM(churn = 'Yes') / COUNT(*), 2) AS churn_rate_pct
FROM customers
GROUP BY paymentmethod;


-- 5. CHURN BY TENURE

CREATE OR REPLACE VIEW churn_by_tenure AS
SELECT
    CASE
        WHEN tenure <= 12 THEN '0-12 Months'
        WHEN tenure <= 24 THEN '13-24 Months'
        WHEN tenure <= 48 THEN '25-48 Months'
        WHEN tenure <= 60 THEN '49-60 Months'
        ELSE '61-72 Months'
    END AS tenure_group,
    COUNT(*) AS customer_count,
    SUM(churn = 'Yes') AS churned_customers,
    ROUND(100.0 * SUM(churn = 'Yes') / COUNT(*), 2) AS churn_rate_pct
FROM customers
GROUP BY tenure_group;


-- 6. CHURN BY MONTHLY CHARGES

CREATE OR REPLACE VIEW churn_by_monthly_charges AS
SELECT
    CASE
        WHEN monthlycharges <= 35 THEN 'Low Charges'
        WHEN monthlycharges <= 70 THEN 'Medium Charges'
        WHEN monthlycharges <= 100 THEN 'High Charges'
        ELSE 'Very High Charges'
    END AS monthly_charge_group,
    COUNT(*) AS customer_count,
    SUM(churn = 'Yes') AS churned_customers,
    ROUND(100.0 * SUM(churn = 'Yes') / COUNT(*), 2) AS churn_rate_pct
FROM customers
GROUP BY monthly_charge_group;


-- 7. CHURN BY ONLINE SECURITY

CREATE OR REPLACE VIEW churn_by_online_security AS
SELECT
    onlinesecurity AS service_status,
    COUNT(*) AS customer_count,
    SUM(churn = 'Yes') AS churned_customers,
    ROUND(100.0 * SUM(churn = 'Yes') / COUNT(*), 2) AS churn_rate_pct
FROM customers
GROUP BY onlinesecurity;


-- 8. CHURN BY TECH SUPPORT

CREATE OR REPLACE VIEW churn_by_tech_support AS
SELECT
    techsupport AS service_status,
    COUNT(*) AS customer_count,
    SUM(churn = 'Yes') AS churned_customers,
    ROUND(100.0 * SUM(churn = 'Yes') / COUNT(*), 2) AS churn_rate_pct
FROM customers
GROUP BY techsupport;


-- 9. CUSTOMER VALUE BY CHURN

CREATE OR REPLACE VIEW customer_value_by_churn AS
SELECT
    churn,
    COUNT(*) AS customer_count,
    ROUND(AVG(tenure), 2) AS average_tenure,
    ROUND(AVG(monthlycharges), 2) AS average_monthly_charges,
    ROUND(AVG(totalcharges), 2) AS average_total_charges,
    ROUND(SUM(monthlycharges), 2) AS total_monthly_charge_base
FROM customers
GROUP BY churn;


-- 10. CHURN BY SENIOR CITIZEN

CREATE OR REPLACE VIEW churn_by_senior_citizen AS
SELECT
    senior_citizen,
    COUNT(*) AS customer_count,
    SUM(churn = 'Yes') AS churned_customers,
    ROUND(100.0 * SUM(churn = 'Yes') / COUNT(*), 2) AS churn_rate_pct
FROM customers
GROUP BY senior_citizen;


-- 11. HIGH-PRIORITY HISTORICAL CHURN SEGMENT

CREATE OR REPLACE VIEW high_priority_churn_segment AS
SELECT
    customer_id,
    contract,
    tenure,
    monthlycharges,
    totalcharges,
    churn
FROM customers
WHERE contract = 'Month-to-month'
  AND tenure <= 12
  AND churn = 'Yes';


-- ============================================================
-- VERIFY ALL 11 VIEWS
-- ============================================================

SHOW FULL TABLES
WHERE Table_type = 'VIEW';


-- TEST THE VIEWS

SELECT * FROM churn_summary;
SELECT * FROM churn_by_contract;
SELECT * FROM churn_by_internet_service;
SELECT * FROM churn_by_payment_method;
SELECT * FROM churn_by_tenure;
SELECT * FROM churn_by_monthly_charges;
SELECT * FROM churn_by_online_security;
SELECT * FROM churn_by_tech_support;
SELECT * FROM customer_value_by_churn;
SELECT * FROM churn_by_senior_citizen;
SELECT * FROM high_priority_churn_segment;
