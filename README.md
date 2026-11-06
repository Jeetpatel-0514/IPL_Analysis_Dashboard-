# IPL Data Analytics & Dashboard Project

Comprehensive data analytics project on Indian Premier League (IPL) cricket match and delivery datasets. This repository contains scripts for data cleaning, data transformation, dashboard metrics calculation, and reports for Power BI visualization.

---

## 📁 Repository Structure

```text
├── Cleaning.py                  # Initial data cleaning, team name harmonization & validation
├── prepare_dashboard_data.py    # Feature engineering & dashboard-ready metrics generation
├── PowerBI_Dashboard_Roadmap.md # Guide for Power BI modeling, visuals & DAX measures
├── deliveries.csv               # Raw IPL delivery-level dataset
├── deliveries_clean.csv         # Cleaned delivery dataset
├── matches.csv                  # Raw IPL match-level dataset
├── matches_clean.csv            # Cleaned match dataset
├── matches_enhanced.csv         # Enhanced match dataset with batting first/chasing & outcomes
├── player_stats_enhanced.csv    # Batting and bowling aggregated performance metrics
├── team_innings_totals.csv      # Per-match innings score aggregates (totals, boundaries, wickets)
├── season_winners.csv           # Season champion mappings
└── reports & presentations/     # Project documentation, presentations, and reports
```

---

## ⚙️ Data Pipeline

1. **Cleaning (`Cleaning.py`)**:
   - Standardizes team renames across all seasons (e.g., Delhi Daredevils → Delhi Capitals, Kings XI Punjab → Punjab Kings, RCB rename).
   - Formats date strings to datetime and standardizes season formats.
   - Handles missing values (`city`, `method`).
   - Produces `deliveries_clean.csv` and `matches_clean.csv`.

2. **Feature Engineering & Dashboard Data (`prepare_dashboard_data.py`)**:
   - Identifies batting first vs. chasing teams based on toss decisions.
   - Computes toss impact and bat-first win correlations.
   - Calculates player batting strike rates, total runs, wickets, and bowling economy rates.
   - Aggregates team match-level innings totals and season champions.

---

## 📊 Power BI Dashboard

See [PowerBI_Dashboard_Roadmap.md](PowerBI_Dashboard_Roadmap.md) for detailed data relationships and DAX measures.

