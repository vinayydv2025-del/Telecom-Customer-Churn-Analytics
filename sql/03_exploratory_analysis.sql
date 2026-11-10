
-- ============================================================
-- PROJECT: TELECOM CUSTOMER CHURN ANALYTICS
-- FILE: 03_exploratory_analysis.sql
-- PURPOSE: Exploratory Data Analysis and Business Analysis
-- DATABASE: telecom_churn_analytics
-- ============================================================

USE telecom_churn_analytics;


-- ============================================================
-- SECTION 1: OVERALL CUSTOMER CHURN ANALYSIS
-- ============================================================

-- 1. Overall churn distribution

SELECT
    churn,
    COUNT(*) AS customer_count,
    ROUND(COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM customers), 2) AS percentage
FROM customers
GROUP BY churn;


-- 2. Average monthly charges

SELECT
    ROUND(AVG(monthlycharges), 2) AS average_monthly_charges
FROM customers;


-- 3. Average customer tenure

SELECT
    ROUND(AVG(tenure), 2) AS average_tenure_months
FROM customers;


-- 4. Consolidated business KPI summary

SELECT
    COUNT(*) AS total_customers,
    SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END)
        AS churned_customers,
    SUM(CASE WHEN churn = 'No' THEN 1 ELSE 0 END)
        AS retained_customers,
    ROUND(
        SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*), 2
    ) AS churn_rate,
    ROUND(AVG(tenure), 2) AS average_tenure,
    ROUND(AVG(monthlycharges), 2) AS average_monthly_charges,
    ROUND(SUM(monthlycharges), 2) AS total_monthly_charge_base
FROM customers;


-- ============================================================
-- SECTION 2: CHURN BY CUSTOMER CONTRACT
-- ============================================================

-- 5. Churn rate by contract type

SELECT
    contract,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END)
        AS churned_customers,
    ROUND(
        SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*), 2
    ) AS churn_rate
FROM customers
GROUP BY contract
ORDER BY churn_rate DESC;


-- ============================================================
-- SECTION 3: CHURN BY INTERNET SERVICE
-- ============================================================

-- 6. Churn rate by internet service

SELECT
    internetservice,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END)
        AS churned_customers,
    ROUND(
        SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*), 2
    ) AS churn_rate
FROM customers
GROUP BY internetservice
ORDER BY churn_rate DESC;


-- ============================================================
-- SECTION 4: CHURN BY PAYMENT METHOD
-- ============================================================

-- 7. Churn rate by payment method

SELECT
    paymentmethod,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END)
        AS churned_customers,
    ROUND(
        SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*), 2
    ) AS churn_rate
FROM customers
GROUP BY paymentmethod
ORDER BY churn_rate DESC;


-- ============================================================
-- SECTION 5: CHURN BY CUSTOMER TENURE
-- ============================================================

-- 8. Churn rate by tenure group

SELECT
    CASE
        WHEN tenure <= 12 THEN '0-12 Months'
        WHEN tenure <= 24 THEN '13-24 Months'
        WHEN tenure <= 48 THEN '25-48 Months'
        WHEN tenure <= 60 THEN '49-60 Months'
        ELSE '61-72 Months'
    END AS tenure_group,

    COUNT(*) AS total_customers,

    SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END)
        AS churned_customers,

    ROUND(
        SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*), 2
    ) AS churn_rate

FROM customers
GROUP BY tenure_group
ORDER BY MIN(tenure);


-- ============================================================
-- SECTION 6: CHURN BY MONTHLY CHARGES
-- ============================================================

-- 9. Churn rate by monthly charge group
-- Boundaries match the Python pd.cut() analysis.

SELECT
    CASE
        WHEN monthlycharges <= 35 THEN 'Low Charges'
        WHEN monthlycharges <= 70 THEN 'Medium Charges'
        WHEN monthlycharges <= 100 THEN 'High Charges'
        ELSE 'Very High Charges'
    END AS charge_group,

    COUNT(*) AS total_customers,

    SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END)
        AS churned_customers,

    ROUND(
        SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*), 2
    ) AS churn_rate

FROM customers
GROUP BY charge_group
ORDER BY MIN(monthlycharges);


-- ============================================================
-- SECTION 7: CHURN BY CUSTOMER DEMOGRAPHICS
-- ============================================================

-- 10. Churn by senior citizen status

SELECT
    senior_citizen,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END)
        AS churned_customers,
    ROUND(
        SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*), 2
    ) AS churn_rate
