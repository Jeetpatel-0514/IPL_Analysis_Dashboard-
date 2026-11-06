import pandas as pd

deliveries = pd.read_csv('deliveries.csv')
matches = pd.read_csv('matches.csv')

print(deliveries.info())
print(matches.info())

team_map = {
    'Delhi Daredevils': 'Delhi Capitals',
    'Deccan Chargers': 'Sunrisers Hyderabad',
    'Kings XI Punjab': 'Punjab Kings',
    'Royal Challengers Bangalore': 'Royal Challengers Bengaluru',
    'Rising Pune Supergiant': 'Rising Pune Supergiants'
}

# Apply to every column that holds a team name
for col in ['batting_team', 'bowling_team']:
    deliveries[col] = deliveries[col].replace(team_map)

for col in ['team1', 'team2', 'toss_winner', 'winner']:
    matches[col] = matches[col].replace(team_map)


matches['date'] = pd.to_datetime(matches['date'], format='%d-%m-%Y')

matches['season'] = matches['season'].str[:4]  # keeps just the starting year, e.g. '2007'

matches['city'] = matches['city'].fillna('Unknown')
matches['method'] = matches['method'].fillna('Standard')

print(deliveries.duplicated().sum())
print(matches.duplicated().sum())

print(deliveries['batsman_runs'].unique())   # should be 0,1,2,3,4,6 (and rarely 5)
print(deliveries['over'].unique())           # should be within valid range
print(matches['result_margin'].min())        # shouldn't be negative


deliveries.to_csv('deliveries_clean.csv', index=False)
matches.to_csv('matches_clean.csv', index=False)


print("Files successfully saved to your current working directory!")