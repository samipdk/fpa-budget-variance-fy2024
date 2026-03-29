# FP&A Budget vs Actual Variance Report — FY2024
### CFO Management Pack for a Financial Services Business Unit — SQL · Python · Power BI

---

## The Business Problem

A Financial Services Business Unit CFO needs a full-year management pack that clearly answers:
1. Did we hit our revenue and EBITDA targets for FY2024?
2. Which product lines and cost categories drove the variances?
3. Where is the margin going and what needs management attention in FY2025?

This project delivers a complete CFO-grade management pack — from raw budget/actual data through to a written variance report with product-level analysis, cost bridge, and forward outlook.

---

## FY2024 Headline Results

| Metric | Budget | Actual | Variance |
|---|---|---|---|
| **Revenue** | A$149,010k | A$151,307k | **+A$2,297k (+1.5%)** ✅ |
| **Total Costs** | A$77,545k | A$79,990k | **+A$2,445k (+3.2%)** ❌ |
| **EBITDA** | A$71,465k | A$71,317k | **-A$148k (-0.2%)** 🟡 |
| **EBITDA Margin** | 48.0% | 47.1% | **-0.9pp compression** ❌ |

**The story:** Revenue beat by +1.5% but costs grew faster (+3.2%), squeezing EBITDA margin by 0.9pp. The margin compression was driven by Technology (+13.5% over budget) and Marketing (+11.2% over budget). Without these two overruns, margin would have been approximately 47.9% — broadly on budget.

---

## Key Findings

**Revenue:**
- Digital Payments: +19.4% above budget — strongest performer, growth accelerating
- Wealth Management: +8.6% above budget — consistent outperformance all year
- Business Lending: -9.2% below budget — significant miss requiring recovery plan
- Retail Banking: -0.6% — broadly in line despite NIM pressure

**Costs:**
- Technology: +13.5% over budget — cloud infrastructure and unplanned licence costs
- Marketing: +11.2% over budget — unbudgeted Digital Payments campaign (revenue-justified)
- Compliance: +7.3% over budget — structural APRA reporting requirement increases
- Facilities: +0.9% — well controlled

---

## Report Contents

### CFO Management Pack (`FPA_CFO_Management_Pack_FY2024.docx`)
5-section Word document:
1. Executive Summary — headline P&L, key message, management action items
2. Revenue Performance — product line variance table, commentary on each line
3. Cost Performance — category variance table, overrun analysis, commentary
4. EBITDA & Margin — bridge analysis, margin compression drivers
5. FY2025 Outlook — revenue outlook, cost risks, margin targets, actions required

### Python Analysis (`analysis.py`)
4 professional charts:
- `01_revenue_analysis.png` — budget vs actual by month + product line variance
- `02_cost_variance.png` — cost category variance + monthly cost trend
- `03_ebitda_margin.png` — monthly EBITDA + margin compression chart
- `04_fy_forecast.png` — full year revenue with trend overlay

### SQL Queries (`analysis_queries.sql`)
5 analytical queries:
- `Query 1` — Full year P&L summary with status flags
- `Query 2` — Revenue variance by product with H1/H2 split and trend
- `Query 3` — Cost variance with accelerating/stable classification
- `Query 4` — Monthly EBITDA bridge with YTD tracking
- `Query 5` — Top variance drivers ranked by EBITDA impact

---

## Dataset Description

**budget_vs_actual.csv** — 504 records (12 months × 6 products + 12 months × 6 cost categories)

| Column | Description |
|---|---|
| month | Month name (Jan–Dec) |
| month_num | Month number (1–12) |
| type | Revenue or Cost |
| category | Product line or cost category |
| budget | Budgeted amount (A$000s) |
| actual | Actual amount (A$000s) |
| variance | Actual minus budget |
| variance_pct | Variance as % of budget |

**monthly_summary.csv** — 12 rows, one per month with P&L totals

---

## Skills Demonstrated

| Category | Skills |
|---|---|
| SQL | CTEs, window functions (SUM OVER, RANK, AVG rolling), conditional aggregation |
| Python | pandas, matplotlib — budget vs actual, margin trend, waterfall |
| Financial Analysis | FP&A, variance analysis, EBITDA bridge, margin analysis |
| Business Writing | CFO-grade management commentary, product-level narrative |
| Domain Knowledge | Financial services P&L, product profitability, cost management |

---

*All data is synthetic and generated for portfolio demonstration purposes.*

*Part of a broader analytics portfolio — see also:*
- *[Brokerage Client Revenue & Churn Analysis](https://github.com/Suyashthakuri/brokerage-client-analytics)* — Client analytics
- *[ASX Fund Performance Report](https://github.com/Suyashthakuri/asx-fund-performance-q3-2024)* — Investment analytics
- *[ASX General Insurer KPI Dashboard](https://github.com/Suyashthakuri/asx-insurer-kpi-dashboard-)* — Power BI, DAX
