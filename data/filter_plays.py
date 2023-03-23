import pandas as pd

# read CSV file into a data frame
data_bowl_df = pd.read_csv('data/data-bowl/plays.csv')

raw_df = pd.read_csv('data/plays/raw/play_by_play_2018.csv')

pass_df = data_bowl_df[data_bowl_df['playDescription'].str.contains(' pass ')]

# write filtered data frame to a CSV file
pass_df.to_csv('data/data-bowl/pass_only_plays.csv', index=False)

raw_df = raw_df.rename(columns={'play_id': 'playId', 'old_game_id': 'gameId'})

full_df = pd.merge(raw_df, pass_df, on=['playId', 'gameId'], how='inner')

full_df = full_df.loc[:, ['playId', 'gameId', 'half_seconds_remaining', 'playDescription', 'game_half', 'posteam_timeouts_remaining', 'down_x', 'ydstogo', 'no_huddle', 'score_differential', 'season']]

full_df = full_df.replace({'Half1': 1, 'Half2': 2, 'Overtime': 3})

full_df['season'] -= 2009

# define a function to extract the desired substring
def get_outcome(description):
    words = description.split()
    outcome = ""
    if "incomplete" in description:
        outcome += "incomplete "
    else:
        outcome += "complete "
    
    if " deep" in description:
        outcome += "deep "
    else:
        outcome += "short "
    
    if " left" in description or " left." in description:
        outcome += "left"
    elif " right" in description or " right." in description:
        outcome += "right"
    else:
        outcome += "middle"
    return outcome

full_df['outcome'] = full_df['playDescription'].apply(lambda x: get_outcome(x))

full_df = full_df.rename(columns={'down_x': 'down'})

full_df = full_df.drop(['playDescription'], axis=1)

full_df.to_csv('data/data-bowl/pass_play_data.csv', index=False)


# print the first few rows of the data frame
print(pass_df.head())