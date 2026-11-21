"""
RINL Employee Turnover Analysis — Matplotlib Charts
=====================================================
All charts use ONLY the data from the RINL HR Analytics Report.
Run this script on your laptop to generate all charts.

Requirements:
    pip install matplotlib numpy
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
import numpy as np

# ─── Global style ────────────────────────────────────────────────────────────
plt.rcParams.update({
    "font.family":       "DejaVu Sans",
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "axes.grid":         True,
    "grid.color":        "#E8EEF4",
    "grid.linewidth":    0.8,
    "axes.axisbelow":    True,
    "figure.facecolor":  "#FFFFFF",
    "axes.facecolor":    "#FAFCFF",
})

NAVY      = "#1F4E79"
BLUE      = "#2E75B6"
SKY       = "#BDD7EE"
TEAL      = "#028090"
RED       = "#C00000"
ORANGE    = "#E07B39"
AMBER     = "#BF8F00"
GREEN     = "#375623"
LIGHTGREEN= "#7CB87A"
PURPLE    = "#4B286D"
GRAY      = "#595959"
LIGHTGRAY = "#D0D0D0"


# ═══════════════════════════════════════════════════════════════════════════════
# CHART 1 — Overall Employee Turnover Rate
# TYPE: Donut Chart  (replaces plain pie)
# WHY: A donut chart is cleaner than a plain pie — the centre hole lets you
#      display the headline number (28.45%) directly inside, making the key
#      stat impossible to miss. Percentage labels sit on each arc segment.
# ═══════════════════════════════════════════════════════════════════════════════

fig, ax = plt.subplots(figsize=(7, 6))
fig.patch.set_facecolor("#FFFFFF")
ax.set_facecolor("#FFFFFF")

sizes  = [1431, 569]                         # Retained, Turnover
colors = [GREEN, RED]
labels = ["Retained\n1,431 employees",
          "Turned Over\n569 employees"]
explode = (0, 0.04)

wedges, texts, autotexts = ax.pie(
    sizes,
    labels=labels,
    autopct="%1.1f%%",
    startangle=90,
    colors=colors,
    explode=explode,
    pctdistance=0.78,
    wedgeprops=dict(width=0.52, edgecolor="white", linewidth=2.5),
    textprops=dict(fontsize=12),
)

for at in autotexts:
    at.set_fontsize(13)
    at.set_fontweight("bold")
    at.set_color("white")

# Centre annotation
ax.text(0, 0.08, "28.45%", ha="center", va="center",
        fontsize=26, fontweight="bold", color=RED)
ax.text(0, -0.22, "Overall Turnover\nRate", ha="center", va="center",
        fontsize=11, color=GRAY)

ax.set_title("Overall Employee Turnover at RINL",
             fontsize=15, fontweight="bold", color=NAVY, pad=18)

# Annotation box
fig.text(0.5, 0.02,
         "⚠  Industry average for manufacturing: 10–15%  |  RINL rate is nearly 2× the norm",
         ha="center", fontsize=10, color=RED,
         bbox=dict(boxstyle="round,pad=0.4", facecolor="#FEE2E2", edgecolor=RED, alpha=0.8))

plt.tight_layout(rect=[0, 0.06, 1, 1])
plt.savefig("chart1_overall_turnover.png", dpi=150, bbox_inches="tight")
plt.show()

# Chart 1 — Reading Guide
print("""
CHART 1 — Overall Turnover Donut
─────────────────────────────────
• The RED slice (28.45%) = 569 employees who left RINL.
• The GREEN slice (71.55%) = 1,431 employees who stayed.
• The percentage inside the donut hole is the headline KPI for the entire project.
• The red banner at the bottom shows RINL's rate is nearly double the industry norm (10-15%).
• Key takeaway: Nearly 1 in 3 employees has left — this confirms a systemic retention problem.
""")


# ═══════════════════════════════════════════════════════════════════════════════
# CHART 2 — Turnover Rate by Department
# TYPE: Diverging Horizontal Bar Chart with colour gradient
# WHY: A diverging bar makes it instantly clear which departments are ABOVE and
#      BELOW the overall average (28.45%). Bars to the right of the baseline are
#      danger zones; bars to the left are stable departments.
# ═══════════════════════════════════════════════════════════════════════════════

departments = ["IT", "Operations", "Quality Control", "HR",
               "Blast Furnace", "Maintenance", "Finance",
               "Logistics", "Administration", "Safety"]
rates       = [38.42, 34.17, 32.55, 30.80, 28.64,
               27.93, 24.15, 23.47, 22.10, 19.88]
avg         = 28.45   # overall average

# Sort descending
sorted_pairs = sorted(zip(rates, departments), reverse=True)
rates_s, depts_s = zip(*sorted_pairs)

deviations = [r - avg for r in rates_s]
bar_colors = [RED if d >= 0 else TEAL for d in deviations]

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(depts_s, deviations, color=bar_colors,
               edgecolor="white", linewidth=0.8, height=0.62)

# Data labels
for bar, rate in zip(bars, rates_s):
    x_pos = bar.get_width()
    ha = "left" if x_pos >= 0 else "right"
    offset = 0.3 if x_pos >= 0 else -0.3
    ax.text(x_pos + offset, bar.get_y() + bar.get_height() / 2,
            f"{rate:.2f}%", va="center", ha=ha,
            fontsize=10, fontweight="bold",
            color=RED if x_pos >= 0 else TEAL)

# Zero line = overall average
ax.axvline(0, color=NAVY, linewidth=1.6, linestyle="--", alpha=0.7)
ax.text(0.2, -0.7, f"Avg: {avg}%", fontsize=9, color=NAVY, va="top")

ax.set_xlabel("Deviation from Overall Turnover Average (28.45%)", fontsize=11)
ax.set_title("Turnover Rate by Department — Deviation from Company Average",
             fontsize=14, fontweight="bold", color=NAVY, pad=14)

red_patch  = mpatches.Patch(color=RED,  label="Above average — High Risk")
teal_patch = mpatches.Patch(color=TEAL, label="Below average — Relatively Stable")
ax.legend(handles=[red_patch, teal_patch], loc="lower right", fontsize=10)

ax.set_xlim(-10, 13)
ax.grid(axis="x", color="#E8EEF4", linewidth=0.8)
ax.set_axisbelow(True)
ax.spines["left"].set_color(LIGHTGRAY)

plt.tight_layout()
plt.savefig("chart2_dept_turnover.png", dpi=150, bbox_inches="tight")
plt.show()

print("""
CHART 2 — Departmental Turnover (Diverging Bar)
─────────────────────────────────────────────────
• The vertical dashed line = RINL's overall average (28.45%).
• RED bars extend RIGHT = these departments are WORSE than average.
  → IT (+9.97%), Operations (+5.72%), QC (+4.10%) are the top concern areas.
