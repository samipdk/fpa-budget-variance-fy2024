-- ============================================================
-- FP&A Budget vs Actual Variance Analysis — FY2024
-- Financial Services Business Unit
-- Author: Suyash Thakuri — Financial Data Analyst
-- ============================================================
-- TABLES:
--   budget_vs_actual  (month, month_num, year, period, type,
--                      category, budget, actual, variance,
--                      variance_pct)
--   monthly_summary   (month, month_num, period,
--                      revenue_budget, revenue_actual,
--                      revenue_variance, revenue_variance_pct,
--                      cost_budget, cost_actual, cost_variance,
--                      ebitda_budget, ebitda_actual,
--                      ebitda_variance, ebitda_margin_budget,
--                      ebitda_margin_actual)
-- ============================================================


-- ============================================================
-- QUERY 1: Full Year P&L Summary — Budget vs Actual
-- BUSINESS QUESTION: What is the overall financial result
--                    for FY2024 vs budget?
-- ============================================================

WITH revenue AS (
    SELECT
        'Revenue'           AS line_item,
        SUM(budget)         AS budget,
        SUM(actual)         AS actual,
        SUM(variance)       AS variance,
        ROUND(SUM(variance) * 100.0 / SUM(budget), 1) AS variance_pct
    FROM budget_vs_actual
    WHERE type = 'Revenue'
),
costs AS (
    SELECT
        'Total Costs'       AS line_item,
        SUM(budget)         AS budget,
        SUM(actual)         AS actual,
        SUM(variance)       AS variance,
        ROUND(SUM(variance) * 100.0 / SUM(budget), 1) AS variance_pct
    FROM budget_vs_actual
    WHERE type = 'Cost'
),
ebitda AS (
    SELECT
        'EBITDA'            AS line_item,
        SUM(CASE WHEN type='Revenue' THEN budget ELSE -budget END) AS budget,
        SUM(CASE WHEN type='Revenue' THEN actual ELSE -actual END) AS actual,
        SUM(CASE WHEN type='Revenue' THEN variance ELSE -variance END) AS variance,
        NULL                AS variance_pct
    FROM budget_vs_actual
)
SELECT line_item, budget, actual, variance, variance_pct,
    CASE
        WHEN line_item = 'Revenue' AND variance > 0 THEN 'Beat'
        WHEN line_item = 'Revenue' AND variance < 0 THEN 'Miss'
        WHEN line_item = 'Total Costs' AND variance > 0 THEN 'Over budget'
        WHEN line_item = 'Total Costs' AND variance < 0 THEN 'Under budget'
        WHEN line_item = 'EBITDA' AND variance > 0 THEN 'Beat'
        ELSE 'Miss'
    END AS status
FROM revenue
UNION ALL SELECT * FROM costs
UNION ALL SELECT * FROM ebitda;


-- ============================================================
-- QUERY 2: Revenue Variance by Product Line — Ranked
-- BUSINESS QUESTION: Which products are driving the
--                    revenue beat or miss?
-- ============================================================

WITH product_variance AS (
    SELECT
        category                                            AS product,
        SUM(budget)                                         AS fy_budget,
        SUM(actual)                                         AS fy_actual,
        SUM(variance)                                       AS fy_variance,
        ROUND(SUM(variance) * 100.0 / SUM(budget), 1)      AS variance_pct,
        -- H1 vs H2 split
        SUM(CASE WHEN month_num <= 6 THEN actual ELSE 0 END) AS h1_actual,
        SUM(CASE WHEN month_num > 6  THEN actual ELSE 0 END) AS h2_actual,
        SUM(CASE WHEN month_num <= 6 THEN budget ELSE 0 END) AS h1_budget,
        SUM(CASE WHEN month_num > 6  THEN budget ELSE 0 END) AS h2_budget,
        RANK() OVER (ORDER BY SUM(variance) DESC)           AS performance_rank
    FROM budget_vs_actual
    WHERE type = 'Revenue'
    GROUP BY category
)
SELECT
    performance_rank,
    product,
    fy_budget,
    fy_actual,
    fy_variance,
    variance_pct,
    ROUND((h1_actual - h1_budget) * 100.0 / h1_budget, 1)  AS h1_variance_pct,
    ROUND((h2_actual - h2_budget) * 100.0 / h2_budget, 1)  AS h2_variance_pct,
    CASE
        WHEN variance_pct >= 5   THEN 'Strong beat'
        WHEN variance_pct >= 0   THEN 'On track'
        WHEN variance_pct >= -5  THEN 'Slight miss'
        ELSE                          'Significant miss'
    END                                                     AS performance_flag,
    -- Trend: is H2 better or worse than H1?
    CASE
        WHEN ROUND((h2_actual-h2_budget)*100.0/h2_budget,1) >
             ROUND((h1_actual-h1_budget)*100.0/h1_budget,1)
        THEN 'Improving'
        ELSE 'Deteriorating'
    END                                                     AS trend
FROM product_variance
ORDER BY performance_rank;


-- ============================================================
-- QUERY 3: Cost Variance by Category with Monthly Trend
-- BUSINESS QUESTION: Which cost categories are over budget
--                    and is the problem getting worse?
-- ============================================================

