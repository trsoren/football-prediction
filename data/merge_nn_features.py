import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

WORK_DIR = '/Users/Patrick/stuff/school/448/football-prediction'
    

def main():


    # Read in the two csv files
    play_df = pd.read_csv('data/pass_play_data.csv')
    position_df = pd.read_csv('data/player_positions_basic.csv')


    # Merge the rows where the playId and gameId are the same in both files
    merged = pd.merge(play_df, position_df, on=['playId', 'gameId'])
    merged = merged.drop(['gameId', 'playId'], axis=1)

    # Remove "incomplete/complete" from outcome
    merged['outcome'] = merged['outcome'].str.replace('incomplete ', '')
    merged['outcome'] = merged['outcome'].str.replace('complete ', '')

    # Write the merged data to 2 new csvs for train and test
    train, test = train_test_split(merged, test_size=0.1, random_state=69)
    train.to_csv('nn_data_train.csv', index=False)
    test.to_csv('nn_data_test.csv', index=False)

if __name__ == '__main__':
    main()
