import pandas as pd
import numpy as np

# -------------------------------
# Load datasets
# -------------------------------
df1 = pd.read_csv(r"C:\Users\LENOVO\OneDrive\Desktop\ML\IPL-Data-Analysis\deliveries.csv", encoding="latin-1")
df2 = pd.read_csv(r"C:\Users\LENOVO\OneDrive\Desktop\ML\IPL-Data-Analysis\matches.csv", encoding="latin1")

# -------------------------------
# Display initial data
# -------------------------------
print("Dataset of Deliveries")
print(df1.head())

print("Dataset of matches")
print(df2.head())

# -------------------------------
# Deliveries dataset info
# -------------------------------
print("Deliveries Columns")
print(df1.columns)
print(df1.info())

# -------------------------------
# Top batsmen by total runs
# -------------------------------
# Group by batsman and sum total runs
group = df1.groupby('batsman')['total_runs'].sum()

# Sort batsmen by highest runs
sorted_list = group.sort_values(ascending=False)

# Display top 10 batsmen
print(sorted_list.head(10))

# -------------------------------
# Matches dataset info
# -------------------------------
print("Matches Columns")
print(df2.columns)
print(df2.info())

# -------------------------------
# Bowler Economy Calculation
# -------------------------------
# Total runs conceded by each bowler
runs = df1.groupby('bowler')['total_runs'].sum()

# Total balls bowled by each bowler
balls = df1.groupby('bowler')['total_runs'].count()

# Convert balls to overs
overs = balls / 6

# Calculate economy rate (runs per over)
economy = runs / overs

# Create DataFrame for bowler stats
eco_df = pd.DataFrame({
    'runs': runs,
    'balls': balls,
    'overs': overs,
    'economy': economy
})

# Filter bowlers who have bowled at least 60 balls
eco_df = eco_df[eco_df['balls'] >= 60]

# Sort by best (lowest) economy
eco_df = eco_df.sort_values(by='economy')

# Display top 10 economical bowlers
print(eco_df.head(10))

# -------------------------------
# Team Performance Analysis
# -------------------------------

# 1. Combine team1 and team2 into one column
teams = pd.concat([
    df2[['season', 'team1']].rename(columns={'team1': 'team'}),
    df2[['season', 'team2']].rename(columns={'team2': 'team'})
])

# 2. Count matches played by each team per season
matches_played = (
    teams.groupby(['season', 'team'])
         .size()
         .reset_index(name='matches')
)

# 3. Count matches won by each team per season
wins = (
    df2.dropna(subset=['winner'])              # remove matches without winner
        .groupby(['season', 'winner'])         # group by season and winning team
        .size()                                # count wins
        .reset_index(name='wins')              # convert to DataFrame
        .rename(columns={'winner': 'team'})    # rename column for merging
)

# 4. Merge matches played and wins
team_stats = matches_played.merge(
    wins,
    on=['season', 'team'],
    how='left'
)

# 5. Replace NaN wins with 0 (teams that didn't win any match)
team_stats['wins'] = team_stats['wins'].fillna(0)

# 6. Calculate win percentage
team_stats['win_percentage'] = (
    team_stats['wins'] / team_stats['matches']
) * 100

# 7. Round win percentage to 2 decimal places
team_stats['win_percentage'] = team_stats['win_percentage'].round(2)

# 8. Sort by season and highest win percentage
team_stats = team_stats.sort_values(
    ['season', 'win_percentage'],
    ascending=[True, False]
)

# 9. Display final result
print(team_stats)
