# FP&A Budget vs Actual Variance Report — FY2024
**Author: Samip Thakuri** | Financial Analyst | Wichita, KS | [LinkedIn](https://linkedin.com/in/samipthakuri) · [Portfolio](https://samipdk.github.io/fin_portfolio/)

### CFO Management Pack for a US Financial Services Business Unit — SQL · Python · Power BI

---

## The Business Problem

A US Financial Services Business Unit CFO needs a full-year management pack that clearly answers:

1. Did we hit our revenue and EBITDA targets for FY2024?
2. Which product lines and cost categories drove the variances?
3. Where is the margin going and what needs management attention in FY2025?

This project delivers a complete CFO-grade management pack — from raw budget/actual data through to a written variance report with product-level analysis, cost bridge, and forward outlook.

---

## FY2024 Headline Results

| Metric | Budget | Actual | Variance |
|---|---|---|---|
| **Revenue** | $149,010k | $151,307k | **+$2,297k (+1.5%)** ✅ |
| **Total Costs** | $77,545k | $79,990k | **+$2,445k (+3.2%)** ❌ |
| **EBITDA** | $71,465k | $71,317k | **-$148k (-0.2%)** 🟡 |
| **EBITDA Margin** | 48.0% | 47.1% | **-0.9pp compression** ❌ |

**The story:** Revenue beat by +1.5% but costs grew faster (+3.2%), squeezing EBITDA margin by 0.9pp. The margin compression was driven by Technology (+13.5% over budget) and Marketing (+11.2% over budget). Without these two overruns, margin would have been approximately 47.9% — broadly on budget.

---

## Key Findings

**Revenue:**
- Digital Payments: +19.4% above budget — strongest performer, growth accelerating through H2
- Wealth Management: +8.6% above budget — consistent outperformance driven by FUM growth and advisory fees
- Business Lending: -9.2% below budget — significant miss driven by tightened credit appetite in SME segment; recovery plan required
- Retail Banking: -0.6% — broadly in line despite NIM pressure from deposit competition

**Costs:**
- Technology: +13.5% over budget — unbudgeted cloud infrastructure costs and vendor licence upgrades in H2
- Marketing: +11.2% over budget — unbudgeted Digital Payments campaign spend; commercially justified given revenue outperformance
- Compliance: +7.3% over budget — structural FDIC reporting requirement increases and three unbudgeted external reviews
- Facilities: +0.9% — well controlled

---

## Report Contents

### CFO Management Pack (`FPA_CFO_Management_Pack_FY2024.pptx`)
7-slide PowerPoint deck covering:
1. Title Slide — headline KPIs at a glance
2. Executive Summary — key messages and full P&L summary table
3. Revenue Performance — product line variance chart and commentary
4. Cost Performance — cost category variance chart and overrun analysis
5. EBITDA & Margin — KPI cards, EBITDA bridge table, margin compression analysis
6. FY2025 Outlook — revenue outlook by product + 5 management actions
7. Closing Summary — key takeaways

### Python Analysis (`analysis.py`)
4 professional charts saved to `outputs/`:
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
| budget | Budgeted amount ($000s USD) |
| actual | Actual amount ($000s USD) |
| variance | Actual minus budget |
| variance_pct | Variance as % of budget |

**monthly_summary.csv** — 12 rows, one per month with P&L totals

---

## Skills Demonstrated

| Category | Skills |
|---|---|
| SQL | CTEs, window functions (SUM OVER, RANK, AVG rolling), conditional aggregation |
| Python | pandas, matplotlib — budget vs actual, margin trend, variance charts |
| Financial Analysis | FP&A, variance analysis, EBITDA bridge, margin analysis, management commentary |
| Business Writing | CFO-grade executive summary, product-level narrative, forward outlook |
| Domain Knowledge | US financial services P&L, product profitability, cost management, FDIC compliance |

---

*All data is synthetic and generated for portfolio demonstration purposes. Scenario modeled on a US financial services business unit. All figures in USD. Regulatory references reflect US standards (FDIC, SOX).*

*Part of a broader analytics portfolio — see also:*
- *[Life Insurance KPI Dashboard](https://github.com/samipdk/AnalyticsDashboard)* — Power BI, DAX, actuarial KPIs
- *[Workforce & Economic Analytics Dashboard](https://github.com/samipdk/BLS_Dashboard)* — BLS labor market analysis, Power BI
- *[IPEDS Enrollment Analytics](https://github.com/samipdk/ipeds-enrollment-analytics)* — Higher education data, SQL, Power BI