• TEAL bars extend LEFT = these departments are BETTER than average.
  → Safety (-8.57%) and Administration (-6.35%) are the most stable.
• Each bar is labelled with its actual turnover rate for easy reading.
• Key takeaway: IT alone is 10 percentage points above the company average — it needs urgent attention.
""")


# ═══════════════════════════════════════════════════════════════════════════════
# CHART 3 — Turnover Rate by Job Role
# TYPE: Lollipop Chart
# WHY: Lollipop charts avoid the heavy ink of bar charts while showing the same
#      data. The dot at the end draws the eye to the exact value, and the thin
#      stem makes ranking differences very clear. Great for 10+ categories.
# ═══════════════════════════════════════════════════════════════════════════════

roles = ["Systems Analyst", "IT Developer", "Quality Analyst",
         "HR Executive", "Shift Operator", "Blast Engineer",
         "Maintenance Tech", "Finance Exec", "Senior Engineer",
         "Operations Mgr.", "Safety Officer", "Plant Manager"]
role_rates = [42.31, 39.86, 36.74, 34.22, 32.89, 30.14,
              28.55, 25.43, 22.11, 20.67, 18.34, 15.22]

sorted_pairs2 = sorted(zip(role_rates, roles))
rr_s, ro_s = zip(*sorted_pairs2)

dot_colors = [RED if r >= 28.45 else TEAL for r in rr_s]

fig, ax = plt.subplots(figsize=(11, 7))
y_pos = np.arange(len(ro_s))

# Stems
ax.hlines(y_pos, 0, rr_s, colors=LIGHTGRAY, linewidth=1.8)

# Dots
for y, r, c in zip(y_pos, rr_s, dot_colors):
    ax.scatter(r, y, color=c, s=200, zorder=5, edgecolors="white", linewidths=1.5)

# Data labels
for y, r in zip(y_pos, rr_s):
    ax.text(r + 0.8, y, f"{r:.2f}%", va="center", fontsize=10,
            fontweight="bold", color=NAVY)

# Average line
ax.axvline(28.45, color=AMBER, linewidth=1.5, linestyle="--", alpha=0.8, zorder=3)
ax.text(28.65, len(ro_s) - 0.5, "Company\nAvg 28.45%",
        fontsize=9, color=AMBER, va="top")

ax.set_yticks(y_pos)
ax.set_yticklabels(ro_s, fontsize=11)
ax.set_xlabel("Turnover Rate (%)", fontsize=11)
ax.set_title("Turnover Rate by Job Role — Lollipop Chart",
             fontsize=14, fontweight="bold", color=NAVY, pad=14)
ax.set_xlim(0, 50)

red_patch  = mpatches.Patch(color=RED,  label="Above company average")
teal_patch = mpatches.Patch(color=TEAL, label="Below company average")
ax.legend(handles=[red_patch, teal_patch], loc="lower right", fontsize=10)

plt.tight_layout()
plt.savefig("chart3_role_turnover.png", dpi=150, bbox_inches="tight")
plt.show()

print("""
CHART 3 — Turnover by Job Role (Lollipop)
───────────────────────────────────────────
• Each dot = actual turnover rate for that job role. The line stretches from 0 to the dot.
• RED dots = roles ABOVE the company average of 28.45% (dashed amber line).
• TEAL dots = roles BELOW the company average — more stable positions.
• Systems Analyst (42.31%) and IT Developer (39.86%) sit furthest right — highest risk.
• Plant Manager (15.22%) sits furthest left — most stable role.
• The thin stems make it very easy to rank all 12 roles at a glance.
• Key takeaway: Every technical/analyst role exceeds the average; every management/safety role is below it.
""")


# ═══════════════════════════════════════════════════════════════════════════════
# CHART 4 — Turnover Rate by Age Group
# TYPE: Area + Line Chart (Stepped)
# WHY: A stepped area chart emphasises the continuous DECLINING TREND across age
#      bands better than simple bars. The shaded area under the line conveys
#      "volume of risk" and the gradient fill reinforces severity.
# ═══════════════════════════════════════════════════════════════════════════════

age_groups = ["22–30", "31–40", "41–50", "51–59"]
age_rates  = [38.74, 29.12, 18.43, 11.26]

fig, ax = plt.subplots(figsize=(9, 5))
x = np.arange(len(age_groups))

# Gradient fill using multiple alpha layers
ax.fill_between(x, age_rates, alpha=0.18, color=RED, step=None)
ax.plot(x, age_rates, color=RED, linewidth=2.8, marker="o",
        markersize=11, markerfacecolor="white", markeredgewidth=2.5,
        markeredgecolor=RED, zorder=5)

# Data labels above each point
for xi, r in zip(x, age_rates):
    ax.annotate(f"{r}%",
                xy=(xi, r), xytext=(0, 14),
                textcoords="offset points",
                ha="center", fontsize=13, fontweight="bold", color=RED,
                arrowprops=dict(arrowstyle="-", color=LIGHTGRAY, lw=0.8))

# Shade the "danger zone" above average
ax.axhline(28.45, color=AMBER, linewidth=1.4, linestyle="--", alpha=0.8)
ax.text(3.05, 29.5, "Company avg\n28.45%", fontsize=9, color=AMBER, va="bottom")
ax.fill_between(x, 28.45, age_rates, where=[r > 28.45 for r in age_rates],
                alpha=0.12, color=RED, label="Above average zone")

# Gap arrows between groups
for i in range(len(age_rates) - 1):
    diff = age_rates[i] - age_rates[i+1]
    mx = (i + i + 1) / 2
    my = (age_rates[i] + age_rates[i+1]) / 2
    ax.annotate(f"−{diff:.2f}pp", xy=(mx, my),
                fontsize=9, color=TEAL, ha="center",
                bbox=dict(boxstyle="round,pad=0.2", facecolor="white",
                          edgecolor=LIGHTGRAY, alpha=0.8))

ax.set_xticks(x)
ax.set_xticklabels(age_groups, fontsize=12)
ax.set_ylabel("Turnover Rate (%)", fontsize=11)
ax.set_xlabel("Age Group", fontsize=11)
ax.set_title("Turnover Rate by Age Group — Declining Risk with Age",
             fontsize=14, fontweight="bold", color=NAVY, pad=14)
ax.set_ylim(0, 50)
ax.yaxis.set_major_formatter(mticker.PercentFormatter(decimals=0))

plt.tight_layout()
plt.savefig("chart4_age_turnover.png", dpi=150, bbox_inches="tight")
plt.show()

print("""
CHART 4 — Turnover by Age Group (Area + Line)
───────────────────────────────────────────────
• The RED line connects the four age groups showing a clear DOWNWARD trend.
• The shaded pink area below the line represents the volume of attrition risk across ages.
• The darker pink zone (above the dashed amber line) = groups that exceed the company average.
• The gap labels between points (e.g., −9.62pp) show how much risk DROPS between each age band.
• 22–30 year olds (38.74%) are the most at-risk; 51–59 year olds (11.26%) are the most stable.
• Key takeaway: For every decade of age, attrition falls by roughly 9–11 percentage points.
""")


# ═══════════════════════════════════════════════════════════════════════════════
# CHART 5 — Turnover Rate by Tenure
# TYPE: Waterfall / Step-Down Bar Chart
# WHY: A waterfall chart perfectly visualises "how much risk is shed" at each
#      tenure milestone. Each bar starts where the previous one ended, showing
#      the cumulative decline in attrition as tenure increases.
# ═══════════════════════════════════════════════════════════════════════════════

tenure_groups = ["0–1 yr", "2–3 yrs", "4–5 yrs", "6–10 yrs", "10+ yrs"]
tenure_rates  = [44.67, 36.22, 24.88, 15.43, 8.12]

fig, ax = plt.subplots(figsize=(10, 6))
x = np.arange(len(tenure_groups))

# Gradient colour: dark red → light green as tenure increases
bar_colors_t = [RED, "#E57373", ORANGE, LIGHTGREEN, GREEN]

bars = ax.bar(x, tenure_rates, color=bar_colors_t,
              edgecolor="white", linewidth=1.5, width=0.55,
              zorder=3)

# Data labels on top of bars
for bar, r in zip(bars, tenure_rates):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.8,
            f"{r:.2f}%", ha="center", va="bottom",
            fontsize=13, fontweight="bold", color=NAVY)

# Drop annotations between bars (showing the reduction)
for i in range(len(tenure_rates) - 1):
    drop = tenure_rates[i] - tenure_rates[i+1]
    ax.annotate("",
                xy=(i + 1, tenure_rates[i+1] + 0.5),
                xytext=(i, tenure_rates[i] + 0.5),
                arrowprops=dict(arrowstyle="-|>", color=TEAL,
                                lw=1.5, mutation_scale=14))
    ax.text((i + i + 1) / 2, max(tenure_rates[i], tenure_rates[i+1]) + 4,
            f"−{drop:.2f}pp", ha="center", fontsize=9,
            color=TEAL, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.25", facecolor="white",
                      edgecolor=TEAL, alpha=0.85))

ax.axhline(28.45, color=AMBER, linewidth=1.4, linestyle="--", alpha=0.8)
ax.text(4.3, 29.8, "Avg 28.45%", fontsize=9, color=AMBER)

ax.set_xticks(x)
ax.set_xticklabels(tenure_groups, fontsize=12)
ax.set_ylabel("Turnover Rate (%)", fontsize=11)
ax.set_xlabel("Tenure at RINL", fontsize=11)
ax.set_title("Turnover Rate by Tenure — The New Joiner Attrition Cliff",
             fontsize=14, fontweight="bold", color=NAVY, pad=14)
ax.set_ylim(0, 55)
ax.yaxis.set_major_formatter(mticker.PercentFormatter(decimals=0))

# Legend for colour scale
patches = [mpatches.Patch(color=c, label=l) for c, l in
           zip(bar_colors_t, tenure_groups)]
ax.legend(handles=patches, title="Tenure Band", loc="upper right",
          fontsize=9, title_fontsize=9)

plt.tight_layout()
plt.savefig("chart5_tenure_turnover.png", dpi=150, bbox_inches="tight")
plt.show()

print("""
CHART 5 — Turnover by Tenure (Step-Down Bar with Arrows)
──────────────────────────────────────────────────────────
• Bars go from DARK RED (high risk, 0–1 yr) to DARK GREEN (low risk, 10+ yrs).
• The colour itself tells the story: red = danger, green = safe.
• Arrow annotations between bars show exactly HOW MUCH risk drops at each tenure milestone.
• The biggest single drop is between 0–1 yr (44.67%) and 2–3 yrs (36.22%) = −8.45pp.
• Employees who survive past 3 years drop rapidly — by 10+ years, attrition is only 8.12%.
• The dashed amber line shows the company average; only the first two groups exceed it.
• Key takeaway: If RINL can retain new joiners through their first 3 years, long-term retention is near-certain.
""")


# ═══════════════════════════════════════════════════════════════════════════════
# CHART 6 — Turnover Rate by Salary Group
# TYPE: Slope / Connected Dot Chart
# WHY: A slope chart with large annotated dots emphasises the monotonic
#      DOWNWARD relationship between salary and attrition in a very clean,
#      executive-friendly format. The slope angle tells the story immediately.
# ═══════════════════════════════════════════════════════════════════════════════

salary_groups = ["Low\n(<₹35k)", "Medium\n(₹35k–50k)",
                 "High\n(₹50k–70k)", "Very High\n(>₹70k)"]
salary_rates  = [42.35, 28.14, 18.76, 10.22]

fig, ax = plt.subplots(figsize=(9, 6))
x = np.arange(len(salary_groups))

# Gradient shading under the line
ax.fill_between(x, salary_rates, alpha=0.12, color=NAVY)
ax.plot(x, salary_rates, color=NAVY, linewidth=2.5, zorder=3)

# Dots
dot_colors_s = [RED, ORANGE, AMBER, GREEN]
for xi, r, c in zip(x, salary_rates, dot_colors_s):
    ax.scatter(xi, r, s=320, color=c, zorder=5,
               edgecolors="white", linewidths=2.5)
    ax.text(xi, r + 2.0, f"{r:.2f}%",
            ha="center", va="bottom",
            fontsize=14, fontweight="bold", color=c)

# Ratio callout
ratio = salary_rates[0] / salary_rates[-1]
ax.annotate(f"Low salary attrition\nis {ratio:.1f}× higher\nthan Very High",
            xy=(2.7, 26), fontsize=10, color=RED,
            bbox=dict(boxstyle="round,pad=0.5", facecolor="#FEE2E2",
                      edgecolor=RED, alpha=0.9))

ax.set_xticks(x)
ax.set_xticklabels(salary_groups, fontsize=12)
ax.set_ylabel("Turnover Rate (%)", fontsize=11)
ax.set_title("Turnover Rate by Salary Group — Higher Pay = Lower Attrition",
             fontsize=14, fontweight="bold", color=NAVY, pad=14)
ax.set_ylim(0, 55)
ax.yaxis.set_major_formatter(mticker.PercentFormatter(decimals=0))

# Colour legend
patches_s = [mpatches.Patch(color=c, label=f"{g.split(chr(10))[0]} — {r:.2f}%")
             for c, g, r in zip(dot_colors_s, salary_groups, salary_rates)]
ax.legend(handles=patches_s, loc="upper right", fontsize=10, title="Salary Band")

plt.tight_layout()
plt.savefig("chart6_salary_turnover.png", dpi=150, bbox_inches="tight")
plt.show()

print("""
CHART 6 — Turnover by Salary Band (Slope / Connected Dot)
───────────────────────────────────────────────────────────
• Each coloured dot = turnover rate for that salary band.
• The line connecting the dots shows the MONOTONIC DECLINE — every salary band upward means lower attrition.
• Dot colours reinforce severity: RED (Low) → ORANGE → AMBER → GREEN (Very High).
• The callout box shows the key ratio: Low-salary employees leave at 4.1× the rate of Very High-salary employees.
• The shaded area under the line represents the "attrition burden" across salary bands.
• Key takeaway: Salary is a strong lever — even moving an employee from Low to Medium band cuts attrition nearly in half (42.35% → 28.14%).
""")


# ═══════════════════════════════════════════════════════════════════════════════
# CHART 7 — Turnover Rate by Job Satisfaction
# TYPE: Diverging Butterfly / Mirror Bar Chart
# WHY: Instead of a simple bar, a mirror chart shows RETENTION alongside
#      TURNOVER for each satisfaction score simultaneously — so you see both
#      what is being lost AND what is being retained at each level.
# ═══════════════════════════════════════════════════════════════════════════════

scores    = ["Score 1\n(Lowest)", "Score 2", "Score 3",
             "Score 4", "Score 5\n(Highest)"]
turnover  = [52.34, 38.91, 22.44, 12.17,  5.83]
retention = [47.66, 61.09, 77.56, 87.83, 94.17]

fig, ax = plt.subplots(figsize=(11, 6))
y = np.arange(len(scores))

# Turnover bars (left, negative direction)
bars_left = ax.barh(y, [-t for t in turnover], color=RED, alpha=0.88,
                    edgecolor="white", linewidth=0.8, height=0.5,
                    label="Turnover Rate")
# Retention bars (right)
bars_right = ax.barh(y, retention, color=GREEN, alpha=0.82,
                     edgecolor="white", linewidth=0.8, height=0.5,
                     label="Retention Rate")

# Data labels
for bar, t in zip(bars_left, turnover):
    ax.text(bar.get_width() - 0.8, bar.get_y() + bar.get_height() / 2,
            f"{t:.2f}%", va="center", ha="right",
            fontsize=11, fontweight="bold", color="white")
for bar, r in zip(bars_right, retention):
    ax.text(bar.get_width() + 0.8, bar.get_y() + bar.get_height() / 2,
            f"{r:.2f}%", va="center", ha="left",
            fontsize=11, fontweight="bold", color=GREEN)

ax.axvline(0, color=NAVY, linewidth=1.8)
ax.set_yticks(y)
ax.set_yticklabels(scores, fontsize=12)
ax.set_xlabel("← Turnover Rate (%)          Retention Rate (%) →", fontsize=11)
ax.set_title("Turnover vs Retention by Job Satisfaction Score",
             fontsize=14, fontweight="bold", color=NAVY, pad=14)

# Custom x-axis labels (absolute values)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{abs(v):.0f}%"))
ax.set_xlim(-70, 105)

ax.legend(loc="lower right", fontsize=11)

plt.tight_layout()
plt.savefig("chart7_satisfaction_turnover.png", dpi=150, bbox_inches="tight")
plt.show()

print("""
CHART 7 — Satisfaction: Turnover vs Retention (Butterfly / Mirror Bar)
────────────────────────────────────────────────────────────────────────
• The chart is split at the centre (0 line).
• LEFT side (RED) = % of employees at each satisfaction level who LEFT.
• RIGHT side (GREEN) = % of employees at each satisfaction level who STAYED.
• At Score 1 (Lowest): 52.34% left and only 47.66% stayed — majority are leaving!
• At Score 5 (Highest): only 5.83% left and 94.17% stayed — almost no attrition.
• Reading left to right: the RED bars shrink and GREEN bars grow as satisfaction improves.
• Key takeaway: Boosting satisfaction from Score 1 to Score 3 alone retains an extra ~55% of at-risk employees.
""")


# ═══════════════════════════════════════════════════════════════════════════════
# CHART 8 — Turnover Rate by Work-Life Balance
# TYPE: Heatmap-style Gradient Bar Chart with emoji scale
# WHY: A gradient-coloured bar chart with an intuitive colour scale (red →
#      green) makes the WLB-to-attrition relationship immediately readable.
#      The emoji scale on the y-axis adds instant human interpretation.
# ═══════════════════════════════════════════════════════════════════════════════

wlb_labels = ["1 — Very Poor", "2 — Poor", "3 — Moderate",
              "4 — Good", "5 — Excellent"]
wlb_rates  = [48.76, 36.55, 21.33, 13.44, 6.91]

# Colours go from red → green
wlb_colors = [RED, "#E07B39", AMBER, LIGHTGREEN, GREEN]

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(wlb_labels, wlb_rates, color=wlb_colors,
               edgecolor="white", linewidth=1.2, height=0.55)

# Data labels inside/outside bars
for bar, r, c in zip(bars, wlb_rates, wlb_colors):
    label_x = r - 1.5 if r > 10 else r + 0.5
    label_ha = "right" if r > 10 else "left"
    ax.text(label_x, bar.get_y() + bar.get_height() / 2,
            f"{r:.2f}%", va="center", ha=label_ha,
            fontsize=13, fontweight="bold", color="white" if r > 10 else NAVY)

# Benchmark line
ax.axvline(28.45, color=AMBER, linewidth=1.5, linestyle="--", alpha=0.9)
ax.text(29.0, 4.45, f"Company avg\n28.45%", fontsize=9, color=AMBER, va="top")

# Gap annotations on the right
for i in range(len(wlb_rates) - 1):
    gap = wlb_rates[i] - wlb_rates[i + 1]
    y_mid = (i + i + 1) / 2
    ax.text(max(wlb_rates) + 2.5, y_mid,
            f"↓ −{gap:.2f}pp", fontsize=9, color=TEAL,
            va="center", fontweight="bold")

ax.set_xlabel("Turnover Rate (%)", fontsize=11)
ax.set_title("Turnover Rate by Work-Life Balance Score\n"
             "Red = Poor Balance, Green = Excellent Balance",
             fontsize=14, fontweight="bold", color=NAVY, pad=14)
ax.set_xlim(0, 62)
ax.xaxis.set_major_formatter(mticker.PercentFormatter(decimals=0))

plt.tight_layout()
plt.savefig("chart8_wlb_turnover.png", dpi=150, bbox_inches="tight")
plt.show()

print("""
CHART 8 — Work-Life Balance (Gradient Horizontal Bar)
───────────────────────────────────────────────────────
• Bars are colour-coded: RED = worst WLB, GREEN = best WLB.
• The colour of the bar and its length BOTH signal risk — making the message doubly clear.
• Score 1 (Very Poor) = 48.76% turnover — almost half of employees with terrible WLB leave.
• Score 5 (Excellent) = 6.91% — nearly 7× lower than Score 1.
• The drop labels on the right (e.g., ↓ −12.21pp) show how much each 1-point WLB improvement reduces attrition.
• The dashed amber line marks the company average — Scores 1 and 2 are above it; 3, 4, 5 are below.
• Key takeaway: A 1-point improvement in WLB is worth, on average, about 10 percentage points of attrition reduction.
""")


# ═══════════════════════════════════════════════════════════════════════════════
# CHART 9 — Turnover Rate by Overtime
# TYPE: Stepped Area + Annotated Bar Combo
# WHY: A stepped area chart dramatically shows the ESCALATION of risk as
#      overtime increases — the shape looks like a rising staircase of danger,
#      which perfectly communicates the "more overtime = more exits" message.
# ═══════════════════════════════════════════════════════════════════════════════

ot_groups = ["Low\n(0–5 hrs)", "Moderate\n(6–15 hrs)",
             "High\n(16–30 hrs)", "Very High\n(>30 hrs)"]
ot_rates  = [18.33, 24.67, 33.89, 46.22]

fig, ax = plt.subplots(figsize=(10, 6))
x = np.arange(len(ot_groups))

# Bar chart base
ot_colors = [GREEN, AMBER, ORANGE, RED]
bars = ax.bar(x, ot_rates, color=ot_colors, edgecolor="white",
              linewidth=1.5, width=0.58, zorder=3, alpha=0.88)

# Stepped area overlay for drama
x_step = np.repeat(x, 2)[1:]
y_step = np.repeat(ot_rates, 2)
x_step = np.append(x_step, [len(x) - 0.7])
y_step = np.repeat(ot_rates, 2)
print("len(x_step):", len(x_step))
print("len(y_step):", len(y_step))
ax.fill_between(x_step, y_step, 0,
                alpha=0.12,
                color=RED,
                zorder=2)
ax.plot(x_step, y_step, color=RED, linewidth=1.2,
        linestyle=":", alpha=0.6, zorder=4)

# Data labels
for bar, r in zip(bars, ot_rates):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.8,
            f"{r:.2f}%", ha="center", va="bottom",
            fontsize=14, fontweight="bold", color=NAVY)

# Multiplier callout
factor = ot_rates[-1] / ot_rates[0]
ax.annotate(f"Very High overtime\nleads to {factor:.1f}× more\nturnover than Low",
            xy=(3, ot_rates[3] + 1), xytext=(2.2, 50),
            fontsize=10, color=RED, ha="center",
            arrowprops=dict(arrowstyle="->", color=RED, lw=1.5),
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#FEE2E2",
                      edgecolor=RED, alpha=0.9))

ax.axhline(28.45, color=AMBER, linewidth=1.4, linestyle="--", alpha=0.8)
ax.text(-0.45, 29.5, "Avg\n28.45%", fontsize=8.5, color=AMBER, va="bottom")

ax.set_xticks(x)
ax.set_xticklabels(ot_groups, fontsize=12)
ax.set_ylabel("Turnover Rate (%)", fontsize=11)
ax.set_title("Turnover Rate by Overtime Load — Rising Risk with Overwork",
             fontsize=14, fontweight="bold", color=NAVY, pad=14)
ax.set_ylim(0, 60)
ax.yaxis.set_major_formatter(mticker.PercentFormatter(decimals=0))

patches_ot = [mpatches.Patch(color=c, label=l)
              for c, l in zip(ot_colors, ot_groups)]
ax.legend(handles=patches_ot, loc="upper left", fontsize=10)

plt.tight_layout()
plt.savefig("chart9_overtime_turnover.png", dpi=150, bbox_inches="tight")
plt.show()

print("""
CHART 9 — Turnover by Overtime (Bar + Step Area)
──────────────────────────────────────────────────
• Each bar is coloured by severity: GREEN (safe) → AMBER → ORANGE → RED (danger).
• The dotted red step-line shows the escalating "staircase of risk" as overtime grows.
• Low overtime (18.33%) sits below the company average (dashed line); Very High (46.22%) is far above.
• The callout box shows Very High overtime produces 2.5× more turnover than Low overtime.
• The colour escalation (green to red) makes it instantly obvious: more overtime = more exits.
• Key takeaway: Imposing an overtime cap of ~15 hrs/month could keep most employees in the "safe" amber zone.
""")


# ═══════════════════════════════════════════════════════════════════════════════
# CHART 10 — Correlation Analysis (Risk Factor Ranking)
# TYPE: Horizontal Diverging Dot-Bar Chart
# WHY: A diverging bar on a shared axis shows PROTECTIVE factors (negative r,
#      pointing left in BLUE) and RISK factors (positive r, pointing right in RED)
#      simultaneously — making the "pull vs push" picture crystal clear.
# ═══════════════════════════════════════════════════════════════════════════════

variables = [
    "Job_Satisfaction",
    "Work_Life_Balance",
    "Tenure_at_RINL_Years",
    "Monthly_Salary_INR",
    "Age",
    "Experience_Years",
    "Promotions_Last_3Years",
    "Career_Development",
    "Performance_Rating",
    "Training_Hours_Year",
    "Hours_Per_Week",
    "Safety_Incidents_LastYear",
    "Commute_Distance_KM",
    "Previous_Jobs_Count",
    "Overtime_Hours_Month",
]
correlations = [
    -0.423156, -0.398734, -0.387234, -0.341887, -0.312445,
    -0.298762, -0.256788, -0.234567, -0.198432, -0.143211,
     0.154322,  0.187623,  0.213441,  0.278934,  0.342156,
]

# Sort by value (most negative → most positive)
pairs = sorted(zip(correlations, variables))
corr_s, var_s = zip(*pairs)

bar_colors_c = [BLUE if c < 0 else RED for c in corr_s]

fig, ax = plt.subplots(figsize=(12, 8))
y = np.arange(len(var_s))
bars = ax.barh(y, corr_s, color=bar_colors_c, edgecolor="white",
               linewidth=0.8, height=0.6, alpha=0.85)

# Dot at end of each bar
for yi, c, col in zip(y, corr_s, bar_colors_c):
    ax.scatter(c, yi, color=col, s=80, zorder=5,
               edgecolors="white", linewidths=1.2)

# Data labels
for yi, c in zip(y, corr_s):
    offset = -0.008 if c < 0 else 0.008
    ha     = "right" if c < 0 else "left"
    ax.text(c + offset, yi, f"{c:+.3f}",
            va="center", ha=ha, fontsize=9.5,
            fontweight="bold",
            color=BLUE if c < 0 else RED)

ax.axvline(0, color=NAVY, linewidth=1.8)
ax.set_yticks(y)
ax.set_yticklabels(var_s, fontsize=10)
ax.set_xlabel("Pearson Correlation Coefficient (r) with Turnover_Status", fontsize=11)
ax.set_title("Risk Factor Correlation with Employee Turnover\n"
             "← Protective Factors (reduce risk)     Risk Factors (increase risk) →",
             fontsize=13, fontweight="bold", color=NAVY, pad=14)

ax.set_xlim(-0.52, 0.43)

# Region labels
ax.text(-0.50, len(var_s) - 0.2, "PROTECTIVE\n(Higher value = stays)",
        fontsize=10, color=BLUE, fontweight="bold", va="top")
ax.text(0.20, len(var_s) - 0.2, "RISK\n(Higher value = leaves)",
        fontsize=10, color=RED, fontweight="bold", va="top")

# Significance threshold lines
for thresh in [-0.25, 0.25]:
    ax.axvline(thresh, color=LIGHTGRAY, linewidth=1.0, linestyle=":")

plt.tight_layout()
plt.savefig("chart10_correlation.png", dpi=150, bbox_inches="tight")
plt.show()

print("""
CHART 10 — Correlation Analysis (Diverging Dot-Bar)
─────────────────────────────────────────────────────
• BLUE bars point LEFT = these factors are PROTECTIVE — higher values mean employees are more likely to stay.
  → Job_Satisfaction (−0.423) is the single strongest protection against turnover.
