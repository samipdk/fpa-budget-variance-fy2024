"""
FP&A Budget vs Actual Variance Analysis — FY2024
Financial Services Business Unit
Author: Suyash Thakuri — Financial Data Analyst
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import json
import os

os.makedirs("outputs", exist_ok=True)

ACCENT  = "#1a6b4a"; ACCENT2 = "#2d9b6e"; RED   = "#c0392b"
AMBER   = "#e07b39"; NEUTRAL = "#6b7a8d"; DARK  = "#0f1419"
BGGRN   = "#e8f5f0"; BGRED   = "#fdf2f2"; BG    = "#fafbfc"

plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": BG,
    "axes.spines.top": False, "axes.spines.right": False,
    "font.family": "sans-serif", "axes.titlesize": 12,
    "axes.titleweight": "bold", "axes.labelsize": 10,
    "xtick.labelsize": 9, "ytick.labelsize": 9,
})

df      = pd.read_csv("budget_vs_actual.csv")
monthly = pd.read_csv("monthly_summary.csv")
with open("metrics.json") as f:
    m = json.load(f)

MONTHS_SHORT = ["J","F","M","A","M","J","J","A","S","O","N","D"]

print("=" * 60)
print("FP&A VARIANCE ANALYSIS — FY2024")
print("Financial Services Business Unit")
print("=" * 60)
print(f"\nRevenue:  Budget A${m['fy_rev_budget']:,.0f}k | Actual A${m['fy_rev_actual']:,.0f}k | Var {m['fy_rev_var_pct']:+.1f}%")
print(f"Costs:    Budget A${m['fy_cst_budget']:,.0f}k | Actual A${m['fy_cst_actual']:,.0f}k | Var +{m['fy_cst_variance']/m['fy_cst_budget']*100:.1f}%")
print(f"EBITDA:   Budget A${m['fy_ebitda_budget']:,.0f}k | Actual A${m['fy_ebitda_actual']:,.0f}k | Var A${m['fy_ebitda_variance']:+,.0f}k")
print(f"Margin:   Budget {m['fy_ebitda_margin_bud']}% | Actual {m['fy_ebitda_margin_act']}% | -0.9pp squeeze")

# ── CHART 1: REVENUE — Budget vs Actual + Waterfall ──────
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle("Revenue Performance — FY2024", fontsize=13, fontweight="bold")

ax = axes[0]
x = np.arange(12)
w = 0.38
ax.bar(x - w/2, monthly["revenue_budget"], w, color=NEUTRAL, alpha=0.6, label="Budget", edgecolor="none")
ax.bar(x + w/2, monthly["revenue_actual"], w,
       color=[ACCENT if v >= b else RED
              for v, b in zip(monthly["revenue_actual"], monthly["revenue_budget"])],
       alpha=0.85, label="Actual", edgecolor="none")
ax.set_xticks(x); ax.set_xticklabels(MONTHS_SHORT)
ax.set_ylabel("Revenue (A$000s)")
ax.set_title("Monthly revenue — budget vs actual")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_: f"${v:,.0f}k"))
ax.legend()

ax = axes[1]
rev_by_prod = df[df["type"]=="Revenue"].groupby("category").agg(
    budget=("budget","sum"), actual=("actual","sum"), variance=("variance","sum")
).sort_values("variance")
colors_p = [ACCENT if v >= 0 else RED for v in rev_by_prod["variance"]]
bars = ax.barh(rev_by_prod.index, rev_by_prod["variance"],
               color=colors_p, edgecolor="none", height=0.55)
ax.axvline(0, color=NEUTRAL, linewidth=0.8)
ax.set_xlabel("Variance vs budget (A$000s)")
ax.set_title("Revenue variance by product line")
for bar, val in zip(bars, rev_by_prod["variance"]):
    x_ = val + 20 if val >= 0 else val - 20
    ha = "left" if val >= 0 else "right"
    ax.text(x_, bar.get_y() + bar.get_height()/2,
            f"A${val:+,.0f}k", va="center", fontsize=8,
            color=ACCENT if val >= 0 else RED)

plt.tight_layout()
plt.savefig("outputs/01_revenue_analysis.png", dpi=150, bbox_inches="tight")
plt.close()
print("\nChart 1 saved: outputs/01_revenue_analysis.png")

# ── CHART 2: COST VARIANCE ────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle("Cost Variance Analysis — FY2024", fontsize=13, fontweight="bold")

ax = axes[0]
cost_by_cat = df[df["type"]=="Cost"].groupby("category").agg(
    budget=("budget","sum"), actual=("actual","sum"), variance=("variance","sum")
).sort_values("variance")
colors_c = [RED if v > 0 else ACCENT for v in cost_by_cat["variance"]]
bars = ax.barh(cost_by_cat.index, cost_by_cat["variance"],
               color=colors_c, edgecolor="none", height=0.55)
ax.axvline(0, color=NEUTRAL, linewidth=0.8)
ax.set_xlabel("Overspend vs budget (A$000s)")
ax.set_title("Cost variance by category")
for bar, val in zip(bars, cost_by_cat["variance"]):
    x_ = val + 10 if val >= 0 else val - 10
    ax.text(x_, bar.get_y() + bar.get_height()/2,
            f"A${val:+,.0f}k", va="center", fontsize=8,
            color=RED if val > 0 else ACCENT)

ax = axes[1]
ax.bar(np.arange(12) - 0.2, monthly["cost_budget"], 0.38, color=NEUTRAL, alpha=0.6, label="Budget", edgecolor="none")
ax.bar(np.arange(12) + 0.2, monthly["cost_actual"], 0.38,
       color=[RED if a > b else ACCENT for a,b in zip(monthly["cost_actual"],monthly["cost_budget"])],
       alpha=0.85, label="Actual", edgecolor="none")
ax.set_xticks(np.arange(12)); ax.set_xticklabels(MONTHS_SHORT)
ax.set_ylabel("Costs (A$000s)")
ax.set_title("Monthly costs — budget vs actual")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_: f"${v:,.0f}k"))
ax.legend()

plt.tight_layout()
plt.savefig("outputs/02_cost_variance.png", dpi=150, bbox_inches="tight")
plt.close()
print("Chart 2 saved: outputs/02_cost_variance.png")

# ── CHART 3: EBITDA & MARGIN ──────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle("EBITDA & Margin Analysis — FY2024", fontsize=13, fontweight="bold")

ax = axes[0]
ax.bar(np.arange(12) - 0.2, monthly["ebitda_budget"], 0.38,
       color=NEUTRAL, alpha=0.6, label="Budget", edgecolor="none")
ax.bar(np.arange(12) + 0.2, monthly["ebitda_actual"], 0.38,
       color=[ACCENT if a >= b else RED
              for a,b in zip(monthly["ebitda_actual"],monthly["ebitda_budget"])],
       alpha=0.85, label="Actual", edgecolor="none")
ax.set_xticks(np.arange(12)); ax.set_xticklabels(MONTHS_SHORT)
ax.set_ylabel("EBITDA (A$000s)")
ax.set_title("Monthly EBITDA — budget vs actual")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_: f"${v:,.0f}k"))
ax.legend()

ax = axes[1]
ax.plot(np.arange(12), monthly["ebitda_margin_budget"],
        color=NEUTRAL, linewidth=2, linestyle="--", marker="o", markersize=4, label="Budget margin")
ax.plot(np.arange(12), monthly["ebitda_margin_actual"],
        color=ACCENT, linewidth=2.5, marker="o", markersize=5, label="Actual margin")
ax.fill_between(np.arange(12),
                monthly["ebitda_margin_actual"],
                monthly["ebitda_margin_budget"],
                where=[a < b for a,b in zip(monthly["ebitda_margin_actual"],monthly["ebitda_margin_budget"])],
                alpha=0.15, color=RED, label="Margin compression")
ax.set_xticks(np.arange(12)); ax.set_xticklabels(MONTHS_SHORT)
ax.set_ylabel("EBITDA margin (%)")
ax.set_title("EBITDA margin trend — budget vs actual")
ax.yaxis.set_major_formatter(mticker.PercentFormatter())
ax.legend()
ax.annotate(f"FY: {m['fy_ebitda_margin_act']}% actual\nvs {m['fy_ebitda_margin_bud']}% budget",
            xy=(11, monthly["ebitda_margin_actual"].iloc[-1]),
            xytext=(-80, -25), textcoords="offset points",
            fontsize=8, color=AMBER,
            arrowprops=dict(arrowstyle="->", color=AMBER, lw=1))

plt.tight_layout()
plt.savefig("outputs/03_ebitda_margin.png", dpi=150, bbox_inches="tight")
plt.close()
print("Chart 3 saved: outputs/03_ebitda_margin.png")

# ── CHART 4: FORECAST ─────────────────────────────────────
fig, ax = plt.subplots(figsize=(14, 5))
fig.suptitle("Full Year Revenue Forecast — FY2024", fontsize=13, fontweight="bold")

ax.bar(np.arange(12), monthly["revenue_budget"],
       color=NEUTRAL, alpha=0.5, label="Budget", edgecolor="none", width=0.55)
ax.bar(np.arange(12), monthly["revenue_actual"],
       color=[ACCENT if a >= b else RED
              for a,b in zip(monthly["revenue_actual"],monthly["revenue_budget"])],
       alpha=0.8, label="Actual", edgecolor="none", width=0.35)
ax.plot(np.arange(12), monthly["revenue_actual"],
        color=AMBER, linewidth=2.5, linestyle=":", marker="D",
        markersize=4, label="Actual trend", zorder=4)
ax.axhline(monthly["revenue_budget"].mean(), color=NEUTRAL, linewidth=1,
           linestyle="--", alpha=0.5,
           label=f"Avg monthly budget: A${monthly['revenue_budget'].mean():,.0f}k")
ax.set_xticks(np.arange(12))
ax.set_xticklabels(MONTHS_SHORT)
ax.set_ylabel("Revenue (A$000s)")
ax.set_title("Monthly revenue with FY trend")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_: f"${v:,.0f}k"))
ax.legend(loc="upper left")
ax.annotate(f"FY Actual: A${m['fy_rev_actual']:,.0f}k\nvs Budget: A${m['fy_rev_budget']:,.0f}k\nVar: +{m['fy_rev_var_pct']}%",
            xy=(10, monthly['revenue_actual'].iloc[10]),
            xytext=(-100, 30), textcoords="offset points",
            fontsize=8, color=ACCENT, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=ACCENT, lw=1.2))

# Forecast line
forecast_vals = list(monthly["revenue_actual"])
plt.tight_layout()
plt.savefig("outputs/04_fy_forecast.png", dpi=150, bbox_inches="tight")
plt.close()
print("Chart 4 saved: outputs/04_fy_forecast.png")
print("\n=== ALL CHARTS GENERATED ===")