WITH cost_monthly AS (
    SELECT
        category,
        month_num,
        month,
        budget,
        actual,
        variance,
        ROUND(variance * 100.0 / budget, 1)                 AS monthly_var_pct,
        -- Running YTD variance
        SUM(variance) OVER (
            PARTITION BY category
            ORDER BY month_num
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        )                                                   AS ytd_variance,
        -- 3-month rolling avg variance
        ROUND(AVG(variance) OVER (
            PARTITION BY category
            ORDER BY month_num
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ), 0)                                               AS rolling_3m_avg_variance
    FROM budget_vs_actual
    WHERE type = 'Cost'
),
annual_summary AS (
    SELECT
        category,
        SUM(budget)                                         AS fy_budget,
        SUM(actual)                                         AS fy_actual,
        SUM(variance)                                       AS fy_variance,
        ROUND(SUM(variance)*100.0/SUM(budget),1)            AS fy_var_pct,
        -- H2 run rate vs H1 (is overspend accelerating?)
        SUM(CASE WHEN month_num <= 6 THEN variance ELSE 0 END) AS h1_variance,
        SUM(CASE WHEN month_num > 6  THEN variance ELSE 0 END) AS h2_variance
    FROM budget_vs_actual
    WHERE type = 'Cost'
    GROUP BY category
)
SELECT
    a.category,
    a.fy_budget,
    a.fy_actual,
    a.fy_variance,
    a.fy_var_pct,
    a.h1_variance,
    a.h2_variance,
    -- Is H2 worse than H1?
    CASE WHEN a.h2_variance > a.h1_variance THEN 'Accelerating overrun'
         ELSE 'Stable / improving'
    END                                                     AS h2_vs_h1_trend,
    CASE
        WHEN a.fy_var_pct > 10  THEN '🔴 Critical'
        WHEN a.fy_var_pct > 3   THEN '🟡 Monitoring'
        WHEN a.fy_var_pct > 0   THEN '🟡 Slight over'
        ELSE                         '🟢 Under budget'
    END                                                     AS rag_status
FROM annual_summary a
ORDER BY a.fy_variance DESC;


-- ============================================================
-- QUERY 4: Monthly EBITDA Bridge
-- BUSINESS QUESTION: Month by month, was EBITDA above
--                    or below budget — and what drove it?
-- ============================================================

WITH monthly_rev AS (
    SELECT month_num, month,
        SUM(budget) AS rev_budget, SUM(actual) AS rev_actual,
        SUM(variance) AS rev_variance
    FROM budget_vs_actual WHERE type = 'Revenue'
    GROUP BY month_num, month
),
monthly_cost AS (
    SELECT month_num,
        SUM(budget) AS cost_budget, SUM(actual) AS cost_actual,
        SUM(variance) AS cost_variance
    FROM budget_vs_actual WHERE type = 'Cost'
    GROUP BY month_num
)
SELECT
    r.month,
    r.month_num,
    r.rev_budget,
    r.rev_actual,
    r.rev_variance,
    c.cost_budget,
    c.cost_actual,
    c.cost_variance,
    (r.rev_budget - c.cost_budget)                          AS ebitda_budget,
    (r.rev_actual - c.cost_actual)                          AS ebitda_actual,
    (r.rev_actual - c.cost_actual) -
    (r.rev_budget - c.cost_budget)                          AS ebitda_variance,
    ROUND((r.rev_actual - c.cost_actual)*100.0/r.rev_actual,1)
                                                            AS ebitda_margin_actual,
    ROUND((r.rev_budget - c.cost_budget)*100.0/r.rev_budget,1)
                                                            AS ebitda_margin_budget,
    -- YTD EBITDA
    SUM((r.rev_actual - c.cost_actual)) OVER (
        ORDER BY r.month_num
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    )                                                       AS ebitda_ytd,
    SUM((r.rev_budget - c.cost_budget)) OVER (
        ORDER BY r.month_num
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    )                                                       AS ebitda_ytd_budget
FROM monthly_rev r
JOIN monthly_cost c ON r.month_num = c.month_num
ORDER BY r.month_num;


-- ============================================================
-- QUERY 5: Top Variance Drivers — EBITDA Impact Ranking
-- BUSINESS QUESTION: Which line items had the biggest
--                    impact on EBITDA vs budget?
-- ============================================================

WITH all_variances AS (
    SELECT
        type,
        category,
        SUM(variance)                                       AS total_variance,
        -- For revenue: positive variance is good
        -- For costs: positive variance is bad (overspend)
        CASE WHEN type = 'Revenue' THEN SUM(variance)
             ELSE -SUM(variance)
        END                                                 AS ebitda_impact,
        ROUND(SUM(variance)*100.0/SUM(budget),1)            AS var_pct
    FROM budget_vs_actual
    GROUP BY type, category
)
SELECT
    RANK() OVER (ORDER BY ebitda_impact DESC)               AS impact_rank,
    type,
    category,
    total_variance,
    ebitda_impact,
    var_pct,
    CASE
        WHEN ebitda_impact > 1000 THEN 'Major positive'
        WHEN ebitda_impact > 0    THEN 'Positive'
        WHEN ebitda_impact > -500 THEN 'Minor drag'
        ELSE                           'Significant drag'
    END                                                     AS ebitda_impact_flag
FROM all_variances
ORDER BY impact_rank;