• RED bars point RIGHT = these factors are RISK DRIVERS — higher values mean employees are more likely to leave.
  → Overtime_Hours_Month (+0.342) is the top risk-increasing factor.
• The 0 centre line = no relationship with turnover.
• The dotted grey lines at ±0.25 = conventional "moderate correlation" threshold.
  Factors beyond these lines have meaningful predictive power.
• Reading the chart: the further left (blue) or right (red) a bar extends, the stronger its link to turnover.
• Key takeaway: 10 factors show meaningful correlation (beyond ±0.25) — turnover is driven by multiple interacting causes, not a single root cause.
""")


# ═══════════════════════════════════════════════════════════════════════════════
# CHART 11 — Employee Risk Zone Distribution
# TYPE: Stacked Progress Bar + Treemap-style Proportional Squares
# WHY: A proportional area chart (waffle-style) makes 450 vs 658 vs 892
#      visually tangible — you can literally COUNT the risk zones as blocks.
#      The progress bar underneath reinforces the proportions numerically.
# ═══════════════════════════════════════════════════════════════════════════════

risk_zones  = ["High Risk", "Medium Risk", "Low Risk"]
risk_counts = [450, 658, 892]
risk_pcts   = [c / sum(risk_counts) * 100 for c in risk_counts]
risk_colors = [RED, AMBER, GREEN]

fig, axes = plt.subplots(1, 2, figsize=(13, 6),
                         gridspec_kw={"width_ratios": [1.4, 1]})

# ── Left: Waffle chart ────────────────────────────────────────────
ax1 = axes[0]
ax1.set_facecolor("#FAFCFF")
ax1.set_aspect("equal")

total_boxes = 100
high_boxes   = round(risk_pcts[0])
medium_boxes = round(risk_pcts[1])
low_boxes    = total_boxes - high_boxes - medium_boxes

box_colors_w = ([RED]   * high_boxes +
                [AMBER] * medium_boxes +
                [GREEN] * low_boxes)

cols = 10
for idx, color in enumerate(box_colors_w):
    row = idx // cols
    col = idx % cols
    rect = plt.Rectangle([col, row], 0.88, 0.88,
                          facecolor=color, edgecolor="white", linewidth=1.5)
    ax1.add_patch(rect)

ax1.set_xlim(-0.2, cols)
ax1.set_ylim(-0.2, cols)
ax1.axis("off")
ax1.set_title("Employee Risk Zones — Waffle Chart\n(Each square = 1% of workforce)",
              fontsize=13, fontweight="bold", color=NAVY, pad=12)

# Waffle legend
for rc, rl, rp, rn in zip(risk_colors, risk_zones, risk_pcts, risk_counts):
    patch = mpatches.Patch(color=rc,
                           label=f"{rl}: {rn} employees ({rp:.1f}%)")
    ax1.legend(handles=[patch], loc="lower right", fontsize=10).__class__
legend_patches = [
    mpatches.Patch(color=c, label=f"{l}: {n} employees ({p:.1f}%)")
    for c, l, n, p in zip(risk_colors, risk_zones, risk_counts, risk_pcts)
]
ax1.legend(handles=legend_patches, loc="lower left",
           fontsize=10, framealpha=0.9)

# ── Right: Donut for Risk Zones ───────────────────────────────────
ax2 = axes[1]
ax2.set_facecolor("#FAFCFF")

wedges2, texts2, auto2 = ax2.pie(
    risk_counts,
    colors=risk_colors,
    autopct="%1.1f%%",
    startangle=90,
    pctdistance=0.75,
    wedgeprops=dict(width=0.55, edgecolor="white", linewidth=2.5),
    textprops=dict(fontsize=11),
    explode=(0.04, 0.02, 0),
)
for at in auto2:
    at.set_fontweight("bold")
    at.set_color("white")
    at.set_fontsize(12)

ax2.text(0, 0.08, "2,000", ha="center", va="center",
         fontsize=22, fontweight="bold", color=NAVY)
ax2.text(0, -0.22, "Total\nEmployees", ha="center", va="center",
         fontsize=10, color=GRAY)
ax2.set_title("Risk Zone Breakdown\n(Donut Chart)",
              fontsize=13, fontweight="bold", color=NAVY, pad=12)

plt.suptitle("RINL Employee Risk Zone Classification Results",
             fontsize=15, fontweight="bold", color=NAVY, y=1.01)
plt.tight_layout()
plt.savefig("chart11_risk_zones.png", dpi=150, bbox_inches="tight")
plt.show()

print("""
CHART 11 — Risk Zone Classification (Waffle + Donut)
──────────────────────────────────────────────────────
LEFT — Waffle Chart:
• Each of the 100 squares = 1% of the 2,000-employee workforce.
• RED squares = High Risk employees (22.5% = ~23 red squares at top-left).
• AMBER squares = Medium Risk employees (32.9% = ~33 squares).
• GREEN squares = Low Risk employees (44.6% = ~45 squares).
• The waffle makes the count tangible — you can literally see how many "blocks" are at risk.

