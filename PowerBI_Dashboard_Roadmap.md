# IPL Power BI Dashboard - Development Roadmap

This document outlines the steps we took to prepare the IPL datasets and provides a guide on how to build the dashboard visuals in Power BI, including necessary DAX formulas.

## 1. Data Preparation Phase (Completed)
We identified that the raw `matches_clean.csv` and `deliveries_clean.csv` files were missing specific columns required to replicate the dashboard screenshots. To solve this, a Python script (`prepare_dashboard_data.py`) was executed to generate four new enriched datasets:

*   **`matches_enhanced.csv`**: Contains new columns like `batting_first`, `chasing_team`, `toss_winner_is_match_winner`, and `bat_first_won`.
*   **`player_stats_enhanced.csv`**: Aggregated player statistics including total `runs`, `balls_faced`, `strike_rate`, `wickets`, and `economy_rate`.
*   **`team_innings_totals.csv`**: Per-match team totals including `total_score`, `wickets_lost`, `total_sixes`, and `total_fours`.
*   **`season_winners.csv`**: A mapping of each IPL season to the team that won the final match.

---

## 2. Power BI Setup Phase

### Step 1: Import Data
1. Open Power BI Desktop.
2. Click **Get Data** -> **Text/CSV**.
3. Import the following 4 files:
   - `matches_enhanced.csv`
   - `player_stats_enhanced.csv`
   - `team_innings_totals.csv`
   - `season_winners.csv`

### Step 2: Create Relationships (Data Modeling)
Go to the **Model View** (the third icon on the left sidebar) and link the tables:
- Drag `match_id` from `team_innings_totals` to `id` in `matches_enhanced`.
- Drag `season` from `season_winners` to `season` in `matches_enhanced` (if needed for filtering).

---

## 3. Building the Visuals (Drag and Drop)

Power BI handles most metrics automatically using standard aggregations. 

*   **Total Runs / Most Sixes:** Drag `total_score` or `total_sixes` into a chart. Power BI will default to `Sum`.
*   **Matches Played:** Drag `id` from `matches_enhanced` into a card or chart and set aggregation to `Count`.
*   **Average 1st Innings Score:** Drag `total_score` to a chart, filter `inning = 1`, and change aggregation from `Sum` to `Average`.
*   **Highest Team Total:** Drag `total_score` to a chart and change aggregation to `Maximum`.
*   **Player Insights:** Use `player_stats_enhanced` directly. Drag `player_name` alongside `strike_rate`, `runs`, or `wickets` into bar charts or scatter plots.

---

## 4. DAX Formulas (For Advanced Metrics)

For dynamic percentages that respond to slicers/filters, you will need to create **New Measures**. Right-click on your table in Power BI, select "New Measure", and paste these formulas:

### Win Percentage
```dax
Win Percentage = 
DIVIDE(
    COUNTROWS(FILTER('matches_enhanced', 'matches_enhanced'[winner] = SELECTEDVALUE('matches_enhanced'[team1]))), 
    COUNTROWS('matches_enhanced'), 
    0
)
```

### Toss Win to Match Win Percentage
```dax
Toss Win % = 
DIVIDE(
    SUM('matches_enhanced'[toss_winner_is_match_winner]), 
    COUNT('matches_enhanced'[id]), 
    0
)
```

### Batting First Win Percentage
```dax
Bat First Win % = 
DIVIDE(
    SUM('matches_enhanced'[bat_first_won]), 
    COUNT('matches_enhanced'[id]), 
    0
)
```

---

## 5. Next Steps / Troubleshooting
- Start by building the **Overview** page first using Card visuals for high-level stats (Total Seasons, Total Matches).
- Use **Slicers** at the top of your dashboard for `Season`, `Team`, and `Venue`.
- If a chart looks wrong, check the **Aggregation type** (e.g., make sure it's set to Average instead of Sum).
- If you need a more specific DAX formula for complex charts (like Head-to-Head matrices or Best Win Streaks), refer back to the AI assistant for custom formulas!