FROM customers
GROUP BY senior_citizen
ORDER BY churn_rate DESC;


-- 11. Churn by gender

SELECT
    gender,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END)
        AS churned_customers,
    ROUND(
        SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*), 2
    ) AS churn_rate
FROM customers
GROUP BY gender
ORDER BY churn_rate DESC;


-- 12. Churn by partner status

SELECT
    partner,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END)
        AS churned_customers,
    ROUND(
        SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*), 2
    ) AS churn_rate
FROM customers
GROUP BY partner
ORDER BY churn_rate DESC;


-- 13. Churn by dependents

SELECT
    dependents,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END)
        AS churned_customers,
    ROUND(
        SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*), 2
    ) AS churn_rate
FROM customers
GROUP BY dependents
ORDER BY churn_rate DESC;


-- ============================================================
-- SECTION 8: CHURN BY ADD-ON SERVICES
-- ============================================================

-- 14. Churn by online security

SELECT
    onlinesecurity,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END)
        AS churned_customers,
    ROUND(
        SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*), 2
    ) AS churn_rate
FROM customers
GROUP BY onlinesecurity
ORDER BY churn_rate DESC;


-- 15. Churn by tech support

SELECT
    techsupport,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END)
        AS churned_customers,
    ROUND(
        SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*), 2
    ) AS churn_rate
FROM customers
GROUP BY techsupport
ORDER BY churn_rate DESC;


-- 16. Churn by online backup

SELECT
    onlinebackup,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END)
        AS churned_customers,
    ROUND(
        SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*), 2
    ) AS churn_rate
FROM customers
GROUP BY onlinebackup
ORDER BY churn_rate DESC;


-- 17. Churn by device protection

SELECT
    deviceprotection,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END)
        AS churned_customers,
    ROUND(
        SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*), 2
    ) AS churn_rate
FROM customers
GROUP BY deviceprotection
ORDER BY churn_rate DESC;


-- 18. Churn by streaming TV

SELECT
    streamingtv,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END)
        AS churned_customers,
    ROUND(
        SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*), 2
    ) AS churn_rate
FROM customers
GROUP BY streamingtv
ORDER BY churn_rate DESC;


-- 19. Churn by streaming movies

SELECT
    streamingmovies,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END)
        AS churned_customers,
    ROUND(
        SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*), 2
    ) AS churn_rate
FROM customers
GROUP BY streamingmovies
ORDER BY churn_rate DESC;


-- ============================================================
-- SECTION 9: CUSTOMER VALUE ANALYSIS
-- ============================================================

-- 20. Compare retained and churned customers

SELECT
    churn,
    COUNT(*) AS customer_count,
    ROUND(AVG(tenure), 2) AS average_tenure,
    ROUND(AVG(monthlycharges), 2) AS average_monthly_charges,
    ROUND(AVG(totalcharges), 2) AS average_total_charges,
    ROUND(SUM(monthlycharges), 2) AS total_monthly_charges
FROM customers
GROUP BY churn;


-- ============================================================
-- SECTION 10: ADVANCED CUSTOMER SEGMENT ANALYSIS
-- ============================================================

-- 21. Churn by contract and tenure group

SELECT
    contract,

    CASE
        WHEN tenure <= 12 THEN '0-12 Months'
        WHEN tenure <= 24 THEN '13-24 Months'
        WHEN tenure <= 48 THEN '25-48 Months'
        WHEN tenure <= 60 THEN '49-60 Months'
        ELSE '61-72 Months'
    END AS tenure_group,

    COUNT(*) AS total_customers,

    SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END)
        AS churned_customers,

    ROUND(
        SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*), 2
    ) AS churn_rate

FROM customers
GROUP BY contract, tenure_group
ORDER BY contract, MIN(tenure);


-- 22. Identify high-priority historical churn segment
-- Month-to-month customers with tenure <= 12
-- who have already churned.

SELECT
    customer_id,
    gender,
    senior_citizen,
    tenure,
    contract,
    internetservice,
    paymentmethod,
    monthlycharges,
    totalcharges,
    churn
FROM customers
WHERE contract = 'Month-to-month'
  AND tenure <= 12
  AND churn = 'Yes';


-- 23. Count customers in the high-priority historical segment

SELECT
    COUNT(*) AS high_priority_churned_customers
FROM customers
WHERE contract = 'Month-to-month'
  AND tenure <= 12
  AND churn = 'Yes';


-- ============================================================
-- END OF EXPLORATORY DATA ANALYSIS
-- ============================================================