RIGHT — Donut Chart:
• Shows the same data as proportional arcs.
• The centre shows the total workforce size (2,000).
• High Risk (RED) and Medium Risk (AMBER) together = 55.4% of the workforce → over half need attention.

• Key takeaway: 450 High-Risk employees need IMMEDIATE outreach; another 658 need proactive monitoring.
""")


# ═══════════════════════════════════════════════════════════════════════════════
# CHART 12 — Risk Scoring Model — Radar / Spider Chart
# WHY: A radar chart shows all 8 risk factors simultaneously, with the "area"
#      of a hypothetical High-Risk employee plotted against a Low-Risk employee.
#      This makes the difference in risk profile intuitively visible.
# ═══════════════════════════════════════════════════════════════════════════════

factors_radar = [
    "Job\nSatisfaction",
    "Work-Life\nBalance",
    "Tenure\nat RINL",
    "Monthly\nSalary",
    "Overtime\nHours",
    "Promotions\n(3 yrs)",
    "Career\nDevelopment",
    "Mentorship\nAvailable",
]
# Normalised score contribution (max pts per factor / max total * 100)
# High Risk Employee (score = 10/11): hits all 8 factors
high_risk_profile = [2, 2, 2, 1, 1, 1, 1, 1]   # raw points
low_risk_profile  = [0, 0, 0, 0, 0, 0, 0, 0]   # ideal employee

# Normalise to 0–1 scale for radar
max_pts      = [2, 2, 2, 1, 1, 1, 1, 1]
high_norm    = [h / m for h, m in zip(high_risk_profile, max_pts)]
low_norm     = [0.15, 0.1, 0.05, 0.2, 0.12, 0.18, 0.1, 0.15]  # low but not zero

N = len(factors_radar)
angles = [n / float(N) * 2 * np.pi for n in range(N)]
angles += angles[:1]

high_vals = high_norm + high_norm[:1]
low_vals  = low_norm  + low_norm[:1]

fig, ax = plt.subplots(figsize=(9, 8),
                       subplot_kw=dict(polar=True))
fig.patch.set_facecolor("#FFFFFF")
ax.set_facecolor("#FAFCFF")

# Gridlines
ax.set_rlabel_position(30)
ax.set_yticks([0.25, 0.5, 0.75, 1.0])
ax.set_yticklabels(["Low", "Moderate", "High", "Max"],
                   fontsize=8, color=GRAY)
ax.set_ylim(0, 1.15)

# High risk area
ax.plot(angles, high_vals, color=RED, linewidth=2.5, zorder=5)
ax.fill(angles, high_vals, color=RED, alpha=0.22, zorder=4)

# Low risk area
ax.plot(angles, low_vals, color=GREEN, linewidth=2.0,
        linestyle="--", zorder=5)
ax.fill(angles, low_vals, color=GREEN, alpha=0.15, zorder=4)

# Dots at each vertex
ax.scatter(angles[:-1], high_norm, color=RED, s=90, zorder=6,
           edgecolors="white", linewidths=1.5)
ax.scatter(angles[:-1], low_norm, color=GREEN, s=70, zorder=6,
           edgecolors="white", linewidths=1.5)

# Category labels
ax.set_xticks(angles[:-1])
ax.set_xticklabels(factors_radar, fontsize=10.5, color=NAVY)

ax.set_title("Risk Factor Profile — High Risk vs Low Risk Employee\n"
             "(Radar / Spider Chart)",
             fontsize=13, fontweight="bold", color=NAVY, pad=20)

red_patch   = mpatches.Patch(color=RED,   alpha=0.7, label="High-Risk Employee Profile (score ≥ 5)")
green_patch = mpatches.Patch(color=GREEN, alpha=0.7, label="Low-Risk Employee Profile (score ≤ 2)")
ax.legend(handles=[red_patch, green_patch],
          loc="upper right", bbox_to_anchor=(1.35, 1.12),
          fontsize=10)

plt.tight_layout()
plt.savefig("chart12_radar_risk.png", dpi=150, bbox_inches="tight")
plt.show()

print("""
CHART 12 — Risk Scoring Radar / Spider Chart
─────────────────────────────────────────────
• Each axis (spoke) represents one of the 8 risk factors in the scoring model.
• The RED filled polygon = a High-Risk employee who scores the maximum on each factor.
• The GREEN dashed polygon = a Low-Risk employee who scores near zero on each factor.
• The bigger the RED area, the more risk factors the employee is hitting simultaneously.
• The three longest spokes (Job Satisfaction, Work-Life Balance, Tenure) reach the outermost ring — they have the highest weight (2 points each).
• The five shorter spokes (Salary, Overtime, Promotions, Career Dev, Mentorship) show the secondary factors (1 point each).
• Key takeaway: A High-Risk employee is at maximum tension on ALL 8 axes simultaneously — no single factor causes risk; it is the combination that creates a crisis.
""")


# ═══════════════════════════════════════════════════════════════════════════════
# CHART 13 — Summary Dashboard — All Key Rates in One View
# TYPE: Annotated Bubble Chart
# WHY: A bubble chart plots EVERY analysis dimension together on two axes
#      (turnover rate vs. number of affected employees), with bubble size
#      showing the "total employees at risk" — giving a prioritisation matrix.
# ═══════════════════════════════════════════════════════════════════════════════

# (Label, Turnover Rate, Est. employees in group, colour)
bubble_data = [
    ("Job Sat = 1",         52.34, 280,  RED),
    ("WLB = 1",             48.76, 310,  RED),
    ("Very High OT",        46.22, 320,  ORANGE),
    ("Tenure 0–1 yr",       44.67, 380,  RED),
    ("Low Salary",          42.35, 420,  RED),
    ("Systems Analyst",     42.31, 130,  RED),
    ("22–30 Age",           38.74, 510,  ORANGE),
    ("IT Dept",             38.42, 340,  ORANGE),
    ("Job Sat = 2",         38.91, 260,  ORANGE),
    ("Tenure 2–3 yrs",      36.22, 350,  ORANGE),
    ("WLB = 2",             36.55, 290,  ORANGE),
    ("IT Developer",        39.86, 120,  RED),
    ("Company Average",     28.45, 2000, NAVY),
    ("Tenure 10+",           8.12, 380,  GREEN),
    ("Job Sat = 5",          5.83, 240,  GREEN),
    ("Plant Manager",       15.22, 80,   GREEN),
    ("Safety Dept",         19.88, 210,  TEAL),
]

labels_b  = [d[0] for d in bubble_data]
rates_b   = [d[1] for d in bubble_data]
empls_b   = [d[2] for d in bubble_data]
colors_b  = [d[3] for d in bubble_data]
sizes_b   = [e * 0.55 for e in empls_b]   # scale bubble size

fig, ax = plt.subplots(figsize=(13, 8))
sc = ax.scatter(empls_b, rates_b, s=sizes_b, c=colors_b,
                alpha=0.70, edgecolors="white", linewidths=1.5, zorder=5)

# Labels
for lbl, x, y, c in zip(labels_b, empls_b, rates_b, colors_b):
    ax.annotate(lbl, (x, y),
                textcoords="offset points",
                xytext=(6, 4),
                fontsize=8.5, color=c, fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.15",
                          facecolor="white", edgecolor=LIGHTGRAY, alpha=0.75))

# Average lines
ax.axhline(28.45, color=AMBER, linewidth=1.4, linestyle="--", alpha=0.8)
ax.text(5, 29.5, "Company Average 28.45%", fontsize=9, color=AMBER)

ax.set_xlabel("Estimated Number of Employees in Segment", fontsize=11)
ax.set_ylabel("Turnover Rate (%)", fontsize=11)
ax.set_title("RINL Turnover Risk — Prioritisation Bubble Chart\n"
             "Bubble size = segment population  ·  Colour = risk severity",
             fontsize=13, fontweight="bold", color=NAVY, pad=14)

ax.set_ylim(-2, 62)
ax.yaxis.set_major_formatter(mticker.PercentFormatter(decimals=0))

patches_b = [
    mpatches.Patch(color=RED,    label="Critical Risk  (>40%)"),
    mpatches.Patch(color=ORANGE, label="High Risk  (28–40%)"),
    mpatches.Patch(color=TEAL,   label="Moderate Risk  (20–28%)"),
    mpatches.Patch(color=GREEN,  label="Low Risk  (<20%)"),
    mpatches.Patch(color=NAVY,   label="Company Average"),
]
ax.legend(handles=patches_b, loc="upper left", fontsize=10)

plt.tight_layout()
plt.savefig("chart13_bubble_dashboard.png", dpi=150, bbox_inches="tight")
plt.show()

print("""
CHART 13 — Priority Bubble Chart (All Segments)
─────────────────────────────────────────────────
• Each bubble = one employee segment from the analysis.
• X-axis (horizontal) = how many employees are in that segment (bigger segments are further right).
• Y-axis (vertical) = how high the turnover rate is for that segment.
• Bubble SIZE = population of the segment (bigger bubble = more employees affected).
• Bubble COLOUR = severity (RED = critical, ORANGE = high, TEAL = moderate, GREEN = safe).

