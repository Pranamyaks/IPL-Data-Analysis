import pandas as pd
import numpy as np

df1=pd.read_csv(r"C:\Users\LENOVO\OneDrive\Desktop\ML\IPL-Data-Analysis\deliveries.csv",encoding="latin-1")

df2=pd.read_csv(r"C:\Users\LENOVO\OneDrive\Desktop\ML\IPL-Data-Analysis\matches.csv",encoding="latin1")

print("Dataset of Deliveries")
print(df1.head())

print("Dataset of matches")
print(df2.head())

print("Deliveries Columns")
print(df1.columns)
print(df1.info())

group=df1.groupby('batsman')['total_runs'].sum()
print(group)

sorted_list=group.sort_values(ascending=False)
print(sorted_list)

print(sorted_list.head(10))

print("Matches Columns")
print(df2.columns)
print(df2.info())

runs=df1.groupby('bowler')['total_runs'].sum()
balls=df1.groupby('bowler')['total_runs'].count()
print(runs)
print(balls)

overs=balls/6
economy=runs/overs

eco_df=pd.DataFrame({
    'runs' : runs,
    'balls' :balls,
    'overs' : overs,
    'economy' : economy 
})

eco_df=eco_df[eco_df['balls'] >= 60]

eco_df=eco_df.sort_values(by='economy')

print(eco_df.head(10))'''

# 1. Combine team1 and team2
teams = pd.concat([
    df2[['season', 'team1']].rename(columns={'team1': 'team'}),
    df2[['season', 'team2']].rename(columns={'team2': 'team'})
])
#print(teams)

# 2. Count matches played by each team in each season
matches_played = (
    teams.groupby(['season', 'team'])
         .size()
         .reset_index(name='matches')
)
#print(matches_played)


# 3. Count matches won by each team in each season
wins = (
    df2.dropna(subset=['winner'])
           .groupby(['season', 'winner'])
           .size()
           .reset_index(name='wins')
           .rename(columns={'winner': 'team'})
)
print(wins)


# 4. Combine matches played and wins
team_stats = matches_played.merge(
    wins,
    on=['season', 'team'],
    how='left'
)

# 5. Teams with no wins → 0
team_stats['wins'] = team_stats['wins'].fillna(0)

# 6. Calculate win percentage
team_stats['win_percentage'] = (
    team_stats['wins'] / team_stats['matches']
) * 100

# 7. Round percentage
team_stats['win_percentage'] = team_stats['win_percentage'].round(2)

# 8. Sort by season and win percentage
team_stats = team_stats.sort_values(
    ['season', 'win_percentage'],
    ascending=[True, False]
)

# 9. Display result
print(team_stats)




