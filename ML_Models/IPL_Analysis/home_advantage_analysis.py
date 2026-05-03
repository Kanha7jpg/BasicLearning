import pandas as pd

df = pd.read_csv('matches.csv')

home_cities = {
    'Mumbai Indians': ['Mumbai'],
    'Chennai Super Kings': ['Chennai', 'Ranchi', 'Pune'], 
    'Royal Challengers Bangalore': ['Bangalore', 'Bengaluru'],
    'Kolkata Knight Riders': ['Kolkata', 'Cuttack'],
    'Delhi Daredevils': ['Delhi', 'Raipur'],
    'Delhi Capitals': ['Delhi', 'Raipur'],
    'Kings XI Punjab': ['Chandigarh', 'Indore', 'Dharamsala', 'Mohali'],
    'Punjab Kings': ['Chandigarh', 'Indore', 'Dharamsala', 'Mohali'],
    'Rajasthan Royals': ['Jaipur', 'Ahmedabad'],
    'Sunrisers Hyderabad': ['Hyderabad', 'Visakhapatnam'],
    'Deccan Chargers': ['Hyderabad', 'Cuttack', 'Nagpur', 'Visakhapatnam'],
    'Gujarat Lions': ['Rajkot', 'Kanpur'],
    'Rising Pune Supergiant': ['Pune'],
    'Rising Pune Supergiants': ['Pune'],
    'Pune Warriors': ['Pune'],
    'Gujarat Titans': ['Ahmedabad'],
    'Lucknow Super Giants': ['Lucknow']
}

def analyze_match(row):
    if pd.isna(row['winner']) or pd.isna(row['city']):
        return None
    
    city = row['city']
    team1 = row['team1']
    team2 = row['team2']
    winner = row['winner']
    
    # Are any of the playing teams at their home ground?
    t1_home = city in home_cities.get(team1, [])
    t2_home = city in home_cities.get(team2, [])
    
    # It is a true home game if exactly ONE team is at home
    if t1_home and not t2_home:
        home_team = team1
        away_team = team2
    elif t2_home and not t1_home:
        home_team = team2
        away_team = team1
    else:
        return None # Neutral venue
        
    return {
        'home_team': home_team,
        'away_team': away_team,
        'home_won': winner == home_team
    }

parsed_games = []
for idx, row in df.iterrows():
    res = analyze_match(row)
    if res is not None:
        parsed_games.append(res)

rdf = pd.DataFrame(parsed_games)
total = len(rdf)
home_wins = rdf['home_won'].sum()

print(f"Total Home Matches: {total}")
print(f"Home Team Wins: {home_wins} ({(home_wins/total)*100:.1f}%)")
print(f"Away Team Wins: {total - home_wins} ({((total-home_wins)/total)*100:.1f}%)")

# Let's break it down by team
team_stats = rdf.groupby('home_team')['home_won'].agg(['count', 'sum'])
team_stats.columns = ['home_matches', 'home_wins']
team_stats['home_win_pct'] = (team_stats['home_wins'] / team_stats['home_matches']) * 100
team_stats = team_stats.sort_values(by='home_win_pct', ascending=False)
print("\n=== Best Home Teams ===")
print(team_stats[team_stats['home_matches'] >= 10])

