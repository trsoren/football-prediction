import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random

WORK_DIR = '/Users/trsorensen/Code/EECS448/football'
NEW_X_RANGE = (0, 60)
NEW_Y_RANGE = (0, 27)

def calculate_x_coords(group):
    new_x_range = NEW_X_RANGE
    x_range_size = new_x_range[1] - new_x_range[0]
    x_scaled = group.x / 120.0
    # fix coords that are out of bounds for some reason?
    x_scaled[x_scaled < 0] = 0
    x_scaled[x_scaled > 1] = 1
    new_x = np.round(x_scaled * x_range_size).astype(int)
    # Flip coords based on play direction so offense always drives same direction
    new_x[group.playDirection == 'right'] = new_x_range[1] - new_x
    return new_x

def calculate_y_coords(group):
    new_y_range = NEW_Y_RANGE
    y_range_size = new_y_range[1] - new_y_range[0]
    y_scaled = group.y / 53.3
    # fix coords that are out of bounds for some reason?
    y_scaled[y_scaled < 0] = 0
    y_scaled[y_scaled > 1] = 1
    new_y = np.round(y_scaled * y_range_size).astype(int)
    # Flip coords based on play direction so offense always drives same direction
    new_y[group.playDirection == 'right'] = new_y_range[1] - new_y
    return new_y
    

def main():
    # Read in all data and merge into single dataframe
    dfs = []
    for i in range(1, 18):
        dfs.append(pd.read_csv(WORK_DIR + f'/data/data-bowl/week{i}.csv'))
    df = pd.concat(dfs, ignore_index=True)

    # Remove all data not corresponding to the time of the snap
    df = df[df['event'] == 'ball_snap']

    # Make new coords for each unqique play
    df['grid_x'] = df.groupby(['gameId', 'playId']).apply(calculate_x_coords).reset_index(level=[0,1], drop=True)
    df['grid_y'] = df.groupby(['gameId', 'playId']).apply(calculate_y_coords).reset_index(level=[0,1], drop=True)

    # Group by unique play, create grid, and save to dict
    grids = {}
    for id, group in df.groupby(['gameId', 'playId']):
        # Skip over plays that are missing football for some reason
        if len(group.grid_x[group.team == 'football']) > 0:
            # Adjust x coords to be relative to football position.
            # Limits (inclusive) should be
            # offense: 10 yards from ball
            # defense: 24 yards from ball
    
            field = np.zeros((NEW_X_RANGE[1]+1, NEW_Y_RANGE[1]+1))
            off_team = group.team[group.grid_x == max(group.grid_x)].iloc[0]
            def_team = group.team[group.grid_x == min(group.grid_x)].iloc[0]

            field[group.grid_x[group.team == off_team], group.grid_y[group.team == off_team]] = -1
            field[group.grid_x[group.team == def_team], group.grid_y[group.team == def_team]] = 1

            football_x = group.grid_x[group.team == 'football'].iloc[0]
            # NOTE: manually change the ranges here if adjusing grid size. Current: 28x18
            min_x = football_x - 13
            max_x = football_x + 5
            # handle if the range is larger than extent of football field
            if min_x < 0:
                field_shrunk = field[0:max_x, :]
                for i in range(abs(min_x)):
                    np.vstack([np.zeros((1, NEW_Y_RANGE[1]+1)), field_shrunk])
            elif max_x > NEW_X_RANGE[1]:
                field_shrunk = field[min_x:NEW_X_RANGE[1]]
                for i in range(NEW_X_RANGE[1]+1, max_x+1):
                    np.vstack([field_shrunk, np.zeros((1, NEW_Y_RANGE[1]+1))])
            else:
                field_shrunk = field[min_x:max_x, :]
                grids[id] = field_shrunk

    # create csv with gameId, playId, then all the grid points flattened to a list in each row
    arr = np.empty((0, 504))
    for gameId, playId in list(grids.keys()):
        row = grids[(gameId, playId)].flatten().tolist()
        row.insert(0, playId)
        row.insert(0, gameId)
        arr = np.vstack([arr, row])
    np.savetxt(WORK_DIR + '/data/player_positions_basic.csv', arr.astype(int), delimiter=',', fmt='%d')

    # plot 10 random grids and save as png
    some_plays = random.sample(list(grids.keys()), 10)
    for i in range(10):
        plt.imshow(grids[some_plays[i]])
        plt.savefig(WORK_DIR + f'/testimg{i}.png')
        plt.close()

if __name__ == '__main__':
    main()
