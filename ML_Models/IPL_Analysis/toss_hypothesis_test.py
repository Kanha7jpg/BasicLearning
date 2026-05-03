import pandas as pd
from scipy.stats import chi2_contingency, binomtest

df = pd.read_csv('matches.csv')
df = df.dropna(subset=['winner', 'toss_winner', 'toss_decision'])
df['toss_win_match_win'] = df['toss_winner'] == df['winner']

print("=== 1. BINOMIAL TEST: Does winning toss = winning match? ===")
total_matches = len(df)
toss_winners_won_match = df['toss_win_match_win'].sum()
print(f"Total Matches: {total_matches}")
print(f"Matches won by Toss Winner: {toss_winners_won_match} ({(toss_winners_won_match/total_matches)*100:.2f}%)")
result = binomtest(k=toss_winners_won_match, n=total_matches, p=0.5, alternative='two-sided')
print(f"P-value: {result.pvalue:.4f}")

print("\n=== 2. CHI-SQUARE TEST: Does the toss decision (bat/field) affect match win rate for the toss winner? ===")
# Create a contingency table: Toss Decision vs whether Toss Winner won the match
contingency_table = pd.crosstab(df['toss_decision'], df['toss_win_match_win'])
print("Contingency Table (Toss Decision vs Match Win for Toss Winner):")
print(contingency_table)

chi2, p, dof, expected = chi2_contingency(contingency_table)
print(f"\nChi-Square Statistic: {chi2:.4f}")
print(f"P-value: {p:.4f}")
