#!python
import pandas as pd

# games = nflgame.games(2022, week=15)
# players = nflgame.combine_game_stats(games)
# for p in players.rushing().sort('rushing_yds').limit(5):
#     msg = '%s %d carries for %d yards and %d TDs'
#     print(msg % (p, p.rushing_att, p.rushing_yds, p.rushing_tds))

# Read in csv

input_files = ['raw/play_by_play_2009.csv', 'raw/play_by_play_2010.csv', 'raw/play_by_play_2011.csv', 'raw/play_by_play_2012.csv',
                'raw/play_by_play_2013.csv', 'raw/play_by_play_2014.csv', 'raw/play_by_play_2015.csv', 'raw/play_by_play_2016.csv',
                'raw/play_by_play_2017.csv', 'raw/play_by_play_2018.csv', 'raw/play_by_play_2019.csv', 'raw/play_by_play_2020.csv',
                'raw/play_by_play_2021.csv', 'raw/play_by_play_2022.csv']

for input in input_files:
    data = pd.read_csv(input)

    teams = ['ARI', 'ATL', 'BAL', 'BUF', 'CAR', 'CHI', 'CIN', 'CLE', 'DAL', 'DEN', 'DET', 'GB',
                'HOU', 'IND', 'JAX', 'KC', 'MIA', 'MIN', 'NE', 'NO', 'NYG', 'NYJ', 'LV', 'PHI',
                'PIT', 'LAC', 'SF', 'SEA', 'LA', 'TB', 'TEN', 'WAS']

    features = ['play_id', 'half_seconds_remaining', 'game_half', 'down', 'ydstogo', 'shotgun', 'no_huddle', 'posteam', 'defteam', 'play_type', 'posteam_timeouts_remaining', 'season', 'score_differential', 'penalty']
    selectlist =[x for x in data.columns if x in features]
    df = data[selectlist]

    df = df[df['play_type'].isin(['run', 'pass'])]
    df = df.replace({'Half1': 1, 'Half2': 2})


    # Add new columns to the DataFrame
    for team in teams:
        df[team + '_DEF'] = 0
        df[team + '_OFF'] = 0
        df = df.replace({'Half1': 1, 'Half2': 2, 'Overtime': 3})

    for index, row in df.iterrows():
        df.loc[index, row['posteam'] + '_OFF'] = 1
        df.loc[index, row['defteam'] + '_DEF'] = 1

    df['season'] -= 2009

    df['play_type'] = df['play_type'].replace({'run': 0, 'pass': 1})

    df = df[df['penalty'] != 1]
    df = df.drop(['play_id', 'posteam', 'defteam', 'penalty'], axis=1)
    df['game_half'] = df['game_half'].astype(int)
    df = df.dropna()
 

    df.to_csv('play_features.csv', index=False, mode='a', header=False)