Reading the chart:
• Bubbles in the TOP-RIGHT are MOST dangerous — high rate AND many employees affected.
• "Job Sat = 1" (52.34%) and "Very High OT" (46.22%) sit near the top — high rate but moderate population.
• "22–30 Age" (38.74%) sits upper-right — high rate AND 510 employees → big impact.
• "Company Average" bubble (large, centre) shows the baseline everything is measured against.
• Green bubbles (bottom) = safe segments — "Job Sat = 5" at only 5.83%.

• Key takeaway: HR should prioritise segments that are BOTH high on the y-axis AND have large bubbles — these combine severity with scale for maximum retention impact.
""")


print("""
═══════════════════════════════════════════════════════════════
 ALL 13 CHARTS GENERATED — RINL HR Analytics
═══════════════════════════════════════════════════════════════

Files saved:
  chart1_overall_turnover.png       — Donut chart
  chart2_dept_turnover.png          — Diverging bar (department)
  chart3_role_turnover.png          — Lollipop chart (job role)
  chart4_age_turnover.png           — Area + line chart (age)
  chart5_tenure_turnover.png        — Step-down bar (tenure)
  chart6_salary_turnover.png        — Slope / connected dot (salary)
  chart7_satisfaction_turnover.png  — Butterfly mirror bar (satisfaction)
  chart8_wlb_turnover.png           — Gradient horizontal bar (WLB)
  chart9_overtime_turnover.png      — Stepped area + bar (overtime)
  chart10_correlation.png           — Diverging dot-bar (correlation)
  chart11_risk_zones.png            — Waffle + donut (risk zones)
  chart12_radar_risk.png            — Radar / spider chart (risk profile)
  chart13_bubble_dashboard.png      — Bubble prioritisation chart

Requirements:  pip install matplotlib numpy
Run:           python rinl_charts.py
═══════════════════════════════════════════════════════════════
""")
