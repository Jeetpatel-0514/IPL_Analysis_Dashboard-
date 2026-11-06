import pandas as pd
import numpy as np

def prepare_data():
    print("Loading data...")
    matches = pd.read_csv('matches_clean.csv')
    deliveries = pd.read_csv('deliveries_clean.csv')
    
 
    print("Enhancing Matches Data...")
    
    # Determine Batting First and Chasing Team
    def get_batting_first(row):
        if row['toss_decision'] == 'bat':
            return row['toss_winner']
        else:
            return row['team1'] if row['toss_winner'] == row['team2'] else row['team2']
            
    def get_chasing_team(row):
        if row['toss_decision'] == 'field':
            return row['toss_winner']
        else:
            return row['team1'] if row['toss_winner'] == row['team2'] else row['team2']

    matches['batting_first'] = matches.apply(get_batting_first, axis=1)
    matches['chasing_team'] = matches.apply(get_chasing_team, axis=1)
    
    
    matches['toss_winner_is_match_winner'] = (matches['toss_winner'] == matches['winner']).astype(int)
    
   
    matches['bat_first_won'] = (matches['batting_first'] == matches['winner']).astype(int)
    
    
    if 'result' not in matches.columns:
         matches['result'] = np.where(matches['winner'] == matches['batting_first'], 'runs', 'wickets')
         
    matches.to_csv('matches_enhanced.csv', index=False)
    print("Created matches_enhanced.csv")
    
    
    print("Calculating Player Stats...")
    
    batting = deliveries.groupby('batter').agg(
        runs=('batsman_runs', 'sum'),
        balls_faced=('ball', 'count')
    ).reset_index()
    batting['strike_rate'] = (batting['runs'] / batting['balls_faced'] * 100).round(2)
    
    
    bowler_wickets = deliveries[
        (deliveries['is_wicket'] == 1) & 
        (~deliveries['dismissal_kind'].isin(['run out', 'retired hurt', 'obstructing the field']))
    ]
    bowling_w = bowler_wickets.groupby('bowler').agg(wickets=('is_wicket', 'count')).reset_index()
    
    bowling_runs = deliveries.groupby('bowler').agg(
        runs_conceded=('total_runs', 'sum'),
        balls_bowled=('ball', 'count')
    ).reset_index()
    
    bowling = pd.merge(bowling_runs, bowling_w, on='bowler', how='left').fillna(0)
    bowling['overs_bowled'] = bowling['balls_bowled'] / 6
    bowling['economy_rate'] = (bowling['runs_conceded'] / bowling['overs_bowled']).round(2)
    
    
    players = pd.merge(batting, bowling, left_on='batter', right_on='bowler', how='outer')
    players['player_name'] = players['batter'].combine_first(players['bowler'])
    players = players[['player_name', 'runs', 'balls_faced', 'strike_rate', 'wickets', 'runs_conceded', 'overs_bowled', 'economy_rate']].fillna(0)
    
    players.to_csv('player_stats_enhanced.csv', index=False)
    print("Created player_stats_enhanced.csv")

    
    print("Calculating Team Totals (with Sixes)...")
    
   
    deliveries['is_six'] = (deliveries['batsman_runs'] == 6).astype(int)
    deliveries['is_four'] = (deliveries['batsman_runs'] == 4).astype(int)
    
    team_totals = deliveries.groupby(['match_id', 'inning', 'batting_team', 'bowling_team']).agg(
        total_score=('total_runs', 'sum'),
        wickets_lost=('is_wicket', 'sum'),
        total_sixes=('is_six', 'sum'),
        total_fours=('is_four', 'sum')
    ).reset_index()
    team_totals.to_csv('team_innings_totals.csv', index=False)
    print("Created team_innings_totals.csv with boundary counts")
    
    
    print("Finding Season Winners...")
    
    if 'match_type' in matches.columns and 'Final' in matches['match_type'].values:
        finals = matches[matches['match_type'] == 'Final']
    else:
        
        matches['date'] = pd.to_datetime(matches['date'])
        finals_idx = matches.groupby('season')['date'].idxmax()
        finals = matches.loc[finals_idx]
        
    season_winners = finals[['season', 'winner']].rename(columns={'winner': 'season_winner'})
    season_winners = season_winners.sort_values('season')
    season_winners.to_csv('season_winners.csv', index=False)
    print("Created season_winners.csv")
    
    print("All done!")

if __name__ == '__main__':
    prepare_data()
