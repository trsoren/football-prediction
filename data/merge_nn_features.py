import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random

WORK_DIR = '/Users/Patrick/stuff/school/448/football-prediction'
    

def main():


    # Read in the two csv files
    play_df = pd.read_csv('data/pass_play_data.csv')
    position_df = pd.read_csv('data/player_positions_basic.csv')


    # Merge the rows where the playId and gameId are the same in both files
    merged = pd.merge(play_df, position_df, on=['playId', 'gameId'])

    merged = merged.drop(['gameId', 'playId'], axis=1)

    # Write the merged data to a new csv file
    merged.to_csv('nn_data.csv', index=False)

    print(len(merged.columns))

if __name__ == '__main__':
    main()
