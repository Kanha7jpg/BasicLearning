import pandas as pd
import matplotlib.pyplot as plt

# Load datasets
matches = pd.read_csv('matches.csv')
deliveries = pd.read_csv('deliveries.csv')

# We'll focus on the first innings score to determine which venue produces the highest scores.
# The 1st inning is the most untainted measure of a pitch's run-scoring potential, since
# the 2nd innings score is capped by the target.

first_innings_deliveries = deliveries[deliveries['inning'] == 1]
match_scores = first_innings_deliveries.groupby('match_id')['total_runs'].sum().reset_index()

# Merge with matches to get the venue
match_scores = match_scores.merge(matches[['id', 'venue']], left_on='match_id', right_on='id')

# Calculate the average 1st inning score per venue
# Filter out venues with fewer than 10 matches to avoid small sample size bias
venue_counts = match_scores['venue'].value_counts()
valid_venues = venue_counts[venue_counts >= 10].index

venue_avg_scores = match_scores[match_scores['venue'].isin(valid_venues)]
venue_avg_scores = venue_avg_scores.groupby('venue')['total_runs'].mean().sort_values(ascending=False).reset_index()

print("=== Top 10 Highest Scoring IPL Venues (Avg 1st Innings Score) ===")
for index, row in venue_avg_scores.head(10).iterrows():
    print(f"{index + 1}. {row['venue']}: {row['total_runs']:.1f} runs")

print("\n=== Why do these venues produce high scores? ===")
print("1. Geography & Altitude: Venues like M Chinnaswamy Stadium (Bangalore) and IS Bindra Stadium (Mohali) are at higher altitudes or have thin air, allowing the ball to travel further.")
print("2. Pitch Characteristics: Flat, hard tracks with even bounce (e.g., Wankhede Stadium, Eden Gardens) allow batsmen to hit through the line comfortably.")
print("3. Boundary Dimensions: Smaller boundaries (like Chinnaswamy and Holkar Stadium) naturally lead to more sixes and fours.")
print("4. Outfield Speed: Lush, fast outfields mean grounded shots easily reach the boundary.")
