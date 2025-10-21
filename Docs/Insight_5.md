# Insight 5: Role Versatility and Team Success

## Type of Finding:
This is a statistical finding because it measures and compares team outcomes as they relate to average Role Versatility Scores (RVS) for role and bench groups, then quantifies the relationship to win percentage using correlations and top–bottom quartile gaps.

---

### Details
This analysis tests whether teams with more versatile **role** and **bench** groups achieve higher win percentages.  
RVS is built from standardized `ts_percent`, winsorized `usg_percent`, `ast_per_game`, and inverse `tov_per_game` for players labeled **R** (role) or **B** (bench), then averaged to the team-season level by role group and linked to `win_pct`.

**Results:**
- **Correlation with Win%**  (`Insight_5_role_rvs_corr_vs_winpct.csv`)
  - Role (R): *r* = 0.358  
  - Bench (B): *r* = 0.140 
  
- **Top vs Bottom Quartile Win% Gap**  (`Insight_5_role_rvs_top_vs_bottom_gap.csv`)
  - Role (R): Q1 0.431 → Q4 0.573 — +0.141 gap  
  - Bench (B): Q1 0.448 → Q4 0.507 — +0.059 gap 

- Team win percentage rises meaningfully as role-group RVS increases (moderate positive relationship).  
- The bench-group relationship is positive but smaller in magnitude.  
- The role-group top–bottom quartile gap (+14.1 pts) indicates a practical advantage in the standings associated with higher versatility among non-starters who play regular roles; the bench-group gap is smaller (+5.9 pts).

---

## Why It Matters:
Teams do better when their non-star players help in lots of ways. The data shows that when role and bench players score efficiently, avoid turnovers, use possessions wisely, and set up teammates, win rates go up—especially when the role group is strong.
